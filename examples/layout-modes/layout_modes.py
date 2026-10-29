"""Lay out the same parts with different auto-layout options, and compare the results.

Open PreForm and start its API server on port 44388, then run:

    uv run layout_modes.py default
    uv run layout_modes.py production

Set FL_LOCAL_BASE_URL to reach PreForm on another port or host.
"""

import argparse
import os
from pathlib import Path
from typing import Any

from formlabs_sdk import FormlabsClient
from formlabs_preform_api.models import LayoutBounds

HERE = Path(__file__).parent
FORM_FILE = HERE / "cubes.form"
PREFORM_URL = os.environ.get("FL_LOCAL_BASE_URL", "http://localhost:44388")

# Each mode sets some of auto_layout_models' options. Every mode passes the same seed, so
# a run of a mode always gives the same layout.
MODES: dict[str, dict[str, Any]] = {
    # PreForm's defaults: 1 mm apart, anywhere on the build platform, turned as it likes.
    "default": {},
    "spaced": {"model_spacing_mm": 5.0},
    # Move each part without turning it.
    "locked": {"lock_rotation": True},
    # An 80 mm square in the middle of the build platform.
    "bounded": {
        "custom_bounds": LayoutBounds(x_min_mm=-40, x_max_mm=40, y_min_mm=-40, y_max_mm=40),
    },
    # Every option a production line sets, with more attempts and iterations than the
    # defaults for a seeded layout, 200 and 25000.
    "production": {
        "model_spacing_mm": 1.0,
        "lock_rotation": True,
        "custom_bounds": LayoutBounds(x_min_mm=-90, x_max_mm=90, y_min_mm=-55, y_max_mm=55),
        "layout_attempts": 500,
        "iterations_per_attempt": 50000,
    },
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("mode", choices=MODES)
    mode = parser.parse_args().mode
    out = HERE / f"cubes.{mode}.form"

    with FormlabsClient() as client:
        preform = client.preform.connect(base_url=PREFORM_URL)
        # PreForm resolves paths from its own working directory.
        scene_id = preform.open_form_file(file=str(FORM_FILE.resolve())).scenes[0].scene_id
        try:
            preform.auto_layout_models(scene_id=scene_id, seed=42, **MODES[mode])
            preform.save_form_file(file=str(out.resolve()), scene_ids=[scene_id])
        finally:
            preform.delete_scene(scene_id=scene_id)
    print(f"-> {out.name}")


if __name__ == "__main__":
    main()
