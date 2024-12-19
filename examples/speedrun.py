"""
Generate variations of print settings from a given .form file to optimize for speed, with a possible tradeoff of print quality or print success.

## Limitations:
- Only works for Form 4 and Form 4L printers. Supporting other printer types is possible but would require additional development.
- Only supports .form files saved using PreForm 3.42 or later.
- Changing wiping behavior may not change the estimated print time, although it would decrease actual print times

## Example Usage:
1. Prepare your print like normal using PreForm 3.42 or newer. Save the prepared print as a .form file.
2. Run speedrun.py with the path to the .form file and your desired speedup options. Run `python3 examples/speedrun.py --help` to see available options.

python3 examples/speedrun.py test.form --reduce_wiping --reduce_exposure

3. The script will generate variations and output:
- A report.md file with a summary of the results
- A .fps Print Setting file for each variation that can be imported into PreForm
- A .form file for each variation using the optimized print settings

4. If you are loading the generated .form file variations into PreForm,
   you must first import the variation's matching .fps file into PreForm's Print Settings Editor before loading .form file.
   
   Importing the variation .form file without first loading the matching .fps file will not apply the correct print settings
   and will give the error "FORM File Warning: The Print Settings saved in this .form file is no longer available.
   The selected material has been updated to the last used material."
"""

import formlabs_local_api_minimal as formlabs
import requests
import argparse
import json
import os
import sys
import copy
import difflib
import pathlib
import itertools
import uuid


server_path = None
if sys.platform == "win32":
    server_path = pathlib.Path().resolve() / "PreFormServer/PreFormServer.exe"
elif sys.platform == "darwin":
    server_path = (
        pathlib.Path().resolve()/ "PreFormServer.app/Contents/MacOS/PreFormServer"
    )
else:
    print("Unsupported platform")
    sys.exit(1)


def main():
    args = parse_args()

    report_data = []
    with formlabs.PreFormApi.start_preform_server(pathToPreformServer=server_path):
        # Load the base .form file and get the estimated print time
        requests.request(
            "POST",
            "http://localhost:44388/load-form/",
            json={
                "file": args.form_file,
            },
        ).raise_for_status()
        estimate_print_time_response = requests.request(
            "POST",
            f"http://localhost:44388/scene/estimate-print-time/",
        )
        estimate_print_time_response.raise_for_status()
        base_estimated_print_time_s = estimate_print_time_response.json()[
            "total_print_time_s"
        ]

        base_settings_path = None
        if args.settings_file:
            base_settings_path = args.settings_file
        else:
            print("Exacting initial settings from form file")
            base_settings_path = os.path.abspath("base_settings.fps")
            requests.request(
                "POST",
                "http://localhost:44388/scene/save-fps-file/",
                json={
                    "file": base_settings_path,
                },
            ).raise_for_status()

        print("Loading initial settings file")
        with open(base_settings_path, "r") as f:
            base_settings = json.load(f)

        print("\nGenerating variations...")
        variations = generate_variations(base_settings, args)
        print(f"Generated {len(variations)} variations")

        for idx, variation in enumerate(variations):
            print(f"\nAnalyzing variation {idx+1}/{len(variations)}: {variation.name}")

            form_file_parent_folder = os.path.dirname(args.form_file)
            settings_file = os.path.join(form_file_parent_folder, f"settings_{variation.name}.fps")
            with open(settings_file, "w") as f:
                json.dump(variation.settings, f, indent=4)
            print(f"saved {os.path.basename(settings_file)}")

            requests.request(
                "PUT",
                "http://localhost:44388/scene/",
                json={
                    "fps_file": os.path.abspath(settings_file),
                },
            ).raise_for_status()
            estimate_print_time_response = requests.request(
                "POST",
                f"http://localhost:44388/scene/estimate-print-time/",
            )
            estimate_print_time_response.raise_for_status()
            estimated_print_time_s = estimate_print_time_response.json()[
                "total_print_time_s"
            ]
            base_form_file_name_without_extension = os.path.splitext(args.form_file)[0]
            job_name = f"{base_form_file_name_without_extension}{variation.name}"
            variation_form_file_name = f"{job_name}.form"
            requests.request(
                "POST",
                "http://localhost:44388/scene/save-form/",
                json={
                    "file": os.path.abspath(variation_form_file_name),
                },
            ).raise_for_status()
            print(f"saved {os.path.basename(variation_form_file_name)}")

            if args.printers:
                printer_id = args.printers[idx % len(args.printers)]
                print(
                    f"Slicing and uploading job {job_name} to printer {printer_id}..."
                )
                requests.request(
                    "POST",
                    "http://localhost:44388/scene/print/",
                    json={
                        "printer": printer_id,
                        "job_name": job_name,
                    },
                ).raise_for_status()
                print(f"Job upload complete")

            # Record report data
            print_time_decrease_percentage = (
                100
                * (base_estimated_print_time_s - estimated_print_time_s)
                / base_estimated_print_time_s
            )
            report_data.append(
                {
                    "variation_name": variation.name,
                    "estimated_print_time_s": estimated_print_time_s,
                    "print_time_decrease_percentage": print_time_decrease_percentage,
                    "settings_file": settings_file,
                    "form_file": variation_form_file_name,
                    "diffs": get_settings_diff(base_settings, variation.settings),
                }
            )
            print(f"Result: {print_time_decrease_percentage:.1f}% print time decrease")

        generate_report(report_data, args.report_file)
        # Optional addition: Run pandoc to convert markdown to pdf
        # os.system(f"pandoc -s -V geometry:margin=1in {args.report_file} -o {args.report_file.replace('.md', '.pdf')}")
        print(f"\nDone. Result summary written to {args.report_file}")


