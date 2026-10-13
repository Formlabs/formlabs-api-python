"""Drain a job's parts into builds, letting PreForm's packer decide what fits in each.

Each build starts as one scene holding about one build's worth of the queue, mixed across part types so the
packer can nest small parts around large ones. auto_pack_models runs with PARK_OUTSIDE_BUILD_VOLUME: the models
it placed make the build, and the ones it could not are deleted from the scene and go back to the head of the
queue for the next build.
"""

from __future__ import annotations

import bisect
import math
import threading
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

from formlabs_preform_api.models import EulerAngles, OnPackFailure, RenderViewType
from formlabs_preform_api.types import UNSET

import preform
from jobs import Build, Job, Part

API_LOCKS = {"FREE": "FREE", "XY_LOCKED": "LOCKED_XY_ROTATION_FREE_TRANSLATION", "LOCKED_ROTATION": "LOCKED_ROTATION_FREE_TRANSLATION"}
MAX_MODELS_PER_PACK = 400
# About 30% mass packing density is as dense as a Fuse build gets, so one build's worth of parts is roughly
# 30% of the build volume.
FULL_BUILD_FRACTION = 0.30


class Cancelled(Exception):
    pass


@dataclass(frozen=True, order=True)
class Model:
    """One copy of a part in the queue, ordered by when it joined it."""
    seq: int
    part: Part = field(compare=False)


def reject_reason(part: Part, bv: tuple[float, float, float]) -> str | None:
    """Why a part can never fit this build volume in its lock, or None."""
    if part.import_error:
        return f"PreForm cannot import this file: {part.import_error}"
    ex, ey, ez = part.footprint_extents
    bx, by, bz = bv
    if part.lock == "FREE":
        longest, diagonal = max(ex, ey, ez), math.hypot(bx, by, bz)
        return f"longest extent {longest:.0f} mm exceeds the build volume diagonal {diagonal:.0f} mm" if longest > diagonal else None
    if ez > bz:
        return f"height {ez:.0f} mm exceeds the build volume height {bz:.0f} mm"
    if part.lock == "LOCKED_ROTATION":
        if ex > bx or ey > by:
            return f"footprint {ex:.0f}x{ey:.0f} mm exceeds the {bx:.0f}x{by:.0f} mm build area in this pose"
        return None
    if min(ex, ey) > max(bx, by) or math.hypot(ex, ey) > math.hypot(bx, by):
        return f"footprint {ex:.0f}x{ey:.0f} mm cannot fit the {bx:.0f}x{by:.0f} mm build area at any spin"
    return None


def posed_extents(path: Path, orientation: list[float]) -> list[float]:
    """The part's size once turned to `orientation`. orient_models composes x, y, z degrees as Ry * Rx * Rz."""
    import numpy as np
    import trimesh

    x, y, z = (math.radians(a) for a in orientation)
    rx = np.array([[1, 0, 0], [0, math.cos(x), -math.sin(x)], [0, math.sin(x), math.cos(x)]])
    ry = np.array([[math.cos(y), 0, math.sin(y)], [0, 1, 0], [-math.sin(y), 0, math.cos(y)]])
    rz = np.array([[math.cos(z), -math.sin(z), 0], [math.sin(z), math.cos(z), 0], [0, 0, 1]])
    v = trimesh.load_mesh(path).vertices @ (ry @ rx @ rz).T
    return [float(e) for e in (v.max(0) - v.min(0))]


