import pandas as pd

from berlin_emergency_response.spatial import ALEXANDERPLATZ, haversine_km, nearest_km, planning_room_centroids


def test_haversine_known_distance():
    # Alexanderplatz to Brandenburger Tor is roughly 2 km
    d = haversine_km(*ALEXANDERPLATZ, 13.3777, 52.5163)
    assert 2.0 < float(d) < 3.5


def test_nearest_picks_closest_site():
    points = pd.DataFrame({"lon": [13.40], "lat": [52.52]})
    sites = pd.DataFrame({"lon": [13.40, 13.60], "lat": [52.52, 52.60]})
    assert nearest_km(points, sites)[0] < 0.01


def test_centroids_cover_all_planning_rooms():
    assert len(planning_room_centroids()) == 542
