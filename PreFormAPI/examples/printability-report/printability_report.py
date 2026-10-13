"""Check a set of STL files before a job is confirmed: will each part print as it is?

An order system receives STL files from customers. Before the job is confirmed, an
operator needs to know which parts print as delivered, which need a word with the
customer, and which can't print at all. Each part gets PASS, WARN, or FAIL with its
findings, and the script exits with status 1 if any part fails.

Open PreForm and start its API server on port 44388, then run:

    uv run printability_report.py order-1234 --screenshots renders
    uv run printability_report.py order-1234 --repair --json > report.json

Set FL_LOCAL_BASE_URL to reach PreForm on another port or host.
"""

import argparse
import json
import os
import sys
from collections import defaultdict
from pathlib import Path
from uuid import UUID

from formlabs_sdk import FormlabsClient, PreFormApi, PreFormApiError
from formlabs_preform_api.models import (
    OnLayoutFailure,
    RenderViewType,
    RepairBehavior,
    ThinWallDetectionResultStatus,
)

PREFORM_URL = os.environ.get("FL_LOCAL_BASE_URL", "http://localhost:44388")
MACHINE_TYPE = "FORM-4-0"
PASS, WARN, FAIL = "PASS", "WARN", "FAIL"
# A part with more than this percentage of its surface under-supported gets a warning.
MAX_UNSUPPORTED_PERCENT = 1.0
MESH_SUFFIXES = {".stl", ".obj", ".3mf"}

Findings = dict[str, list[tuple[str, str]]]


def collect_parts(paths: list[Path]) -> list[Path]:
    """Expand each folder into the mesh files it holds, so an order folder can be checked whole."""
    parts: list[Path] = []
    for path in paths:
        if path.is_dir():
            parts += sorted(p for p in path.iterdir() if p.suffix.lower() in MESH_SUFFIXES)
        else:
            parts.append(path)
    return parts


def import_parts(
    preform: PreFormApi, scene_id: UUID, parts: list[Path], findings: Findings
) -> dict[str, str]:
    """Import each file as delivered and return a map of model ID to part name."""
    names: dict[str, str] = {}
    for part in parts:
        findings[part.stem] = []
        try:
            # IGNORE imports the mesh as the customer sent it, so the manifold check
            # sees any holes. The default, ERROR, fails the import of such a mesh.
            result = preform.import_models(
                scene_id=scene_id,
                file=str(part.resolve()),
                name=part.stem,
                repair_behavior=RepairBehavior.IGNORE,
            )
        except PreFormApiError as exc:
            findings[part.stem].append((FAIL, f"could not import: {exc.message}"))
            continue
        for model in result.new_models:
            names[str(model.model_id)] = part.stem
    return names


def check_meshes(preform: PreFormApi, scene_id: UUID, names: dict[str, str],
                 findings: Findings, thin_mm: float, repair: bool) -> None:
    """Check each mesh for holes and walls thinner than thin_mm."""
    manifold = preform.validate_manifoldness(scene_id=scene_id).per_model_results
    broken = [
        model_id
        for model_id, result in manifold.additional_properties.items()
        if not result.is_manifold
    ]
    if broken and repair:
        repaired = preform.repair_models(
            scene_id=scene_id, model_ids=broken
        ).per_model_results
        for model_id in broken:
            if model_id in repaired and repaired[model_id].is_manifold:
                findings[names[model_id]].append(
                    (WARN, "not manifold; repaired, check it with the customer")
                )
            else:
                findings[names[model_id]].append(
                    (FAIL, "not manifold; repair did not fix it")
                )
    else:
        for model_id in broken:
            findings[names[model_id]].append(
                (FAIL, "not manifold (holes or self-intersections); "
                       "rerun with --repair")
            )

    thin = preform.validate_thin_features(
        scene_id=scene_id, threshold_mm=thin_mm
    ).per_model_results
    for model_id, result in thin.additional_properties.items():
        # Any status other than ANALYZED means the model could not be assessed, such as
        # a mesh with holes.
        if result.status != ThinWallDetectionResultStatus.ANALYZED:
            findings[names[model_id]].append(
                (WARN, f"wall thickness not checked ({result.status})")
            )
        elif result.has_thin_walls:
            findings[names[model_id]].append(
                (WARN, f"{result.thin_region_count} region(s) thinner than {thin_mm} mm, "
                       f"{result.thin_volume_mm3:.1f} mm3")
            )


def check_layout(
    preform: PreFormApi, scene_id: UUID, names: dict[str, str], findings: Findings
) -> None:
    """Lay the parts out on one build platform and report the ones that don't fit."""
    # EJECT_A_MODEL_AND_RETRY removes parts from the scene, picked at random, until the
    # rest fit. The cup and support checks fail for the whole scene while any model is
    # out of bounds, so layout runs before them.
    layout = preform.auto_layout_models(
        scene_id=scene_id, on_layout_failure=OnLayoutFailure.EJECT_A_MODEL_AND_RETRY
    )
    for model_id in layout.ejected_model_ids:
        findings[names[str(model_id)]].append(
            (FAIL, "does not fit on the build platform")
        )
    for pair in preform.validate_interferences(scene_id=scene_id).model_ids:
        for model_id in pair:
            findings[names[str(model_id)]].append(
                (FAIL, "collides with another part after layout")
            )
    for model in preform.list_models(scene_id=scene_id).models:
        if not model.in_bounds:
            findings[names[str(model.id)]].append((FAIL, "outside the build volume"))