class Packer:
    def __init__(self, job: Job, cancel: threading.Event | None = None):
        self.job = job
        self.cancel = cancel or threading.Event()
        self.api = preform.api
        self.bv = preform.build_volume(job.machine_type, job.material_code)

    def candidates(self, queue: list[Model]) -> list[Model]:
        """Take one build's worth of models from the queue, one of each part type in turn so the packer sees a mix."""
        x, y, z = self.bv
        cap_mm3 = FULL_BUILD_FRACTION * x * y * z
        lanes: dict[str, list[Model]] = {}
        for m in queue:
            lanes.setdefault(m.part.id, []).append(m)
        chosen: list[Model] = []
        volume = 0.0
        while lanes and len(chosen) < MAX_MODELS_PER_PACK and volume < cap_mm3:
            for part_id in list(lanes):
                m = lanes[part_id].pop(0)
                chosen.append(m)
                volume += m.part.volume_mm3
                if not lanes[part_id]:
                    del lanes[part_id]
                if len(chosen) >= MAX_MODELS_PER_PACK or volume >= cap_mm3:
                    break
        for m in chosen:
            queue.remove(m)
        return chosen

    def stage(self, scene_id: str, models: list[Model]) -> dict[str, Model]:
        """Import each part type once, duplicate it for its copies, orient and lock them, and map model ids to Models."""
        by_part: dict[str, list[Model]] = {}
        for m in models:
            by_part.setdefault(m.part.id, []).append(m)
        mapping: dict[str, Model] = {}
        for copies in by_part.values():
            part = copies[0].part
            ids = preform.import_part(scene_id, self.job.part_path(part), part.filename)
            if len(copies) > 1:
                duplicated = self.api.duplicate_models(scene_id=scene_id, model_ids=ids, count=len(copies) - 1)
                ids += [str(i) for i in duplicated.results[0].new_model_ids]
            if part.orientation:
                x, y, z = part.orientation
                self.api.orient_models(scene_id=scene_id, model_ids=ids, orientation=EulerAngles(x=x, y=y, z=z))
            self.api.update_models(scene_id=scene_id, model_ids=ids, lock=API_LOCKS[part.lock])
            mapping.update(zip(ids, copies))
        return mapping

    def finish(self, scene_id: str, number: int) -> dict:
        """Save the packed scene as build `number`, render it, and measure it."""
        state = self.api.get_scene(scene_id=scene_id)
        usage = state.material_usage
        self.api.save_form_file(file=str(self.job.build_path(number, ".form")), scene_ids=[scene_id],
                                project_name=f"{self.job.name} build {number}")
        self.api.render_scene(scene_id=scene_id, file=str(self.job.build_path(number, ".png")),
                              view_type=RenderViewType.FULL_BUILD_VOLUME, image_size_px=700,
                              yaw=30, pitch=25, crop_to_models=True)
        times = self.api.calculate_print_time(scene_id=scene_id) if self.job.print_time else None
        return {
            "height": max(m.bounding_box.max_corner.z for m in state.models),
            "density": usage.mass_packing_density,
            "print_time_s": (times.printing_time_s + times.preprint_time_s) if times else None,
            "cool_time_s": times.cool_to_removal_time_s if times else None,
            "powder_kg": usage.total_powder_kg, "sintered_kg": usage.total_sintered_powder_kg,
        }


# --8<-- [start:run]
def run(job: Job, on_build: Callable[[Build], None],
        cancel: threading.Event | None = None) -> None:
    """Pack the job's parts into builds, saving the job after each.

    Raises Cancelled between builds when asked.
    """
    packer = Packer(job, cancel)
    queue: list[Model] = []
    for part in job.parts:
        part.reject_reason = reject_reason(part, packer.bv)
        if not part.reject_reason:
            queue += [Model(len(queue) + i, part) for i in range(part.quantity)]
    job.builds, job.unplaceable = [], []
    while queue:
        if packer.cancel.is_set():
            raise Cancelled("packing cancelled")
        chosen = packer.candidates(queue)
        settings = preform.scene_settings(job.machine_type, job.material_code)
        scene_id = str(packer.api.create_scene(**settings).scene_id)
        spacing = job.spacing_mm if job.spacing_mm is not None else UNSET
        try:
            mapping = packer.stage(scene_id, chosen)
            packed = packer.api.auto_pack_models(
                scene_id=scene_id, seed=7, model_spacing_mm=spacing,
                on_pack_failure=OnPackFailure.PARK_OUTSIDE_BUILD_VOLUME)
            landed = [mapping[str(i)] for i in packed.packed_model_ids]
            carried = [mapping[str(i)] for i in packed.unpacked_model_ids]
            if not landed:
                # Nothing fit, though every part passed reject_reason: the oldest
                # part cannot be placed in its lock.
                culprit = min(chosen, key=lambda m: m.seq).part
                job.unplaceable.append(culprit.filename)
                for m in chosen:
                    if m.part is not culprit:
                        bisect.insort(queue, m)
                continue
            for m in carried:
                bisect.insort(queue, m)
            if carried:
                packer.api.delete_models(
                    scene_id=scene_id,
                    model_ids=[str(i) for i in packed.unpacked_model_ids])
            result = packer.finish(scene_id, len(job.builds) + 1)
        finally:
            packer.api.delete_scene(scene_id=scene_id)
        counts: dict[str, int] = {}
        for m in landed:
            counts[m.part.filename] = counts.get(m.part.filename, 0) + 1
        build = Build(len(job.builds) + 1, counts, [m.part.filename for m in carried],
                      round(result["height"], 1), round(result["density"], 4),
                      result["density"] >= job.min_density, result["print_time_s"],
                      result["cool_time_s"], round(result["powder_kg"], 3),
                      round(result["sintered_kg"], 3))
        job.builds.append(build)
        job.save()
        on_build(build)
# --8<-- [end:run]
