"""Quote parts in every material on a price list: resin, print time, and price for each.

A service bureau's website answers "how much for ten of these in a tough resin?" in a
minute. For each material the parts are prepared the way they would print: oriented,
supported, and laid out on the build platform, then sliced for the print time. The
resin includes the supports and the raft.

Open PreForm and start its API server on port 44388, then run:

    uv run instant_quote.py bracket.stl --copies 10
    uv run instant_quote.py bracket.stl --materials grey,tough-2000 --json

Set FL_LOCAL_BASE_URL to reach PreForm on another port or host.
"""

import argparse
import json
import os
import sys
import tomllib
from pathlib import Path

from formlabs_sdk import FormlabsClient, PreFormApi, PreFormApiError

PRICING_FILE = Path(__file__).parent / "pricing.toml"
PREFORM_URL = os.environ.get("FL_LOCAL_BASE_URL", "http://localhost:44388")


def quote(
    preform: PreFormApi, shop: dict, material: dict, parts: list[Path], copies: int
) -> dict:
    """Prepare the parts as one build in this material and price it."""
    scene = preform.create_scene(
        machine_type=shop["machine_type"],
        material_code=material["material_code"],
        layer_thickness_mm=material["layer_thickness_mm"],
        print_setting=material.get("print_setting", "DEFAULT"),
    )
    try:
        for part in parts:
            # The server resolves the path from its own working directory.
            preform.import_models(
                scene_id=scene.scene_id, file=str(part.resolve()), name=part.stem
            )
        if copies > 1:
            preform.duplicate_models(scene_id=scene.scene_id, count=copies - 1)

        # Supports depend on the orientation, and the layout on both.
        preform.auto_orient_models(scene_id=scene.scene_id)
        preform.auto_support_models(scene_id=scene.scene_id)
        try:
            preform.auto_layout_models(scene_id=scene.scene_id)
        except PreFormApiError as exc:
            # By default a layout that can't place every model fails and leaves the
            # scene unchanged, so the material is reported unpriced.
            return {
                "material": material["label"],
                "error": f"does not fit on one build platform ({exc.code})",
            }

        print_time_s = preform.calculate_print_time(scene_id=scene.scene_id).total_print_time_s
        state = preform.get_scene(scene_id=scene.scene_id)
    finally:
        preform.delete_scene(scene_id=scene.scene_id)

    # volume_ml includes the supports and the raft; unsupported_volume_ml is the
    # parts alone.
    resin_ml = state.material_usage.volume_ml
    cost = {
        "resin": round(resin_ml * material["price_per_ml"], 2),
        "machine": round(print_time_s / 3600 * shop["machine_hour_rate"], 2),
        "setup": shop["setup_fee"],
    }
    # The total is the sum of the rounded lines, so the quote adds up as printed.
    cost["total"] = round(sum(cost.values()), 2)
    return {
        "material": material["label"],
        "layer_thickness_mm": material["layer_thickness_mm"],
        "models": len(state.models),
        "layers": state.layer_count,
        "print_time_s": print_time_s,
        "parts_ml": round(state.material_usage.unsupported_volume_ml, 1),
        "resin_ml": round(resin_ml, 1),
        "cost": cost,
    }


def hours_minutes(seconds: float) -> str:
    return f"{int(seconds // 3600)}h {int(seconds % 3600 // 60):02d}m"


def print_table(quotes: list[dict], shop: dict, parts: list[Path], copies: int) -> None:
    print(f"{len(parts)} part(s) x {copies} on {shop['machine_type']}: {', '.join(p.name for p in parts)}\n")
    print(
        f"{'material':18} {'layers':>6} {'print time':>10} {'parts mL':>8} {'resin mL':>8}"
        f" {'resin':>7} {'machine':>7} {'setup':>6} {'total ' + shop['currency']:>10}"
    )
    for q in quotes:
        if "error" in q:
            print(f"{q['material']:18} {q['error']}")
            continue
        c = q["cost"]
        print(
            f"{q['material']:18} {q['layers']:6d} {hours_minutes(q['print_time_s']):>10} {q['parts_ml']:8.1f}"
            f" {q['resin_ml']:8.1f} {c['resin']:7.2f} {c['machine']:7.2f} {c['setup']:6.2f} {c['total']:10.2f}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "parts", nargs="+", type=Path, help="STL, OBJ, or 3MF files to quote"
    )
    parser.add_argument(
        "--copies", type=int, default=1, help="copies of each part (default: 1)"
    )
    parser.add_argument(
        "--materials", help="comma-separated names from the price list (default: all)"
    )
    parser.add_argument(
        "--pricing", type=Path, default=PRICING_FILE,
        help="price list (default: pricing.toml)",
    )
    parser.add_argument("--json", action="store_true", help="print the quotes as JSON")
    args = parser.parse_args()

    pricing = tomllib.loads(args.pricing.read_text())
    shop, materials = pricing["shop"], pricing["materials"]
    chosen = args.materials.split(",") if args.materials else list(materials)
    unknown = [name for name in chosen if name not in materials]
    if unknown:
        sys.exit(
            f"Unknown materials {unknown}; the price list has {', '.join(materials)}"
        )

    with FormlabsClient() as client:
        try:
            preform = client.preform.connect(base_url=PREFORM_URL)
        except PreFormApiError as exc:
            sys.exit(
                f"{exc}\nNo PreForm at {PREFORM_URL}; "
                "open PreForm and start its API server"
            )
        quotes = [
            quote(preform, shop, materials[name], args.parts, args.copies)
            for name in chosen
        ]

    if args.json:
        result = {"parts": [p.name for p in args.parts], "copies": args.copies, "currency": shop["currency"]}
        print(json.dumps(result | {"quotes": quotes}, indent=2))
    else:
        print_table(quotes, shop, args.parts, args.copies)


if __name__ == "__main__":
    main()
