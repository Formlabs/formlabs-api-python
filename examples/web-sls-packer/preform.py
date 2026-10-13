"""The PreForm Server this app packs with, and what its print-setting catalog says about each printer."""

from __future__ import annotations

import os
import threading
from dataclasses import dataclass, field
from pathlib import Path

from formlabs_preform_api.models import EulerAngles, RenderViewType, RepairBehavior
from formlabs_sdk import FormlabsClient, PreFormApi, PreFormApiError

PREFORM_URL = os.environ.get("FL_LOCAL_BASE_URL", "http://localhost:44388")
# The printers a job can target, in the order they are offered: Fuse 1+ 30W and Fuse X1.
MACHINE_TYPES = ("FS30-1-0", "FUSX-1-0")
DEFAULT_MATERIAL = "FLP12G01"  # Nylon 12

api: PreFormApi  # bound by connect()


@dataclass
class Printer:
    """One machine type a job can target, as PreForm's print-setting catalog describes it."""
    machine_type: str
    label: str
    product_names: set[str] = field(default_factory=set)   # what list_devices reports for printers of this type
    materials: dict[str, dict] = field(default_factory=dict)

    @property
    def material_list(self) -> list[dict]:
        return sorted(self.materials.values(), key=lambda m: m["label"])


printers: dict[str, Printer] = {}


def connect(client: FormlabsClient) -> None:
    """Attach to the PreForm Server at PREFORM_URL and read which of MACHINE_TYPES it has print settings for."""
    global api
    api = client.preform.connect(base_url=PREFORM_URL)
    load_printers()
    if not printers:
        raise RuntimeError(f"the PreForm Server at {PREFORM_URL} has no print settings for {', '.join(MACHINE_TYPES)}")


def load_printers() -> None:
    """Keep every material the catalog lists for MACHINE_TYPES, with the print setting Formlabs marks as default."""
    found: dict[str, Printer] = {}
    for group in api.list_print_settings().to_dict()["printer_types"]:
        for material in group["materials"]:
            chosen = default_setting(material["material_settings"])
            settings = chosen["scene_settings"]
            if settings["machine_type"] not in MACHINE_TYPES:
                continue
            printer = found.setdefault(settings["machine_type"], Printer(settings["machine_type"], group["label"]))
            printer.product_names.update(group.get("supported_product_names", []))
            printer.materials.setdefault(settings["material_code"], {
                "code": settings["material_code"], "label": material["label"],
                "print_setting": settings["print_setting"], "layer_thickness_mm": float(settings["layer_thickness_mm"]),
                "setting_label": chosen["label"].replace(" settings", "").replace(")", "").split("(")[-1],
            })
    printers.clear()
    printers.update({mt: found[mt] for mt in MACHINE_TYPES if mt in found})


def default_setting(settings: list[dict]) -> dict:
    """The setting labelled as the default, else the first whose code starts with DEFAULT, else the first."""
    for s in settings:
        if "(Default settings)" in s["label"]:
            return s
    return next((s for s in settings if s["scene_settings"]["print_setting"].startswith("DEFAULT")), settings[0])


def default_material(machine_type: str) -> str:
    printer = printers[machine_type]
    return DEFAULT_MATERIAL if DEFAULT_MATERIAL in printer.materials else printer.material_list[0]["code"]


def scene_settings(machine_type: str, material_code: str) -> dict:
    material = printers[machine_type].materials[material_code]
    return {"machine_type": machine_type, "material_code": material_code,
            "print_setting": material["print_setting"], "layer_thickness_mm": material["layer_thickness_mm"]}


_build_volumes: dict[tuple[str, str], tuple[float, float, float]] = {}


def build_volume(machine_type: str, material_code: str) -> tuple[float, float, float]:
    """The printer's build volume in millimetres, read once from a scene created for it."""
    key = (machine_type, material_code)
    if key not in _build_volumes:
        scene_id = str(api.create_scene(**scene_settings(machine_type, material_code)).scene_id)
        try:
            d = api.get_scene(scene_id=scene_id).build_volume.dimensions_mm
            _build_volumes[key] = (d.x, d.y, d.z)
        finally:
            api.delete_scene(scene_id=scene_id)
    return _build_volumes[key]


def import_part(scene_id: str, path: Path, filename: str) -> list[str]:
    """Import one part file and return its models' ids. REPAIR mends a damaged mesh on the way in, where the
    default would refuse it; an import that still fails names the file, which PreForm's own message does not."""
    try:
        imported = api.import_models(scene_id=scene_id, file=str(path), name=filename.rsplit(".", 1)[0],
                                     repair_behavior=RepairBehavior.REPAIR)
    except PreFormApiError as exc:
        raise PreFormApiError(exc.code, f"{filename}: {exc.message}") from exc
    return [str(m.model_id) for m in imported.new_models]


def thumbnail(machine_type: str, material_code: str, stl: Path, out: Path, orientation: list[float] | None = None) -> str | None:
    """Render one part on its own, in its chosen pose if it has one. Returns PreForm's message if it could not
    import the file, else None."""
    scene_id = str(api.create_scene(**scene_settings(machine_type, material_code)).scene_id)
    try:
        model_ids = import_part(scene_id, stl, stl.name)
        if orientation:
            x, y, z = orientation
            api.orient_models(scene_id=scene_id, model_ids=model_ids, orientation=EulerAngles(x=x, y=y, z=z))
        api.render_scene(scene_id=scene_id, file=str(out), view_type=RenderViewType.ZOOM_ON_MODELS,
                         image_size_px=320, crop_to_models=True)
        return None
    except PreFormApiError as exc:
        return exc.message.split(": ", 1)[-1]
    finally:
        api.delete_scene(scene_id=scene_id)


def devices(machine_type: str) -> list[dict]:
    """Connected printers that can take this machine type's builds, idle ones first."""
    names = printers[machine_type].product_names if machine_type in printers else set()
    found = [d.to_dict() for d in api.list_devices().devices]
    found = [d for d in found if d.get("is_connected") and d.get("product_name") in names]
    return sorted(found, key=lambda d: (d.get("status") != "Idle", d.get("id", "")))


class PrintUpload:
    """Slice one build and upload it to a printer in the background; the page polls `status` and `progress`."""

    def __init__(self, form: Path, printer: str, job_name: str):
        self.printer, self.job_name = printer, job_name
        self.status, self.progress, self.message = "starting", 0.0, ""
        threading.Thread(target=self._run, args=(form,), daemon=True).start()

    def _run(self, form: Path) -> None:
        scene_ids: list[str] = []
        try:
            scene_ids = [str(s.scene_id) for s in api.open_form_file(file=str(form)).scenes]
            self.status = "slicing"
            api.print_scene(scene_id=scene_ids[0], printer=self.printer, job_name=self.job_name,
                            find_printer_timeout_seconds=20, print_now=False,
                            on_progress=lambda fraction: setattr(self, "progress", fraction))
            self.status, self.progress = "done", 1.0
            self.message = f"Uploaded to {self.printer} as '{self.job_name}'. Start it from the printer."
        except Exception as exc:
            self.status, self.message = "failed", f"Could not print on {self.printer}: {getattr(exc, 'message', str(exc))[:200]}"
        finally:
            for scene_id in scene_ids:
                api.delete_scene(scene_id=scene_id)
