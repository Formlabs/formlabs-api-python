"""Web SLS Packer: pack STL parts into Fuse 1+ and Fuse X1 builds from a browser.

Make a job, drop parts onto it, set how many of each and how the packer may turn them, then press Pack. The
app fills one build volume after another with PreForm Server behind it, and each build can be downloaded as a
.form file or sent to a printer. FastAPI serves the pages; htmx swaps in the fragments.

Open PreForm and start its API server on port 44388, then run:

    uv run app.py

and open http://localhost:8323. Set FL_LOCAL_BASE_URL to reach PreForm on another port or host.
"""

from __future__ import annotations

import queue
import shutil
import threading
import time
from collections.abc import Iterator
from contextlib import asynccontextmanager
from pathlib import Path

import trimesh
from fastapi import FastAPI, Form, Request, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import packer
import preform
from formlabs_sdk import FormlabsClient
from jobs import LOCK_LABELS, LOCKS, Build, Job, Part, list_jobs, load_job, new_job

HERE = Path(__file__).resolve().parent
PORT = 8323

templates = Jinja2Templates(directory=HERE / "templates")
templates.env.globals.update(LOCKS=LOCKS, LOCK_LABELS=LOCK_LABELS, printers=preform.printers)
templates.env.globals["cache_key"] = lambda path: int(path.stat().st_mtime) if path.exists() else 0
templates.env.filters["mm"] = lambda v: f"{v:.0f}"
templates.env.filters["ml"] = lambda v: f"{v / 1000:.1f}"
templates.env.filters["when"] = lambda t: time.strftime("%Y-%m-%d %H:%M", time.localtime(t))
templates.env.filters["hm"] = lambda s: f"{int(s // 3600)}h {int(s % 3600 // 60):02d}m" if s is not None else ""
templates.env.filters["printer_label"] = lambda job: preform.printers[job.machine_type].label if job.machine_type in preform.printers else job.machine_type
templates.env.filters["material_label"] = lambda job: (
    preform.printers[job.machine_type].materials.get(job.material_code, {}).get("label", job.material_code)
    if job.machine_type in preform.printers else job.material_code)

_events: dict[str, list[queue.Queue]] = {}
_cancels: dict[str, threading.Event] = {}
_prints: dict[tuple[str, int], preform.PrintUpload] = {}


# --8<-- [start:setup]
@asynccontextmanager
async def lifespan(app: FastAPI):
    with FormlabsClient() as client:
        preform.connect(client)
        for job in list_jobs():
            if job.status == "packing":
                job.status = "failed"
                job.error = "interrupted by an app restart; press Pack again"
                job.save()
        yield


app = FastAPI(title="Web SLS Packer", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=HERE / "static"), name="static")
# --8<-- [end:setup]


def render(request: Request, name: str, **ctx) -> HTMLResponse:
    return templates.TemplateResponse(request, name, ctx)


def fragment(name: str, **ctx) -> str:
    return templates.get_template(name).render(LOCKS=LOCKS, LOCK_LABELS=LOCK_LABELS, **ctx)


def _default_setting() -> str:
    machine_type = next(iter(preform.printers))
    return f"{machine_type}|{preform.default_material(machine_type)}"


def _parse_setting(setting: str) -> tuple[str, str]:
    """A `machine_type|material_code` pair from the printer-and-material select; anything unknown falls back to the default."""
    machine_type, _, material_code = setting.partition("|")
    if machine_type not in preform.printers:
        return _parse_setting(_default_setting())
    if material_code not in preform.printers[machine_type].materials:
        material_code = preform.default_material(machine_type)
    return machine_type, material_code


def _rows_and_summary(job: Job, parts: list[Part]) -> HTMLResponse:
    rows = "".join(fragment("_part_row.html", job=job, part=p) for p in parts)
    return HTMLResponse(rows + fragment("_summary.html", job=job))


def _devices(machine_type: str) -> list[dict]:
    try:
        return preform.devices(machine_type)
    except Exception:
        return []


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return render(request, "index.html", jobs=list_jobs(), default=_default_setting())


@app.post("/jobs")
def create_job(name: str = Form(""), setting: str = Form("")):
    job = new_job(name, *_parse_setting(setting))
    return RedirectResponse(f"/jobs/{job.id}", status_code=303)


@app.delete("/jobs/{job_id}", response_class=HTMLResponse)
def delete_job(job_id: str):
    job = load_job(job_id)
    if job.status == "packing":
        return HTMLResponse(f'<tr><td colspan="8" class="warn">"{job.name}" is still packing; cancel it first.</td></tr>')
    shutil.rmtree(job.dir, ignore_errors=True)
    return HTMLResponse("")


@app.get("/jobs/{job_id}", response_class=HTMLResponse)
def job_page(request: Request, job_id: str):
    job = load_job(job_id)
    return render(request, "job.html", job=job, devices=_devices(job.machine_type))


