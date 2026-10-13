"""Jobs on disk: jobs/<id>/job.json, with the job's parts, thumbnails and builds beside it."""

from __future__ import annotations

import dataclasses
import json
import secrets
import time
from dataclasses import dataclass, field
from pathlib import Path

JOBS_DIR = Path(__file__).resolve().parent / "jobs"
# A build packed less densely than this is marked for a person to look at before it prints.
MIN_DENSITY = 0.12

LOCKS = ("FREE", "XY_LOCKED", "LOCKED_ROTATION")
LOCK_LABELS = {"FREE": "Free", "XY_LOCKED": "Keep Z up (XY locked)", "LOCKED_ROTATION": "Keep this pose"}


@dataclass
class Part:
    id: str
    filename: str
    volume_mm3: float
    extents_mm: list[float]
    quantity: int = 1
    lock: str = "FREE"
    thumbnail: bool = False
    reject_reason: str | None = None
    import_error: str | None = None             # PreForm could not import the file, even with repair
    orientation: list[float] | None = None      # degrees about x, y, z, as orient_models takes them; None is the file's pose
    posed_extents_mm: list[float] | None = None

    @property
    def footprint_extents(self) -> list[float]:
        return self.posed_extents_mm or self.extents_mm


@dataclass
class Build:
    number: int
    models: dict[str, int]                      # part filename to copies in this build
    carried: list[str]                          # offered to this build but not placed, so packed later
    height_mm: float
    density: float
    released: bool                              # packed at least MIN_DENSITY
    print_time_s: float | None = None
    cool_time_s: float | None = None
    powder_kg: float | None = None
    sintered_kg: float | None = None


@dataclass
class Job:
    id: str
    name: str
    created: float
    machine_type: str
    material_code: str
    parts: list[Part] = field(default_factory=list)
    builds: list[Build] = field(default_factory=list)
    unplaceable: list[str] = field(default_factory=list)
    status: str = "editing"                     # editing | packing | done | cancelled | failed
    error: str = ""
    spacing_mm: float | None = None             # None leaves PreForm's default gap between models
    min_density: float = MIN_DENSITY
    print_time: bool = False                    # slice each build for its print time, 10 to 30 s more per build

    @property
    def dir(self) -> Path:
        return JOBS_DIR / self.id

    def part(self, part_id: str) -> Part:
        return next(p for p in self.parts if p.id == part_id)

    def part_path(self, part: Part) -> Path:
        return self.dir / "parts" / f"{part.id}_{part.filename}"

    def thumbnail_path(self, part: Part) -> Path:
        return self.dir / "parts" / f"{part.id}.png"

    def build_path(self, number: int, suffix: str) -> Path:
        return self.dir / "builds" / f"build_{number:03d}{suffix}"

    @property
    def model_count(self) -> int:
        return sum(p.quantity for p in self.parts if not p.reject_reason)

    @property
    def models_volume_mm3(self) -> float:
        return sum(p.volume_mm3 * p.quantity for p in self.parts if not p.reject_reason)

    def save(self) -> None:
        self.dir.mkdir(parents=True, exist_ok=True)
        (self.dir / "job.json").write_text(json.dumps(dataclasses.asdict(self), indent=1))


def new_job(name: str, machine_type: str, material_code: str) -> Job:
    job = Job(id=secrets.token_hex(4), name=name.strip() or time.strftime("Job %Y-%m-%d %H:%M"), created=time.time(),
              machine_type=machine_type, material_code=material_code)
    (job.dir / "parts").mkdir(parents=True, exist_ok=True)
    (job.dir / "builds").mkdir(parents=True, exist_ok=True)
    job.save()
    return job


def load_job(job_id: str) -> Job:
    raw = json.loads((JOBS_DIR / job_id / "job.json").read_text())
    raw["parts"] = [Part(**p) for p in raw["parts"]]
    raw["builds"] = [Build(**b) for b in raw["builds"]]
    return Job(**raw)


def list_jobs() -> list[Job]:
    jobs = [load_job(p.name) for p in JOBS_DIR.iterdir() if (p / "job.json").is_file()] if JOBS_DIR.is_dir() else []
    return sorted(jobs, key=lambda j: j.created, reverse=True)
