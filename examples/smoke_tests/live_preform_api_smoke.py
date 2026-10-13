"""Manual smoke test for the PreForm API child (client.preform).

Not run in CI. Two modes:

  - FL_PREFORM_SERVER_EXE set  -> the SDK launches its own PreFormServer
  - otherwise                  -> connects to one already running at
                                  FL_LOCAL_BASE_URL (default http://localhost:44388)

Login uses FL_TEST_USER / FL_TEST_PASS (the server stays logged out when unset).

Flow: launch/connect -> create scene -> async validate-manifoldness ->
list scenes -> delete scene -> close (terminates the server only in launch mode).
"""

import os
import sys

from formlabs_sdk import FormlabsClient, PreFormApi


def acquire(client: FormlabsClient) -> PreFormApi:
    exe = os.environ.get("FL_PREFORM_SERVER_EXE")
    if exe:
        print(f"[..] launching {exe}")
        preform = client.preform.launch(exe)
        print(f"[ok] launched PreFormServer {preform.version} at {preform.base_url}")
    else:
        base_url = os.environ.get("FL_LOCAL_BASE_URL", "http://localhost:44388")
        preform = client.preform.connect(base_url=base_url, login=True)
        print(f"[ok] connected to PreFormServer {preform.version} at {preform.base_url}")
    return preform


def main() -> int:
    with FormlabsClient(
        username=os.environ.get("FL_TEST_USER"),
        password=os.environ.get("FL_TEST_PASS"),
    ) as client:
        preform = acquire(client)
        user = preform.current_user()
        print(f"[ok] logged in as {user.username}" if user else "[--] server is not logged in")

        scene = preform.create_scene(
            machine_type="FORM-4-0",
            material_code="FLGPGR05",
            layer_thickness_mm=0.1,
        )
        print(f"[ok] scene created: {scene.id}")

        report = preform.validate_manifoldness(
            scene_id=scene.id, on_progress=lambda p: print(f"     validating {p:.0%}")
        )
        print(f"[ok] async validate-manifoldness: {report}")

        scenes = preform.list_scenes()
        print(f"[ok] scene list: {len(scenes.scenes)} scene(s)")

        preform.delete_scene(scene_id=scene.id)
        print("[ok] scene deleted")

    print("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