@app.post("/jobs/{job_id}/setting", response_class=HTMLResponse)
def set_setting(job_id: str, setting: str = Form(...)):
    """Change the job's printer and material. The build volume may change with them, so every part is re-checked."""
    job = load_job(job_id)
    job.machine_type, job.material_code = _parse_setting(setting)
    bv = preform.build_volume(job.machine_type, job.material_code)
    for part in job.parts:
        part.reject_reason = packer.reject_reason(part, bv)
    job.save()
    return _rows_and_summary(job, job.parts)


@app.post("/jobs/{job_id}/options", response_class=HTMLResponse)
def set_options(job_id: str, spacing_mm: str = Form(""), min_density: float = Form(0.12), print_time: str = Form("")):
    job = load_job(job_id)
    try:
        job.spacing_mm = max(0.0, float(spacing_mm)) if spacing_mm.strip() else None
    except ValueError:
        job.spacing_mm = None
    job.min_density = max(0.0, min(min_density, 1.0))
    job.print_time = print_time == "on"
    job.save()
    return HTMLResponse(fragment("_summary.html", job=job))


# --8<-- [start:add_parts]
@app.post("/jobs/{job_id}/parts", response_class=HTMLResponse)
def add_parts(job_id: str, files: list[UploadFile]):
    """Save each mesh, measure it, and render a thumbnail.

    The thumbnail also shows whether PreForm can import the mesh.
    """
    job = load_job(job_id)
    bv = preform.build_volume(job.machine_type, job.material_code)
    added: list[Part] = []
    for upload in files:
        name = upload.filename
        if not name or not name.lower().endswith((".stl", ".obj", ".3mf")):
            continue
        stamp = int(time.time() * 1000) % 10**9
        part = Part(id=f"p{stamp:09d}{len(job.parts) + len(added):02d}",
                    filename=Path(name).name, volume_mm3=0, extents_mm=[0, 0, 0])
        path = job.part_path(part)
        with path.open("wb") as f:
            shutil.copyfileobj(upload.file, f)
        mesh = trimesh.load_mesh(path)
        part.volume_mm3 = float(abs(mesh.volume))
        part.extents_mm = [float(e) for e in mesh.bounding_box.extents]
        part.import_error = preform.thumbnail(job.machine_type, job.material_code,
                                              path, job.thumbnail_path(part))
        part.thumbnail = part.import_error is None
        part.reject_reason = packer.reject_reason(part, bv)
        added.append(part)
    job.parts += added
    job.save()
    return _rows_and_summary(job, added)
# --8<-- [end:add_parts]


@app.post("/jobs/{job_id}/parts/{part_id}", response_class=HTMLResponse)
def update_part(job_id: str, part_id: str, quantity: int | None = Form(None), lock: str | None = Form(None)):
    """Change only the fields the form sent, so a partial post never resets the others."""
    job = load_job(job_id)
    part = job.part(part_id)
    if quantity is not None:
        part.quantity = max(1, quantity)
    if lock in LOCKS:
        part.lock = lock
    part.reject_reason = packer.reject_reason(part, preform.build_volume(job.machine_type, job.material_code))
    job.save()
    return _rows_and_summary(job, [part])


@app.post("/jobs/{job_id}/parts/{part_id}/orientation", response_class=HTMLResponse)
def set_orientation(job_id: str, part_id: str, x: float = Form(...), y: float = Form(...), z: float = Form(...)):
    """Keep a pose chosen in the viewer. A part posed by hand keeps that pose through the pack unless its lock is changed."""
    job = load_job(job_id)
    part = job.part(part_id)
    part.orientation = [round(x, 2), round(y, 2), round(z, 2)]
    part.posed_extents_mm = packer.posed_extents(job.part_path(part), part.orientation)
    if part.lock == "FREE":
        part.lock = "LOCKED_ROTATION"
    part.reject_reason = packer.reject_reason(part, preform.build_volume(job.machine_type, job.material_code))
    part.thumbnail = preform.thumbnail(job.machine_type, job.material_code, job.part_path(part), job.thumbnail_path(part),
                                       orientation=part.orientation) is None
    job.save()
    return _rows_and_summary(job, [part])


@app.delete("/jobs/{job_id}/parts/{part_id}/orientation", response_class=HTMLResponse)
def clear_orientation(job_id: str, part_id: str):
    job = load_job(job_id)
    part = job.part(part_id)
    part.orientation, part.posed_extents_mm = None, None
    if part.lock == "LOCKED_ROTATION":
        part.lock = "FREE"
    part.reject_reason = packer.reject_reason(part, preform.build_volume(job.machine_type, job.material_code))
    part.thumbnail = preform.thumbnail(job.machine_type, job.material_code, job.part_path(part), job.thumbnail_path(part)) is None
    job.save()
    return _rows_and_summary(job, [part])


