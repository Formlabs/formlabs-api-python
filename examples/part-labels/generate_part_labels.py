"""Write a build report for a .form file: a billing summary, then one bag label per part.

A service bureau packs parts from several customer orders into one build. After the
print, sorters bag the parts by order and billing charges each order for the material
its parts used. The report carries both: every part with its order, quantity, and
material, and a label for each bag with a rendered picture of the part.

Edit the settings below, open PreForm and start its API server on port 44388, then run:

    uv run generate_part_labels.py

Set FL_LOCAL_BASE_URL to reach PreForm on another port or host.
"""

import csv
import datetime
import os
import sys
import tempfile
from collections import defaultdict
from pathlib import Path

from formlabs_sdk import FormlabsClient, PreFormApi, PreFormApiError
from formlabs_preform_api.models import RenderViewType

from label_pdf_builder import Build, Label, render_pdf

FORM_FILE = Path(__file__).parent / "model_octopus.form"
ORDERS_FILE = Path(__file__).parent / "orders.csv"
OUTPUT_PATH = FORM_FILE.with_suffix(".report.pdf")
DATE = datetime.date.today().isoformat()
PREFORM_URL = os.environ.get("FL_LOCAL_BASE_URL", "http://localhost:44388")
UNASSIGNED = ("UNASSIGNED", "No order found for this part")


def read_orders(path: Path) -> dict[str, tuple[str, str]]:
    """Map each part name to its (order, customer), from the order system's export."""
    with path.open(newline="") as f:
        rows = csv.DictReader(f)
        return {row["part"]: (row["order"], row["customer"]) for row in rows}


def fetch_builds(
    preform: PreFormApi,
    form_file: Path,
    orders: dict[str, tuple[str, str]],
    images: Path,
) -> list[Build]:
    """Open the .form file and return its builds, with a Label per distinct part."""
    opened = preform.open_form_file(file=str(form_file.resolve()))
    builds: list[Build] = []
    try:
        for scene in opened.scenes:
            metadata = preform.get_scene_metadata(scene_id=scene.scene_id)

            # Copies of a part share a display name and a mesh hash, so grouping on that
            # pair gives one entry per distinct part, holding the metadata of every copy.
            parts: dict[tuple[str, str], list[dict]] = defaultdict(list)
            for model in metadata["Models"]:
                parts[(model["DisplayName"], model["RawMeshHash"])].append(model)

            labels: list[Label] = []
            for (name, _mesh), copies in parts.items():
                image = images / f"{len(builds):02d}-{len(labels):03d}.png"
                preform.render_scene(
                    scene_id=scene.scene_id,
                    file=str(image),
                    # The copies are identical, so any one will do
                    model_ids=[copies[0]["Guid"].strip("{}")],
                    view_type=RenderViewType.ZOOM_ON_MODELS,
                    crop_to_models=True,
                    image_size_px=600,
                )
                order, customer = orders.get(name, UNASSIGNED)
                labels.append(
                    Label(
                        order=order,
                        customer=customer,
                        part=name,
                        quantity=len(copies),
                        # Volume_mL is the model plus its own supports and share of the raft, so
                        # the parts' totals add up to the material the whole build uses.
                        model_ml=sum(copy["ModelVolume_mL"] for copy in copies),
                        material_ml=sum(copy["Volume_mL"] for copy in copies),
                        image=image,
                    )
                )

            # Sorters work one order at a time, so the labels for an order print together.
            labels.sort(key=lambda label: (label.order, label.part))
            builds.append(
                Build(
                    name=form_file.name if len(opened.scenes) == 1 else f"{form_file.name}, build {len(builds) + 1}",
                    material=metadata["MaterialName"],
                    layer_thickness_mm=metadata["LayerThickness_mm"],
                    material_ml=metadata["MaterialUsage_mL"],
                    date=DATE,
                    labels=labels,
                )
            )
    finally:
        for scene in opened.scenes:
            preform.delete_scene(scene_id=scene.scene_id)
    return builds


def main() -> None:
    orders = read_orders(ORDERS_FILE)
    with FormlabsClient() as client:
        try:
            preform = client.preform.connect(base_url=PREFORM_URL)
        except PreFormApiError as exc:
            sys.exit(
                f"{exc}\nNo PreForm at {PREFORM_URL}; "
                "open PreForm and start its API server"
            )

        with tempfile.TemporaryDirectory() as images:
            builds = fetch_builds(preform, FORM_FILE, orders, Path(images))
            if not any(build.labels for build in builds):
                sys.exit(f"No parts found in {FORM_FILE.name}")
            render_pdf(builds, OUTPUT_PATH)

    for build in builds:
        print(f"{build.name}: {len(build.labels)} labels, {build.material_ml:.1f} mL of {build.material}")
        for label in build.labels:
            print(f"  {label.order:<10} {label.quantity:3d} x {label.part:<28} {label.material_ml:6.1f} mL")
    print(f"-> {OUTPUT_PATH.name}")


if __name__ == "__main__":
    main()
