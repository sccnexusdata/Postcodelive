from __future__ import annotations
from math import asin, cos, radians, sin, sqrt

EARTH_RADIUS_KM = 6371.0088

def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    dlat = radians(lat2-lat1); dlon = radians(lon2-lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1))*cos(radians(lat2))*sin(dlon/2)**2
    return 2*EARTH_RADIUS_KM*asin(sqrt(a))

def within_radius(lat: float|None, lon: float|None, centre_lat: float, centre_lon: float, radius_km: float) -> bool:
    if lat is None or lon is None: return False
    return haversine_km(lat, lon, centre_lat, centre_lon) <= radius_km
