"""Fetch Berlin LOR polygons (Stand 01.01.2021) from the Geoportal WFS, simplify, split by level.

Source:  Amt für Statistik Berlin-Brandenburg / Statistische Einheiten im INSPIRE-Datenmodell
         (Lebensweltlich Orientierte Räume 01.01.2021), licence CC BY 3.0 DE.
Output:  public/app/data/geo/lor_<level>.geojson (EPSG:4326), properties: region_id, region_name.
"""

from __future__ import annotations

import argparse
import json
import pathlib

import httpx
from shapely.geometry import mapping, shape

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
WFS_URL = "https://gdi.berlin.de/services/wfs/su_lor"
WFS_PARAMS = {
    "service": "WFS",
    "version": "2.0.0",
    "request": "GetFeature",
    "typeNames": "su_lor:AreaStatisticalUnit",
    "outputFormat": "application/json",
    "srsName": "EPSG:4326",
}
LEVELS = {8: "planning_room", 6: "district_area", 4: "prediction_area"}
EXPECTED = {"planning_room": 542, "district_area": 143, "prediction_area": 58}
DECIMALS = 5  # ~1 m


def _round(coords):
    if isinstance(coords[0], (int, float)):
        return [round(c, DECIMALS) for c in coords]
    return [_round(c) for c in coords]


def build(raw: dict, tolerance: float) -> dict[str, dict]:
    collections = {
        level: {"type": "FeatureCollection", "features": []} for level in LEVELS.values()
    }
    for feat in raw["features"]:
        props = feat["properties"]
        region_id = props["thematicId"]["identifier"]
        level = LEVELS.get(len(region_id))
        if level is None:
            raise SystemExit(f"unexpected LOR id: {region_id}")
        geom = shape(feat["geometry"]).simplify(tolerance, preserve_topology=True)
        if geom.is_empty or not geom.is_valid:
            raise SystemExit(f"invalid geometry after simplification: {region_id}")
        mapped = mapping(geom)
        collections[level]["features"].append(
            {
                "type": "Feature",
                "id": region_id,
                "properties": {
                    "region_id": region_id,
                    "region_name": props["geographicalName"]["spelling"]["text"],
                },
                "geometry": {"type": mapped["type"], "coordinates": _round(mapped["coordinates"])},
            }
        )
    for level, expected in EXPECTED.items():
        got = len(collections[level]["features"])
        if got != expected:
            raise SystemExit(f"{level}: expected {expected} features, got {got}")
    return collections


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out-dir", default=str(BASE_DIR / "public" / "app" / "data" / "geo"))
    parser.add_argument("--raw-file", default=str(BASE_DIR / "data" / "raw" / "geo" / "lor_wfs.json"))
    parser.add_argument("--tolerance", type=float, default=0.00002, help="simplification in degrees")
    parser.add_argument("--refresh", action="store_true", help="download again even if raw file exists")
    args = parser.parse_args()

    raw_path = pathlib.Path(args.raw_file)
    if args.refresh or not raw_path.exists():
        raw_path.parent.mkdir(parents=True, exist_ok=True)
        response = httpx.get(WFS_URL, params=WFS_PARAMS, timeout=300.0)
        response.raise_for_status()
        raw_path.write_bytes(response.content)
    raw = json.loads(raw_path.read_text(encoding="utf-8"))

    out_dir = pathlib.Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for level, collection in build(raw, args.tolerance).items():
        path = out_dir / f"lor_{level}.geojson"
        path.write_text(json.dumps(collection, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        print(f"{path.name}: {len(collection['features'])} features, {path.stat().st_size / 1e6:.2f} MB")


if __name__ == "__main__":
    main()
