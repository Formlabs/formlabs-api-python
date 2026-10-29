"""Prepare an STL file for a Form 4, then queue it on a printer or save it as a .form file.

Before you run it, open PreForm, click File > Start PreForm Server, and start the server
on port 44388.

Usage:  py -3 quickstart.py part.stl

Environment:
  FORMLABS_PRINTER   printer serial name (optional)
"""

import os
import sys
from pathlib import Path

from formlabs_sdk import FormlabsClient, PreFormApiError


def main() -> None:
    # PreForm resolves a relative path against its own working directory.
    PART = str(Path(sys.argv[1]).resolve())
    # Without a printer, the script saves a .form file.
    PRINTER = os.environ.get("FORMLABS_PRINTER")

    with FormlabsClient() as client:
        # connect() attaches to the PreForm window on port 44388, and each call shows
        # up in it. Leaving this with block leaves PreForm open.
        with client.preform.connect() as preform:
            # FORM-4-0 is the Form 4, and FLGPGR05 is Grey V5.
            scene = preform.create_scene(
                machine_type="FORM-4-0",
                material_code="FLGPGR05",
                layer_thickness_mm=0.1,
            )

            # One file can produce several models, so the result holds a list of their ids.
            imported = preform.import_models(scene_id=scene.scene_id, file=PART)
            first = imported.new_models[0]
            print(f"Imported {len(imported.new_models)} model(s): {first.model_id}")

            # Without model_ids, each call applies to every model in the scene.
            preform.auto_orient_models(scene_id=scene.scene_id)
            preform.auto_support_models(scene_id=scene.scene_id)
            preform.auto_layout_models(scene_id=scene.scene_id)

            # A mesh that isn't a closed solid reports is_manifold as False.
            report = preform.validate_manifoldness(scene_id=scene.scene_id)
            for model_id, result in report.per_model_results.additional_properties.items():
                if not result.is_manifold:
                    print(f"Model {model_id} is not manifold: {result.status}")

            # The faster estimate_print_time raises ESTIMATION_NOT_SUPPORTED on a Form 4.
            times = preform.calculate_print_time(scene_id=scene.scene_id)
            print(f"Print time: {times.total_print_time_s / 3600:.1f} h")

            if PRINTER:
                try:
                    # printer takes a serial name, an IP address, or a Fleet Control
                    # queue ID. print_now=False puts the print job in the queue without
                    # starting it.
                    job = preform.print_scene(
                        scene_id=scene.scene_id,
                        printer=PRINTER,
                        job_name="quickstart",
                        print_now=False,
                        on_progress=lambda p: print(f"Uploading {p:.0%}"),
                    )
                    print(f"Queued job {job.job_id} on {PRINTER}")
                except PreFormApiError as exc:
                    print(f"Could not send to {PRINTER}: {exc.code}: {exc.message}")
            else:
                # A .form file holds the scene, and it opens in PreForm.
                preform.save_form_file(
                    file=str(Path("quickstart.form").resolve()),
                    scene_ids=[scene.scene_id],
                )
                print("Saved quickstart.form")


if __name__ == "__main__":
    main()
