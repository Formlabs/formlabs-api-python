"""Apply a print preset to a set of models and save a print-ready .form file.

A dental lab receives scans all day. Each case is one of a few kinds, and each kind
always prints the same way: the same material and layer thickness, the same
orientation, supports or not, and an automatic layout. A preset in presets.toml holds
those choices, like the presets in PreForm's dental workspace.

Open PreForm and start its API server on port 44388, then run:

    uv run apply_preset.py --list
    uv run apply_preset.py orthodontic-models scans/case-1042_*.stl

Set FL_LOCAL_BASE_URL to reach PreForm on another port or host.
"""

import argparse
import os
import sys
import tomllib
from pathlib import Path

from formlabs_sdk import FormlabsClient, PreFormApi, PreFormApiError
from formlabs_preform_api.models import (
    AutoLayoutMode,
    AutoOrientMode,
    ImportUnits,
    RaftType,
    RepairBehavior,
    Scene,
)

PRESETS_FILE = Path(__file__).parent / "presets.toml"
PREFORM_URL = os.environ.get("FL_LOCAL_BASE_URL", "http://localhost:44388")


def load_presets(path: Path) -> dict[str, dict]:
    """Read the presets, each filled in from the [defaults] table."""
    data = tomllib.loads(path.read_text())
    defaults = data.get("defaults", {})
    return {name: defaults | preset for name, preset in data["presets"].items()}


def apply_preset(
    preform: PreFormApi, preset: dict, models: list[Path], out: Path
) -> Scene:
    """Build a scene from the preset and models, save it as a .form, and return it."""
    scene = preform.create_scene(
        machine_type=preset["machine_type"],
        material_code=preset["material_code"],
        print_setting=preset["print_setting"],
        layer_thickness_mm=preset["layer_thickness_mm"],
    )
    try:
        for model in models:
            # PreForm resolves paths from its own working directory.
            preform.import_models(
                scene_id=scene.scene_id,
                file=str(model.resolve()),
                name=model.stem,
                units=ImportUnits(preset["units"]),
                repair_behavior=RepairBehavior(preset["repair_behavior"]),
            )

        # DENTAL puts each arch occlusal side up, then tilts the occlusal plane by tilt degrees.
        preform.auto_orient_models(
            scene_id=scene.scene_id, mode=AutoOrientMode.DENTAL, tilt=preset["tilt_deg"]
        )

        if supports := preset.get("supports"):
            preform.auto_support_models(
                scene_id=scene.scene_id,
                raft_type=RaftType(supports["raft_type"]),
                raft_label_enabled=supports["raft_label_enabled"],
                density=supports["density"],
                touchpoint_size_mm=supports["touchpoint_size_mm"],
                internal_supports_enabled=supports["internal_supports_enabled"],
            )

        preform.auto_layout_models(
            scene_id=scene.scene_id,
            mode=AutoLayoutMode(preset["layout_mode"]),
            model_spacing_mm=preset["model_spacing_mm"],
        )
        preform.save_form_file(
            file=str(out.resolve()), scene_ids=[scene.scene_id], project_name=out.stem
        )
        return preform.get_scene(scene_id=scene.scene_id)
    finally:
        preform.delete_scene(scene_id=scene.scene_id)


def report(name: str, preset: dict, scene: Scene, out: Path) -> None:
    settings = scene.scene_settings
    print(
        f"{name}: {preset['material']} ({settings.material_code}) at {settings.layer_thickness_mm} mm, "
        f"tilt {preset['tilt_deg']} deg, supports {'on' if 'supports' in preset else 'off'}"
    )
    print(f"  {'model':32} {'size x*y*z mm':>18} {'supports':>9} {'fits':>5}")
    for model in scene.models:
        low, high = model.bounding_box.min_corner, model.bounding_box.max_corner
        size = f"{high.x - low.x:.1f}x{high.y - low.y:.1f}x{high.z - low.z:.1f}"
        supported = "yes" if model.has_supports else "no"
        fits = "yes" if model.in_bounds else "NO"
        print(f"  {model.name[:32]:32} {size:>18} {supported:>9} {fits:>5}")
    print(f"  {scene.layer_count} layers, {scene.material_usage.volume_ml:.1f} mL of resin")
    print(f"-> {out}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("preset", nargs="?", help="preset name from the presets file")
    parser.add_argument("models", nargs="*", type=Path, help="STL, OBJ, 3MF, or STEP files")
    parser.add_argument("--presets", type=Path, default=PRESETS_FILE, help="presets file (default: presets.toml)")
    parser.add_argument("--out", type=Path, help="output .form file (default: <preset>.form next to the first model)")
    parser.add_argument("--list", action="store_true", help="list the presets and exit")
    args = parser.parse_args()

    presets = load_presets(args.presets)
    if args.list or not args.preset:
        for name, preset in presets.items():
            supports = "supports" if "supports" in preset else "no supports"
            print(f"{name:20} {preset['material']}, {preset['layer_thickness_mm']} mm, tilt {preset['tilt_deg']}, {supports}")
        return
    if args.preset not in presets:
        sys.exit(f"Unknown preset {args.preset!r}; choose one of {', '.join(presets)}")
    if not args.models:
        sys.exit("No models given")
    out = args.out or args.models[0].parent / f"{args.preset}.form"

    with FormlabsClient() as client:
        try:
            preform = client.preform.connect(base_url=PREFORM_URL)
        except PreFormApiError as exc:
            sys.exit(
                f"{exc}\nNo PreForm at {PREFORM_URL}; open PreForm and start its API server"
            )
        scene = apply_preset(preform, presets[args.preset], args.models, out)

    report(args.preset, presets[args.preset], scene, out)


if __name__ == "__main__":
    main()
