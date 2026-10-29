"""Pack the same boats with different model locks, and compare the results.

Open PreForm and start its API server on port 44388, then run:

    uv run pack_modes.py free
    uv run pack_modes.py upright

Set FL_LOCAL_BASE_URL to reach PreForm on another port or host.
"""

import argparse
import os
from pathlib import Path

from formlabs_sdk import FormlabsClient

HERE = Path(__file__).parent
FORM_FILE = HERE / "parts.form"
PREFORM_URL = os.environ.get("FL_LOCAL_BASE_URL", "http://localhost:44388")

# Each mode locks every part the same way before the pack. Every mode passes the same
# seed, so a run of a mode always gives the same build.
MODES = {
    # Packing may move and turn each part any way.
    "free": "FREE",
    # Packing may spin each part about z and turn it upside down, but never tip it
    # on its side.
    "flip": "LOCKED_XY_FLIP_ENABLED",
    # Packing may spin each part about z, but keeps it the right way up.
    "spin": "LOCKED_XY_ROTATION_FREE_TRANSLATION",
    # Packing may move each part, but never turns it.
    "upright": "LOCKED_ROTATION_FREE_TRANSLATION",
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("mode", choices=MODES)
    mode = parser.parse_args().mode
    out = HERE / f"parts.{mode}.form"

    with FormlabsClient() as client:
        preform = client.preform.connect(base_url=PREFORM_URL)
        # PreForm resolves paths from its own working directory.
        scene_id = preform.open_form_file(file=str(FORM_FILE.resolve())).scenes[0].scene_id
        try:
            # A lock belongs to each part. Without model_ids, update_models sets this
            # lock on every part, and auto_pack_models packs every part.
            preform.update_models(scene_id=scene_id, lock=MODES[mode])
            preform.auto_pack_models(scene_id=scene_id, seed=7)
            preform.save_form_file(file=str(out.resolve()), scene_ids=[scene_id])
        finally:
            preform.delete_scene(scene_id=scene_id)
    print(f"-> {out.name}")


if __name__ == "__main__":
    main()
