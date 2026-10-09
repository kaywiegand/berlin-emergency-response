"""Spatial helpers shared by notebooks: distances from LOR planning rooms to the city centre and to fire stations."""

from __future__ import annotations

import json

import numpy as np
import pandas as pd
from shapely.geometry import shape

from berlin_emergency_response.config import PATHS

ALEXANDERPLATZ = (13.4132, 52.5219)  # lon, lat; reference point for "distance to centre"


def haversine_km(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(np.radians, (lon1, lat1, lon2, lat2))
    a = np.sin((lat2 - lat1) / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1) / 2) ** 2
    return 2 * 6371.0 * np.arcsin(np.sqrt(a))


def planning_room_centroids() -> pd.DataFrame:
    geo = json.loads((PATHS["app_data"] / "geo" / "lor_planning_room.geojson").read_text(encoding="utf-8"))
    rows = []
    for f in geo["features"]:
        c = shape(f["geometry"]).centroid
        rows.append({"region_id": f["properties"]["region_id"], "lon": c.x, "lat": c.y})
    return pd.DataFrame(rows)


def nearest_km(points: pd.DataFrame, sites: pd.DataFrame) -> np.ndarray:
    """Straight-line distance from every point to its nearest site (both need lon and lat columns)."""
    d = haversine_km(points["lon"].to_numpy()[:, None], points["lat"].to_numpy()[:, None],
                     sites["lon"].to_numpy()[None, :], sites["lat"].to_numpy()[None, :])
    return d.min(axis=1)


def planning_room_distances(stations: pd.DataFrame) -> pd.DataFrame:
    """Per planning room: distance to the centre and to the nearest station of three station sets.

    `stations` needs station_type, lon, lat and rtw_alarms (from app_data/stations.parquet);
    RTW sites are those with RTW alarms since 2025.
    """
    cent = planning_room_centroids()
    cent["dist_centre_km"] = haversine_km(cent["lon"], cent["lat"], *ALEXANDERPLATZ)
    cent["nearest_rtw_km"] = nearest_km(cent, stations[stations["rtw_alarms"] > 0])
    cent["nearest_rescue_km"] = nearest_km(cent, stations[stations["station_type"].isin(["BF", "RW"])])
    cent["nearest_any_km"] = nearest_km(cent, stations)
    return cent
