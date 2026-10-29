"""Pack more parts than fit in one SLS build volume, across as many builds as it takes.

Open PreForm and start its API server on port 44388, then run:

    uv run pack_across_builds.py

Set FL_LOCAL_BASE_URL to reach PreForm on another port or host.
"""

import os
import sys
from pathlib import Path

from formlabs_sdk import FormlabsClient
from formlabs_preform_api.models import OnPackFailure

HERE = Path(__file__).parent
FORM_FILE = HERE / "parts.form"
PREFORM_URL = os.environ.get("FL_LOCAL_BASE_URL", "http://localhost:44388")


def main() -> None:
    placed: set[str] = set()
    with FormlabsClient() as client:
        preform = client.preform.connect(base_url=PREFORM_URL)
        build = 0
        while True:
            # Each build starts from every part, less the ones earlier builds took.
            # PreForm resolves paths from its own working directory.
            scene_id = preform.open_form_file(file=str(FORM_FILE.resolve())).scenes[0].scene_id
            try:
                models = preform.list_models(scene_id=scene_id).models
                taken = [m.id for m in models if m.name in placed]
                if taken:
                    preform.delete_models(scene_id=scene_id, model_ids=taken)
                names = {str(m.id): m.name for m in models if m.name not in placed}
                if not names:
                    break
                # PARK_OUTSIDE_BUILD_VOLUME packs what fits and moves the rest outside the
                # build volume, for the next build.
                packed = preform.auto_pack_models(
                    scene_id=scene_id, seed=7, on_pack_failure=OnPackFailure.PARK_OUTSIDE_BUILD_VOLUME
                )
                if not packed.packed_model_ids:
                    sys.exit(f"None of these fit in an empty build: {', '.join(sorted(names.values()))}")
                if packed.unpacked_model_ids:
                    preform.delete_models(scene_id=scene_id, model_ids=packed.unpacked_model_ids)
                build += 1
                out = HERE / f"parts.build-{build}.form"
                preform.save_form_file(file=str(out.resolve()), scene_ids=[scene_id])
                placed |= {names[str(i)] for i in packed.packed_model_ids}
                print(f"{out.name}: {len(packed.packed_model_ids)} parts, {len(packed.unpacked_model_ids)} left over")
            finally:
                preform.delete_scene(scene_id=scene_id)


if __name__ == "__main__":
    main()
