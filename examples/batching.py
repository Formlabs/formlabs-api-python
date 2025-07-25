"""
Demo application that batches all STL files in a folder into .form files.

Usage: python3 batching.py ~/Documents/folder-of-stl-files

Optional flags:
--auto-orient: Auto orient models
--dental-mode: Use dental mode when auto orienting
--auto-support: Auto support models
--username: Username for login if uploading to a remote printer or Fleet Control queue
--password: Password for login if uploading to a remote printer or Fleet Control queue
--upload-to: Upload to a specific printer, IP Address, or Fleet Control Printer Group ID
"""

import argparse
import os
import pathlib
import csv
import sys
import formlabs_local_api as formlabs
from formlabs_local_api import (
    AutoSupportRequest,
    AutoOrientRequest,
    AutoLayoutRequest,
    SceneTypeModel,
    Manual,
    ManualLayerThicknessMm,
    ModelsSelectionModel,
    LoadFormFileRequest,
    LoginRequest,
    UsernameAndPassword,
    PrintRequest,
    Default,
    DentalMode,
)


def list_files_in_directory(directory_path):
    return [
        f
        for f in os.listdir(directory_path)
        if os.path.isfile(os.path.join(directory_path, f)) and f.endswith(".stl")
    ]

def create_scene(preform):
    return preform.api.create_default_scene(SceneTypeModel(Manual(
        machine_type="FORM-4-0",
        material_code="FLGPGR05",
        layer_thickness_mm=ManualLayerThicknessMm("0.1"),
        print_setting="DEFAULT",
    )))

parser = argparse.ArgumentParser(description="Process a folder path.")
parser.add_argument("folder", type=str, help="Path to the folder")
parser.add_argument("--auto-orient", action="store_true", help="Auto orient models")
parser.add_argument("--dental-mode", action="store_true", help="Use dental mode when auto orienting")
parser.add_argument("--auto-support", action="store_true", help="Auto support models")
parser.add_argument("--username", type=str, help="Username for login")
parser.add_argument("--password", type=str, help="Password for login")
parser.add_argument("--upload-to", type=str, help="Upload to a specific printer, IP Address, or Fleet Control Printer Group ID")
args = parser.parse_args()

directory_path = os.path.abspath(args.folder)
files_to_batch = list_files_in_directory(directory_path)
print("Files to batch:")
print(files_to_batch)
current_batch = 1
models_in_current_batch = []
CSV_RESULT_FILENAME = os.path.join(directory_path, "summary.csv")

pathToPreformServer = None
if sys.platform == 'win32':
    pathToPreformServer = pathlib.Path().resolve() / "PreFormServer/PreFormServer.exe"
elif sys.platform == 'darwin':
    pathToPreformServer = pathlib.Path().resolve() / "PreFormServer.app/Contents/MacOS/PreFormServer"
else:
    print("Unsupported platform")
    sys.exit(1)

with formlabs.PreFormApi.start_preform_server(pathToPreformServer=pathToPreformServer) as preform:
    if args.username and args.password:
        preform.api.login(LoginRequest(UsernameAndPassword(username=args.username, password=args.password)))

    with open(CSV_RESULT_FILENAME, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Batch Number", "Batch Print Filename", "Model Source Filename"])

        def save_batch_form():
            global current_batch, models_in_current_batch
            form_file_name = f"batch_{current_batch}.form"
            save_path = os.path.join(directory_path, form_file_name)
            preform.api.save_form_file("default", LoadFormFileRequest(file=save_path))
            print(f"Saving batch {current_batch} to {save_path}")
            for i, model in enumerate(models_in_current_batch):
                print(f"{i+1}. {model['file_name']}")
                csvwriter.writerow([current_batch, form_file_name, model['file_name']])
            current_batch += 1
            models_in_current_batch = []
            if args.upload_to:
                print(f"Uploading batch to {args.upload_to}")
                preform.api.call_print(PrintRequest(printer=args.upload_to, job_name=form_file_name))

        create_scene(preform)
        while len(files_to_batch) > 0:
            next_file = files_to_batch.pop()
            print(f"Importing {next_file}")
            new_model = preform.api.import_model("default", {"file": os.path.join(directory_path, next_file)})
            new_model_id = new_model.id
            models_in_current_batch.append({"model_id": new_model_id, "file_name": next_file})
            if args.auto_orient:
                print(f"Auto orienting {new_model_id}")
                if args.dental_mode:
                    preform.api.auto_orient(AutoOrientRequest(DentalMode(models=ModelsSelectionModel([new_model_id]), mode="DENTAL", tilt=0)))
                else:
                    preform.api.auto_orient(AutoOrientRequest(Default(models=ModelsSelectionModel([new_model_id]))))
            if args.auto_support:
                print(f"Auto supporting {new_model_id}")
                preform.api.auto_support(AutoSupportRequest(models=ModelsSelectionModel([new_model_id])))
            print(f"Auto layouting all")
            try:
                preform.api.auto_layout_with_http_info(
                    "default",
                    AutoLayoutRequest(models=ModelsSelectionModel("ALL"))
                )
            except formlabs.exceptions.ApiException as e:
                print("Not all models can fit, removing model")
                model_data = models_in_current_batch.pop()
                preform.api.delete_model(str(model_data["model_id"]), "default")
                files_to_batch.append(model_data["file_name"])
                save_batch_form()
                print("Clearing scene")
                create_scene(preform)

        if len(models_in_current_batch) > 0:
            save_batch_form()
