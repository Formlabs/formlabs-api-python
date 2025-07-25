"""
Demo application that batches all STL files in a folder into .form files.

Usage: python3 batching-minimal.py ~/Documents/folder-of-stl-files

Optional flags:
--auto-orient: Auto orient models
--dental-mode: Use dental mode when auto orienting
--auto-support: Auto support models
--username: Username for login if uploading to a remote printer or Fleet Control queue
--password: Password for login if uploading to a remote printer or Fleet Control queue
--upload-to: Upload to a specific printer, IP Address, or Fleet Control Printer Group ID
--traveler-pdf: Generates a traveler pdf
"""

import argparse
import pathlib
import csv
import sys
import tempfile
import typing
from functools import reduce
import operator

import pdf_generation

import requests
import formlabs_local_api_minimal as formlabs

MACHINE_TYPE = "FRML-4-0"
MATERIAL_CODE = "FLGPGR05"


def list_files_in_directory(directory_path: pathlib.Path) -> list[pathlib.Path]:
    return [f for f in directory_path.iterdir() if f.is_file() and f.suffix == ".stl"]


def create_scene():
    response = requests.post(
        "http://localhost:44388/scene/",
        json={
            "machine_type": MACHINE_TYPE,
            "material_code": MATERIAL_CODE,
            "layer_thickness_mm": 0.1,
            "print_setting": "DEFAULT",
        },
    )
    response.raise_for_status()
    return response.json()


def get_screenshot(settings: dict) -> typing.BinaryIO:
    """
    Calls the /scene/save-screenshot endpoint with the given settings and returns a temp file handle to the screenshot.
    :param settings: Settings to send to the /scene/save-screenshot endpoint
    :return: A temp file handle to the saved screenshot.
    """
    temp = tempfile.NamedTemporaryFile("rb", suffix=".png")
    screenshot_response = requests.post(
        "http://localhost:44388/scene/save-screenshot/",
        json={"file": temp.name, "image_size_px": 125} | settings,
    )
    if not screenshot_response.ok:
        print(screenshot_response.json())
    screenshot_response.raise_for_status()
    return temp


parser = argparse.ArgumentParser(description="Process a folder path.")
parser.add_argument("folder", type=str, help="Path to the folder")
parser.add_argument("--auto-orient", action="store_true", help="Auto orient models")
parser.add_argument(
    "--dental-mode", action="store_true", help="Use dental mode when auto orienting"
)
parser.add_argument("--auto-support", action="store_true", help="Auto support models")
parser.add_argument("--username", type=str, help="Username for login")
parser.add_argument("--password", type=str, help="Password for login")
parser.add_argument(
    "--upload-to",
    type=str,
    help="Upload to a specific printer, IP Address, or Fleet Control Printer Group ID",
)
parser.add_argument(
    "--traveler-pdf", action="store_true", help="Generates a traveler pdf"
)
parser.add_argument(
    "--ps-path", type=str, help="Path to directory containing PreFormServer"
)
args = parser.parse_args()

directory_path = pathlib.Path(args.folder).resolve(strict=True)
files_to_batch = list_files_in_directory(directory_path)
print("Files to batch:")
print(list(map(str, files_to_batch)))
current_batch = 1
models_in_current_batch = []
model_pdf_data = []
CSV_RESULT_FILENAME = directory_path / "summary.csv"

pathToPreformServer = None
ps_containing_dir = pathlib.Path(args.ps_path) if args.ps_path else pathlib.Path()
if sys.platform == "win32":
    pathToPreformServer = (
        ps_containing_dir.resolve() / "PreFormServer/PreFormServer.exe"
    )
elif sys.platform == "darwin":
    pathToPreformServer = (
        ps_containing_dir.resolve() / "PreFormServer.app/Contents/MacOS/PreFormServer"
    )
else:
    print("Unsupported platform")
    sys.exit(1)

