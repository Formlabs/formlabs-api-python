"""Lay out more parts than fit on one build platform, across as many builds as it takes.

Open PreForm and start its API server on port 44388, then run:

    uv run layout_across_builds.py

Set FL_LOCAL_BASE_URL to reach PreForm on another port or host.
"""

import os
from pathlib import Path

from formlabs_sdk import FormlabsClient, PreFormApiError

HERE = Path(__file__).parent
FORM_FILE = HERE / "arches.form"
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
                # Parts are named in the order they arrived, so the last one is the newest.
                models = sorted(preform.list_models(scene_id=scene_id).models, key=lambda m: m.name)
                taken = [m.id for m in models if m.name in placed]
                if taken:
                    preform.delete_models(scene_id=scene_id, model_ids=taken)
                models = [m for m in models if m.name not in placed]
                if not models:
                    break
                while True:
                    try:
                        # The arches all face the same way, so they lay out without turning.
                        preform.auto_layout_models(
                            scene_id=scene_id, model_ids=[m.id for m in models], lock_rotation=True, seed=42
                        )
                        break
                    except PreFormApiError as exc:
                        # OPERATION_FAILED here means the parts don't all fit together.
                        if exc.code != "OPERATION_FAILED" or len(models) == 1:
                            raise
                        # Eject the newest part, so the oldest parts print first.
                        preform.delete_models(scene_id=scene_id, model_ids=[models.pop().id])
                build += 1
                out = HERE / f"arches.build-{build}.form"
                preform.save_form_file(file=str(out.resolve()), scene_ids=[scene_id])
                placed |= {m.name for m in models}
                print(f"{out.name}: {', '.join(m.name for m in models)}")
            finally:
                preform.delete_scene(scene_id=scene_id)


if __name__ == "__main__":
    main()