def check_printability(
    preform: PreFormApi, scene_id: UUID, names: dict[str, str], findings: Findings
) -> None:
    """Check for cups that trap resin, then support each part and check its supports."""
    cups = preform.validate_cups(scene_id=scene_id).per_model_results
    for model_id, result in cups.additional_properties.items():
        if result.cup_count:
            findings[names[model_id]].append(
                (FAIL, f"{result.cup_count} cup(s) that trap resin; "
                       "reorient or add drain holes")
            )

    preform.auto_support_models(scene_id=scene_id)
    minima = preform.validate_minima(scene_id=scene_id).per_model_results
    for model_id, result in minima.additional_properties.items():
        if result.minima_count:
            findings[names[model_id]].append(
                (FAIL, f"{result.minima_count} unsupported minima after auto-support")
            )

    supported = preform.validate_supportedness(scene_id=scene_id).per_model_results
    for model_id, result in supported.additional_properties.items():
        if result.percent_unsupported > MAX_UNSUPPORTED_PERCENT:
            findings[names[model_id]].append(
                (WARN, f"{result.percent_unsupported:.0f}% of the surface under-supported")
            )


def render_offenders(preform: PreFormApi, scene_id: UUID, names: dict[str, str],
                     findings: Findings, folder: Path) -> None:
    """Render a picture of every part that did not pass, framed on that part alone."""
    folder.mkdir(parents=True, exist_ok=True)
    # Parts that layout ejected are no longer in the scene, so they get no picture.
    for model in preform.list_models(scene_id=scene_id).models:
        name = names[str(model.id)]
        if findings[name]:
            preform.render_scene(
                scene_id=scene_id,
                file=str((folder / f"{name}.png").resolve()),
                model_ids=[model.id],
                view_type=RenderViewType.ZOOM_ON_MODELS,
                image_size_px=600,
            )


def printability_report(preform: PreFormApi, parts: list[Path], material: str,
                        thin_mm: float, repair: bool,
                        screenshots: Path | None) -> list[dict]:
    """Run every check on the parts in one scene and grade each PASS, WARN, or FAIL."""
    scene = preform.create_scene(
        machine_type=MACHINE_TYPE,
        material_code=material,
        layer_thickness_mm=0.1,
        print_setting="DEFAULT",
    )
    findings: Findings = defaultdict(list)
    try:
        names = import_parts(preform, scene.scene_id, parts, findings)
        if names:
            check_meshes(preform, scene.scene_id, names, findings, thin_mm, repair)
            check_layout(preform, scene.scene_id, names, findings)
            check_printability(preform, scene.scene_id, names, findings)
            if screenshots:
                render_offenders(preform, scene.scene_id, names, findings, screenshots)
    finally:
        preform.delete_scene(scene_id=scene.scene_id)

    report = []
    for name, items in findings.items():
        levels = {level for level, _ in items}
        status = FAIL if FAIL in levels else WARN if WARN in levels else PASS
        report.append({
            "part": name,
            "status": status,
            "findings": [{"level": level, "message": message} for level, message in items],
        })
    return report


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("parts", nargs="+", type=Path,
                        help="STL, OBJ, or 3MF files, or folders of them")
    parser.add_argument("--repair", action="store_true",
                        help="repair non-manifold parts and check again")
    parser.add_argument("--thin-mm", type=float, default=0.5,
                        help="warn about walls thinner than this")
    parser.add_argument("--material", default="FLGPGR05",
                        help="material code to support and lay out with")
    parser.add_argument("--screenshots", type=Path,
                        help="folder for a picture of each part that did not pass")
    parser.add_argument("--json", action="store_true", help="print the report as JSON")
    args = parser.parse_args()

    with FormlabsClient() as client:
        try:
            preform = client.preform.connect(base_url=PREFORM_URL)
        except PreFormApiError as exc:
            sys.exit(f"{exc}\nNo PreForm at {PREFORM_URL}; "
                     "open PreForm and start its API server")
        parts = collect_parts(args.parts)
        report = printability_report(preform, parts, args.material, args.thin_mm,
                                     args.repair, args.screenshots)

    counts = {status: sum(entry["status"] == status for entry in report)
              for status in (PASS, WARN, FAIL)}
    if args.json:
        print(json.dumps(report, indent=1))
    else:
        for entry in report:
            print(f"{entry['status']} {entry['part']}")
            for finding in entry["findings"]:
                print(f"     {finding['level']}: {finding['message']}")
        print(f"\n{len(report)} parts: {counts[PASS]} pass, "
              f"{counts[WARN]} warn, {counts[FAIL]} fail")
    # A non-zero exit lets an order system or a CI pipeline hold the job.
    sys.exit(1 if counts[FAIL] else 0)


if __name__ == "__main__":
    main()
