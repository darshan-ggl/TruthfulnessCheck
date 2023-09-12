import requests
from truthfulnesscheck.config import config

API_KEY = config["MAPS"]["API_KEY"]
geocode_url = config["MAPS"]["GEOCODE_URL"]
autocomplete_url = config["MAPS"]["AUTOCOMPLETE_URL"]


def get_lat_lng(city_name, api_key=API_KEY):
    params = {
        "address": city_name,
        "key": api_key
    }
    response = requests.get(geocode_url, params=params)
    data = response.json()

    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        lat = location['lat']
        lng = location['lng']
        return f"{lat}, {lng}"
    else:
        return None


def places_existence(place, centric_city, radius, strictbounds, types='establishment', api_key=API_KEY):
    # Getting location lat long
    lat_long = get_lat_lng(centric_city)

    params = {
        'input': place,
        # 'location': lat_long,
        # 'radius':radius,
        'locationrestriction': f'circle:{radius}@{lat_long}',
        'strictbounds': strictbounds,
        'types': types,
        'rankby': radius,
        'key': api_key,
    }
    response = requests.get(autocomplete_url, params=params)
    return response.json()