def parse_args():
    parser = argparse.ArgumentParser(description="3D Print Job Speed Optimization Tool")
    parser.add_argument("form_file", help="Path to starting .form file")

    parser.add_argument(
        "--settings_file",
        action="store_true",
        help="Path to starting .fps settings file",
    )
    parser.add_argument(
        "--reduce_wiping", action="store_true", help="Apply reduced wiping optimization"
    )
    parser.add_argument(
        "--reduce_exposure",
        action="store_true",
        help="Apply reduced exposure optimization",
    )
    parser.add_argument(
        "--increase_layer_height",
        action="store_true",
        help="Apply increased layer height optimization",
    )

    parser.add_argument(
        "--printers", nargs="*", help="List of printer serial names to send jobs to"
    )
    parser.add_argument("--report_file", default="report.md", help="Output report file")

    args = parser.parse_args()
    return args


class VariationOption:
    def __init__(self, name, func):
        self.name = name
        self.func = func


class Variation:
    def __init__(self, name, settings):
        self.name = name
        self.settings = settings


def generate_variations(base_settings, args) -> list[Variation]:
    form4_reduce_wipe_options = [
        VariationOption(
            "one_way_wipe", lambda settings: form4_reduce_wiping(settings, -1)
        ),
        VariationOption(
            "disable_wiping", lambda settings: form4_reduce_wiping(settings, 0)
        ),
    ]
    reduce_expose_options = [
        VariationOption(
            "reduce_exposure_10", lambda settings: form4_reduce_exposure(settings, 0.1)
        ),
        VariationOption(
            "reduce_exposure_20", lambda settings: form4_reduce_exposure(settings, 0.2)
        ),
        VariationOption(
            "reduce_exposure_30", lambda settings: form4_reduce_exposure(settings, 0.3)
        ),
    ]
    increase_layer_height_options = [
        VariationOption(
            "increase_layer_height_0.11",
            lambda settings: increase_layer_height(settings, 0.11),
        ),
        VariationOption(
            "increase_layer_height_0.12",
            lambda settings: increase_layer_height(settings, 0.12),
        ),
        VariationOption(
            "increase_layer_height_0.13",
            lambda settings: increase_layer_height(settings, 0.13),
        ),
        VariationOption(
            "increase_layer_height_0.14",
            lambda settings: increase_layer_height(settings, 0.14),
        ),
        VariationOption(
            "increase_layer_height_0.15",
            lambda settings: increase_layer_height(settings, 0.15),
        ),
        VariationOption(
            "increase_layer_height_0.16",
            lambda settings: increase_layer_height(settings, 0.16),
        ),
        VariationOption(
            "increase_layer_height_0.17",
            lambda settings: increase_layer_height(settings, 0.17),
        ),
    ]

    is_form4_family = (
        base_settings["public_fields"]["categories"][
            get_printer_knobs_index(base_settings)
        ]["key"]
        == "Material_Form_4_Family_Print"
    )
    if not is_form4_family:
        print("Only Form 4/4L supported")
        raise Exception("Unsupported printer type. Only Form 4 and Form 4L printer types are currently supported.")

    options = []
    if args.reduce_wiping:
        options.append(form4_reduce_wipe_options)
    if args.reduce_exposure:
        options.append(reduce_expose_options)
    if args.increase_layer_height:
        options.append(increase_layer_height_options)

    if len(options) == 0:
        print("No options selected")
        return []

    combinations = list(itertools.product(*options))
    variations = []
    for combo in combinations:
        settings = copy.deepcopy(base_settings)
        combined_name = ""
        for variation_option in combo:
            settings = variation_option.func(settings)
            combined_name += f"_{variation_option.name}"
        settings = update_settings_with_new_id_and_name(settings, combined_name)
        variation_number = len(variations) + 1
        combined_name = f"v{variation_number}{combined_name}"
        variations.append(Variation(combined_name, settings))
    return variations


def update_settings_with_new_id_and_name(settings, combined_name):
    settings["metadata"]["id"] = "{" + str(uuid.uuid4()) + "}"
    settings["metadata"]["name"] = settings["metadata"]["name"] + combined_name
    return settings


