from typing import Union
import requests

############################
# Get Geolocation Data
############################


def get_address_from_location(lat: str, lon: str) -> dict:
    r = requests.get(
        f'https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat={lat}&lon={lon}')

    if(r.ok):
        res = r.json()
        return res
    return {"status": False}