@app.delete("/jobs/{job_id}/parts/{part_id}", response_class=HTMLResponse)
def delete_part(job_id: str, part_id: str):
    job = load_job(job_id)
    part = job.part(part_id)
    job.parts.remove(part)
    job.part_path(part).unlink(missing_ok=True)
    job.thumbnail_path(part).unlink(missing_ok=True)
    job.save()
    return HTMLResponse(fragment("_summary.html", job=job))


@app.get("/jobs/{job_id}/parts/{part_id}.stl")
def part_mesh(job_id: str, part_id: str):
    job = load_job(job_id)
    part = job.part(part_id)
    return FileResponse(job.part_path(part), media_type="model/stl", filename=part.filename)


@app.get("/jobs/{job_id}/parts/{part_id}.png")
def part_thumbnail(job_id: str, part_id: str):
    job = load_job(job_id)
    return FileResponse(job.thumbnail_path(job.part(part_id)), media_type="image/png")


@app.post("/jobs/{job_id}/pack", response_class=HTMLResponse)
def start_pack(job_id: str):
    """Pack in a background thread; the page follows along on /events."""
    job = load_job(job_id)
    if job.status != "packing":
        job.status, job.error = "packing", ""
        job.builds, job.unplaceable = [], []
        for stale in job.dir.glob("builds/*"):
            stale.unlink()
        job.save()
        _cancels[job.id] = threading.Event()
        threading.Thread(target=_pack_worker, args=(job,), daemon=True).start()
    return HTMLResponse(fragment("_builds.html", job=job, devices=[]) + fragment("_summary.html", job=job))


def _pack_worker(job: Job) -> None:
    devices = _devices(job.machine_type)

    def on_build(build: Build) -> None:
        publish(job.id, "build", fragment("_build_card.html", job=job, build=build, devices=devices))
    try:
        packer.run(job, on_build, _cancels.get(job.id))
        job.status = "done"
    except packer.Cancelled:
        job.status = "cancelled"
    except Exception as exc:
        job.status, job.error = "failed", str(exc)[:300]
    job.save()
    # The summary rides along out of band, so the Pack button comes back when the stream ends.
    publish(job.id, "done", fragment("_builds.html", job=job, devices=devices) + fragment("_summary.html", job=job))


@app.post("/jobs/{job_id}/cancel", response_class=HTMLResponse)
def cancel_pack(job_id: str):
    """Stop after the build being packed now; the page updates when the stream's done event arrives."""
    if (event := _cancels.get(job_id)) is not None:
        event.set()
    return HTMLResponse('<p aria-busy="true">Cancelling after the current build…</p>')


def publish(job_id: str, event: str, html: str) -> None:
    for q in _events.get(job_id, []):
        q.put((event, html))


@app.get("/jobs/{job_id}/events")
def events(job_id: str):
    """Server-sent events: each finished build as a `build` event, then `done` with the final page fragments."""
    q: queue.Queue = queue.Queue()
    _events.setdefault(job_id, []).append(q)

    def stream() -> Iterator[str]:
        try:
            while True:
                try:
                    event, html = q.get(timeout=15)
                except queue.Empty:
                    yield ": keep-alive\n\n"
                    continue
                yield f"event: {event}\ndata: {html.replace(chr(10), ' ')}\n\n"
                if event == "done":
                    return
        finally:
            _events[job_id].remove(q)

    return StreamingResponse(stream(), media_type="text/event-stream")


@app.get("/jobs/{job_id}/builds/{number}.{suffix}")
def build_file(job_id: str, number: int, suffix: str):
    job = load_job(job_id)
    if suffix == "png":
        return FileResponse(job.build_path(number, ".png"), media_type="image/png")
    return FileResponse(job.build_path(number, ".form"), media_type="application/octet-stream",
                        filename=f"{job.name} build {number:03d}.form")


@app.post("/jobs/{job_id}/builds/{number}/print", response_class=HTMLResponse)
def print_build(job_id: str, number: int, printer: str = Form(...)):
    job = load_job(job_id)
    current = _prints.get((job_id, number))
    if current is None or current.status in ("done", "failed"):
        _prints[(job_id, number)] = preform.PrintUpload(job.build_path(number, ".form"), printer.strip(), f"{job.name} build {number}")
    return HTMLResponse(fragment("_print_status.html", job=job, number=number, upload=_prints[(job_id, number)]))


@app.get("/jobs/{job_id}/builds/{number}/print-status", response_class=HTMLResponse)
def print_status(job_id: str, number: int):
    return HTMLResponse(fragment("_print_status.html", job=load_job(job_id), number=number, upload=_prints.get((job_id, number))))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=PORT)