with formlabs.PreFormApi.start_preform_server(pathToPreformServer=pathToPreformServer):
    material_response = requests.get("http://localhost:44388/list-materials")
    material_response.raise_for_status()
    material_response_json = material_response.json()
    printer_types = list(
        filter(
            lambda printer_type: MACHINE_TYPE
            in printer_type["supported_machine_type_ids"],
            material_response_json["printer_types"],
        )
    )
    MACHINE_NAME: str = printer_types[0]["label"]
    materials = dict(
        map(
            lambda material: (
                material["material_settings"][0]["scene_settings"]["material_code"],
                material["label"],
            ),
            reduce(
                operator.iconcat,
                map(lambda printer_type: printer_type["materials"], printer_types),
                [],
            ),
        )
    )

    MATERIAL_NAME = materials[MATERIAL_CODE]

    if args.username and args.password:
        login_response = requests.post(
            "http://localhost:44388/login/",
            json={
                "username": args.username,
                "password": args.password,
            },
        )
        login_response.raise_for_status()

    with open(CSV_RESULT_FILENAME, "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(
            ["Batch Number", "Batch Print Filename", "Model Source Filename"]
        )

        def save_batch_form():
            global current_batch, models_in_current_batch, model_pdf_data
            form_file_name = f"batch_{current_batch}.form"
            save_path = directory_path / form_file_name
            save_form_response = requests.post(
                "http://localhost:44388/scene/save-form/",
                json={
                    "file": str(save_path),
                },
            )
            save_form_response.raise_for_status()
            print(f"Saving batch {current_batch} to {save_path}")
            for i, model in enumerate(models_in_current_batch):
                print(f"{i + 1}. {model['file_name']}")
                csvwriter.writerow([current_batch, form_file_name, model["file_name"]])
            if args.traveler_pdf:
                pdf = pdf_generation.TravelerPDF(
                    directory_path / f"summary-batch-{current_batch}.pdf",
                )

                build_volume_image = get_screenshot({})

                get_scene_response = requests.get("http://localhost:44388/scene")
                get_scene_response.raise_for_status()
                get_scene_response_json = get_scene_response.json()
                print_setting = get_scene_response_json["scene_settings"][
                    "print_setting"
                ]
                layer_thickness_mm = get_scene_response_json["scene_settings"][
                    "layer_thickness_mm"
                ]

                pdf.add_header(
                    form_file_name,
                    MACHINE_NAME,
                    MATERIAL_NAME,
                    print_setting,
                    layer_thickness_mm,
                    build_volume_image,
                )
                pdf.add_parts(model_pdf_data)
                pdf.save()
                model_pdf_data = []
            current_batch += 1
            models_in_current_batch = []
            if args.upload_to:
                print(f"Uploading batch to {args.upload_to}")
                print_response = requests.post(
                    "http://localhost:44388/scene/print/",
                    json={
                        "printer": args.upload_to,
                        "job_name": form_file_name,
                    },
                )
                print_response.raise_for_status()

        create_scene()
        while len(files_to_batch) > 0:
            next_file = files_to_batch.pop()
            print(f"Importing {next_file}")
            import_model_response = requests.post(
                "http://localhost:44388/scene/import-model/",
                json={"file": str(directory_path / next_file)},
            )
            if not import_model_response.ok:
                continue
            import_model_response.raise_for_status()
            new_model_id = import_model_response.json()["id"]
            models_in_current_batch.append(
                {"model_id": new_model_id, "file_name": next_file}
            )
            if args.auto_orient:
                print(f"Auto orienting {new_model_id}")
                auto_orient_params = {"models": [new_model_id]}
                if args.dental_mode:
                    auto_orient_params["mode"] = "DENTAL"
                    auto_orient_params["tilt"] = 0
                auto_orient_response = requests.post(
                    "http://localhost:44388/scene/auto-orient/",
                    json=auto_orient_params,
                )
                auto_orient_response.raise_for_status()
            if args.traveler_pdf:
                image = get_screenshot({"models": [new_model_id]})
                import_model_response_json = import_model_response.json()
                model_dimensions = tuple(
                    map(
                        lambda dim: float(
                            import_model_response_json["bounding_box"]["max_corner"][
                                dim
                            ]
                        )
                        - float(
                            import_model_response_json["bounding_box"]["min_corner"][
                                dim
                            ]
                        ),
                        ["x", "y", "z"],
                    )
                )
                model_pdf_data.append(
                    pdf_generation.Model(next_file, image, model_dimensions)
                )
            if args.auto_support:
                print(f"Auto supporting {new_model_id}")
                auto_support_response = requests.post(
                    "http://localhost:44388/scene/auto-support/",
                    json={
                        "models": [new_model_id],
                    },
                )
                auto_support_response.raise_for_status()
            print(f"Auto layouting all")
            layout_response = requests.post(
                "http://localhost:44388/scene/auto-layout/",
                json={
                    "models": "ALL",
                },
            )
            if layout_response.status_code != 200:
                print("Not all models can fit, removing model")
                model_data = models_in_current_batch.pop()
                model_pdf_data.pop()
                delete_response = requests.delete(
                    f"http://localhost:44388/scene/models/{model_data['model_id']}/",
                )
                delete_response.raise_for_status()
                files_to_batch.append(model_data["file_name"])
                save_batch_form()
                print("Clearing scene")
                create_scene()

        if len(models_in_current_batch) > 0:
            save_batch_form()
