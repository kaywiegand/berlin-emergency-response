"""Fetch Berlin fire station sites and operational areas from the Geoportal WFS.

Source:  Berliner Feuerwehr, "Feuerwehr Standorte und Einsatzbereiche" (Geoportal Berlin, WFS `feuerwehr`),
         licence dl-de-zero-2.0 (no attribution required).
Output:  dbt/seeds/seed_stations.csv                     one row per site (BF, FF, RW), WGS84 coordinates
         public/app/data/geo/fire_operational_areas.geojson  the six operational areas (Einsatzbereiche)
The sites carry a `source_date` (Stand); the dataset changes rarely, so this is a one-off script like fetch_lor.py.
"""

from __future__ import annotations

import argparse
import csv
import json
import pathlib

import httpx

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
WFS_URL = "https://gdi.berlin.de/services/wfs/feuerwehr"
LAYERS = {"sites": "feuerwehr:a_feuerwehr_standorte", "areas": "feuerwehr:b_feuerwehr_einsatzbereiche"}
STATION_TYPES = {"BF", "FF", "RW"}
EXPECTED_AREAS = 6
SEED_COLUMNS = [
    "station_id", "station_name", "station_type", "volunteer_id", "address", "postcode",
    "district_name", "operational_area", "lon", "lat", "source_date",
]  # fmt: skip


def fetch(layer: str) -> dict:
    params = {
        "service": "WFS", "version": "2.0.0", "request": "GetFeature", "typeNames": layer,
        "outputFormat": "application/json", "srsName": "EPSG:4326",
    }  # fmt: skip
    response = httpx.get(WFS_URL, params=params, timeout=120.0)
    response.raise_for_status()
    return response.json()


def to_rows(sites: dict) -> list[dict]:
    rows = []
    for feat in sites["features"]:
        p, (lon, lat) = feat["properties"], feat["geometry"]["coordinates"]
        if p["wach_typ"] not in STATION_TYPES:
            raise SystemExit(f"unknown station type: {p['wach_typ']} ({p['wach_nr']})")
        rows.append({
            "station_id": str(p["wach_nr"]), "station_name": p["wach_name"], "station_type": p["wach_typ"],
            "volunteer_id": p["ff_nr"], "address": p["adresse"], "postcode": p["plz"],
            "district_name": p["bezirk"], "operational_area": p["eb_kurz"],
            "lon": round(lon, 6), "lat": round(lat, 6), "source_date": p["stand"],
        })  # fmt: skip
    ids = [r["station_id"] for r in rows]
    if len(ids) != len(set(ids)):
        raise SystemExit("duplicate station ids in source")
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--seed", default=str(BASE_DIR / "dbt" / "seeds" / "seed_stations.csv"))
    parser.add_argument("--areas", default=str(BASE_DIR / "public" / "app" / "data" / "geo" / "fire_operational_areas.geojson"))
    args = parser.parse_args()

    rows = to_rows(fetch(LAYERS["sites"]))
    areas = fetch(LAYERS["areas"])
    if len(areas["features"]) != EXPECTED_AREAS:
        raise SystemExit(f"expected {EXPECTED_AREAS} operational areas, got {len(areas['features'])}")

    seed = pathlib.Path(args.seed)
    seed.parent.mkdir(parents=True, exist_ok=True)
    with seed.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=SEED_COLUMNS)
        writer.writeheader()
        writer.writerows(sorted(rows, key=lambda r: r["station_id"]))
    out = pathlib.Path(args.areas)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(areas, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"{seed.name}: {len(rows)} stations; {out.name}: {len(areas['features'])} areas ({out.stat().st_size / 1e6:.2f} MB)")


if __name__ == "__main__":
    main()
