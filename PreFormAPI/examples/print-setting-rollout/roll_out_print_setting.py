"""Move every queued job from one print setting to another, and save the jobs again.

A lab has jobs queued on version 3 of a tuned print setting when version 4 is approved.
The production lead wants every v3 job moved to v4, wants to see what the change does
to layer counts and print times first, and wants jobs on other settings left alone.

Open PreForm and start its API server on port 44388, then preview and roll out:

    uv run roll_out_print_setting.py lab_arches_v4.fps queue --only-from "Lab arches v3" --dry-run --print-time
    uv run roll_out_print_setting.py lab_arches_v4.fps queue --only-from "Lab arches v3" --out queue-v4

A shipped setting works as the target too: --shipped FORM-4-0 FLFMGR01 DEFAULT 0.2.
Set FL_LOCAL_BASE_URL to reach PreForm on another port or host.
"""

import argparse
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from uuid import UUID

from formlabs_sdk import FormlabsClient, PreFormApi, PreFormApiError

PREFORM_URL = os.environ.get("FL_LOCAL_BASE_URL", "http://localhost:44388")
SKIPPED = "skipped, other setting"


@dataclass
class Row:
    label: str
    setting: str
    layers: str
    print_time: str = ""
    status: str = ""


def setting_name(preform: PreFormApi, scene_id: UUID) -> str:
    return preform.get_scene_metadata(scene_id=scene_id)["PrintSettingsName"]


def describe(preform: PreFormApi, scene_id: UUID) -> str:
    settings = preform.get_scene(scene_id=scene_id).scene_settings
    return (
        f"{setting_name(preform, scene_id)} ({settings.machine_type}, {settings.material_code}, "
        f"{settings.print_setting} at {settings.layer_thickness_mm} mm)"
    )


def check_target(preform: PreFormApi, target: dict) -> str:
    """Create an empty scene on the target setting, so a bad setting stops the run."""
    if "fps_file" not in target and not preform.validate_print_setting(**target).valid:
        sys.exit(f"No shipped print setting matches {target}")
    scene = preform.create_scene(**target)
    try:
        return describe(preform, scene.scene_id)
    finally:
        preform.delete_scene(scene_id=scene.scene_id)


def print_time(preform: PreFormApi, scene_id: UUID) -> str:
    seconds = preform.calculate_print_time(scene_id=scene_id).total_print_time_s
    return f"{seconds // 3600}h {seconds % 3600 // 60:02d}m"


def roll_out(
    preform: PreFormApi,
    form: Path,
    target: dict,
    only_from: str | None,
    out: Path | None,
    with_time: bool,
) -> list[Row]:
    """Change each build volume in a .form file to the target, then save the file."""
    opened = preform.open_form_file(file=str(form.resolve()))
    rows: list[Row] = []
    try:
        for scene in opened.scenes:
            label = form.name
            if len(opened.scenes) > 1:
                label = f"{form.name} / {scene.scene_name}"
            before = setting_name(preform, scene.scene_id)
            layers_before = preform.get_scene(scene_id=scene.scene_id).layer_count
            if only_from and before != only_from:
                rows.append(Row(label, before, str(layers_before), status=SKIPPED))
                continue

            time_before = print_time(preform, scene.scene_id) if with_time else ""
            # Models, supports, and layout stay. On another printer's setting, the
            # models move into its build volume, and any that don't fit are out of
            # bounds.
            preform.update_scene(scene_id=scene.scene_id, **target)
            after = preform.get_scene(scene_id=scene.scene_id)
            outside = [model.name for model in after.models if not model.in_bounds]
            rows.append(
                Row(
                    label,
                    before,
                    f"{layers_before} -> {after.layer_count}",
                    f"{time_before} -> {print_time(preform, scene.scene_id)}" if with_time else "",
                    f"{len(outside)} model(s) outside the build volume" if outside else "changed",
                )
            )

        if out and any(row.status != SKIPPED for row in rows):
            out.mkdir(parents=True, exist_ok=True)
            saved = out / form.name
            preform.save_form_file(
                file=str(saved.resolve()),
                scene_ids=[scene.scene_id for scene in opened.scenes],
                project_name=opened.project_name or form.stem,
            )
            for row in rows:
                if row.status != SKIPPED:
                    row.status = f"saved to {saved}" if row.status == "changed" else f"{row.status}, saved to {saved}"
    finally:
        for scene in opened.scenes:
            preform.delete_scene(scene_id=scene.scene_id)
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "paths", nargs="+", type=Path,
        help="the .fps file to roll out, then .form files or folders",
    )
    parser.add_argument(
        "--shipped", nargs=4, metavar=("MACHINE", "MATERIAL", "SETTING", "THICKNESS_MM")
    )
    parser.add_argument(
        "--only-from", help="change only build volumes on this print setting name"
    )
    parser.add_argument("--out", type=Path, help="folder for the updated .form files")
    parser.add_argument(
        "--print-time", action="store_true", help="report print times before and after"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="report the change without saving"
    )
    args = parser.parse_args()

    paths = args.paths
    if args.shipped:
        machine, material, setting, thickness = args.shipped
        target = dict(
            machine_type=machine,
            material_code=material,
            print_setting=setting,
            layer_thickness_mm=float(thickness),
        )
    elif paths[0].suffix.lower() == ".fps":
        target = {"fps_file": str(paths[0].resolve())}
        paths = paths[1:]
    else:
        sys.exit("Give an .fps file or --shipped MACHINE MATERIAL SETTING THICKNESS_MM")
    if not args.out and not args.dry_run:
        sys.exit("Pass --out FOLDER for the updated jobs, or --dry-run")
    forms = [form for path in paths for form in (sorted(path.glob("*.form")) if path.is_dir() else [path])]

    with FormlabsClient() as client:
        try:
            preform = client.preform.connect(base_url=PREFORM_URL)
        except PreFormApiError as exc:
            sys.exit(
                f"{exc}\nNo PreForm at {PREFORM_URL}; "
                "open PreForm and start its API server"
            )
        try:
            print(f"rolling out: {check_target(preform, target)}")
        except PreFormApiError as exc:
            sys.exit(f"The target print setting doesn't load: {exc}")
        if args.dry_run:
            print("dry run, nothing saved")

        rows: list[Row] = []
        for form in forms:
            try:
                rows += roll_out(preform, form, target, args.only_from, None if args.dry_run else args.out, args.print_time)
            except PreFormApiError as exc:
                rows.append(Row(form.name, "", "", status=f"FAILED: {exc}"))

    # The print time column is left out unless it was asked for, to keep the table narrow.
    def line(label: str, setting: str, layers: str, time: str, status: str) -> str:
        time = f"  {time:>16}" if args.print_time else ""
        return f"{label:<16} {setting:<16} {layers:>10}{time}  {status}"

    print("\n" + line("file", "current setting", "layers", "print time", "status"))
    for row in rows:
        print(line(row.label, row.setting, row.layers, row.print_time, row.status))
    changed = sum(row.layers.count("->") for row in rows)
    print(f"\n{changed} build volume(s) changed in {len(forms)} file(s)")


if __name__ == "__main__":
    main()