def get_printer_knobs_index(settings):
    printerTypeCategoryIndex = -1
    for i, category in enumerate(settings["public_fields"]["categories"]):
        if category["key"] == "Material_Form_4_Family_Print":
            printerTypeCategoryIndex = i
            break
    if printerTypeCategoryIndex == -1:
        raise Exception("supported printer type category not found")
    return printerTypeCategoryIndex


def get_printer_knobs(settings):
    printerTypeCategoryIndex = get_printer_knobs_index(settings)
    return settings["public_fields"]["categories"][printerTypeCategoryIndex]["values"]


def get_settings_with_new_printer_knobs(settings, knobs):
    printerTypeCategoryIndex = get_printer_knobs_index(settings)
    settings["public_fields"]["categories"][printerTypeCategoryIndex]["values"] = knobs
    return settings


def form4_reduce_wiping(settings, wipe_behavior_mode_value):
    knobs = get_printer_knobs(settings)
    if "wipe_behavior_pattern" not in knobs:
        raise Exception("wipe_behavior_pattern not found in settings")
    knobs["wipe_behavior_pattern"] = [{"wipe_behavior": wipe_behavior_mode_value}]
    return get_settings_with_new_printer_knobs(settings, knobs)


def form4_reduce_exposure(settings, percent_decrease):
    knobs = get_printer_knobs(settings)

    knobs["model_fill_exposure_mJpcm2"] = round(
        knobs["model_fill_exposure_mJpcm2"] * (1 - percent_decrease), 1
    )
    for i, v in enumerate(knobs["overhang_fill_exposures"]):
        knobs["overhang_fill_exposures"][i]["exposure_mJpcm2"] = round(
            v["exposure_mJpcm2"] * (1 - percent_decrease), 1
        )
    knobs["perimeter_fill_exposure_mJpcm2"] = knobs["model_fill_exposure_mJpcm2"]
    knobs["supports_fill_exposure_mJpcm2"] = knobs["model_fill_exposure_mJpcm2"]
    knobs["top_surface_exposure_mJpcm2"] = knobs["model_fill_exposure_mJpcm2"]
    if "irradiance_mWpcm2" not in knobs:
        raise Exception("irradiance_mWpcm2 not found in settings")
    knobs["irradiance_mWpcm2"] = 16
    if "post_expose_cure_wait_s" not in knobs:
        raise Exception("post_expose_cure_wait_s not found in settings")
    knobs["post_expose_cure_wait_s"] = 0
    return get_settings_with_new_printer_knobs(settings, knobs)


def increase_layer_height(settings, layer_thickness_mm):
    coreSceneIndex = -1
    for i, category in enumerate(settings["public_fields"]["categories"]):
        if category["key"] == "Core_Scene":
            coreSceneIndex = i
            break
    if coreSceneIndex == -1:
        raise Exception("Core_Scene category not found")

    knobs = settings["public_fields"]["categories"][coreSceneIndex]["values"]
    knobs["layer_thickness"]["layer_thickness_mm"] = layer_thickness_mm
    settings["public_fields"]["categories"][coreSceneIndex]["values"] = knobs
    return settings


def get_settings_diff(base_settings, new_settings):
    base_str = json.dumps(base_settings, sort_keys=True, indent=4)
    new_str = json.dumps(new_settings, sort_keys=True, indent=4)
    diff = difflib.unified_diff(
        base_str.splitlines(), new_str.splitlines(), lineterm=""
    )
    return "\n".join(diff)


def generate_report(report_data, report_file):
    with open(report_file, "w") as f:
        f.write("# speedrun.py Results\n")
        f.write("\n")
        f.write("## Summary\n")
        for data in report_data:
            f.write(
                f"### {data['variation_name']}: {data['print_time_decrease_percentage']:.1f}% print time decrease\n"
            )
            f.write(
                f"- Estimated Print Time: {data['estimated_print_time_s']:.1f} seconds\n"
            )
            f.write(f"- Settings File: {data['settings_file']}\n")
            f.write(f"- .form File: {os.path.basename(data['form_file'])}\n")
            f.write("\n")
        f.write("## Expanded Results\n")
        for data in report_data:
            f.write(
                f"## {data['variation_name']} [{data['print_time_decrease_percentage']:.1f}% print time decrease]\n"
            )
            f.write(
                f"- Estimated Print Time: {data['estimated_print_time_s']:.1f} seconds\n"
            )
            f.write(f"- Settings File: {data['settings_file']}\n")
            f.write(f"- .form File: {os.path.basename(data['form_file'])}\n")
            f.write("- Settings Differences:\n")
            f.write("```\n")
            f.write(f"{data['diffs']}\n")
            f.write("```\n")
            f.write("\n")


if __name__ == "__main__":
    main()
