"""Label every part in a .form file with a serial number.

Open PreForm and start its API server on port 44388, then run:

    uv run serial_numbers.py cubes
    uv run serial_numbers.py arches

Set FL_LOCAL_BASE_URL to reach PreForm on another port or host.
"""

import argparse
import datetime
import math
import os
import sys
from dataclasses import dataclass
from pathlib import Path

from formlabs_sdk import FormlabsClient
from formlabs_preform_api.models import DirectionVectors, ScenePosition

HERE = Path(__file__).parent
PREFORM_URL = os.environ.get("FL_LOCAL_BASE_URL", "http://localhost:44388")

Vector = tuple[float, float, float]


@dataclass
class Build:
    form_file: str
    # A Python format string, filled in with the print date and the part's number.
    serial: str
    font_size_mm: float
    depth_mm: float
    # Where the label goes, in the coordinates the part's mesh file was made in. PreForm
    # projects the label from anchor, a point outside the part, onto the part's surface.
    # The label faces along facing, and its text reads along reading.
    anchor: Vector
    facing: Vector
    reading: Vector


BUILDS = {
    # 15 mm cubes with their origin at the center of the base, numbered on the top face.
    "cubes": Build("cubes.form", "{n:02d}", font_size_mm=8.0, depth_mm=1.0,
                   anchor=(0, 0, 30), facing=(0, 0, 1), reading=(1, 0, 0)),
    # Dental arches with the base on z = 0, the back on y = 0, and the front teeth
    # toward -y. The serial goes on the -x side of the base and reads toward the front
    # teeth, parallel to the build platform.
    "arches": Build("arches.form", "A{date:%y%m%d}-{n:03d}", font_size_mm=3.0, depth_mm=0.6,
                    anchor=(-50, -20, 2.5), facing=(-1, 0, 0), reading=(0, -1, 0)),
}


def turn(vector: Vector, degrees: float) -> Vector:
    """Turn a vector about the z axis, as PreForm turns a model."""
    c, s = math.cos(math.radians(degrees)), math.sin(math.radians(degrees))
    x, y, z = vector
    return (x * c - y * s, x * s + y * c, z)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("build", choices=BUILDS)
    build = BUILDS[parser.parse_args().build]
    form_file = HERE / build.form_file
    out = form_file.with_suffix(".serials.form")

    with FormlabsClient() as client:
        preform = client.preform.connect(base_url=PREFORM_URL)
        # PreForm resolves paths from its own working directory.
        scene_id = preform.open_form_file(file=str(form_file.resolve())).scenes[0].scene_id
        try:
            models = preform.list_models(scene_id=scene_id).models
            # Number the parts in reading order: back row first, left to right.
            models.sort(key=lambda m: (-round(m.position.y), m.position.x))
            for n, model in enumerate(models, start=1):
                serial = build.serial.format(date=datetime.date.today(), n=n)
                # A model's position is where its mesh file's origin sits on the
                # platform, and its orientation turns the mesh about that origin. These
                # parts print flat, so they only turn about z.
                yaw = model.orientation.z
                x, y, z = turn(build.anchor, yaw)
                result = preform.label_models(
                    scene_id=scene_id,
                    model_ids=[model.id],
                    label=serial,
                    position=ScenePosition(x=model.position.x + x, y=model.position.y + y, z=model.position.z + z),
                    # The label faces along z_direction and reads along x_direction.
                    orientation=DirectionVectors(
                        z_direction=list(turn(build.facing, yaw)), x_direction=list(turn(build.reading, yaw))
                    ),
                    font_size_mm=build.font_size_mm,
                    depth_mm=build.depth_mm,
                )
                # A label missing some of its characters is a wrong serial.
                if result.warnings:
                    sys.exit(f"{model.name}: {'; '.join(result.warnings)}")
                print(f"{serial:16} {model.name}")
            preform.save_form_file(file=str(out.resolve()), scene_ids=[scene_id])
        finally:
            preform.delete_scene(scene_id=scene_id)
    print(f"-> {out.name}")


if __name__ == "__main__":
    main()
