import requests
import json
import pandas as pd

def get_facilities_from_osm():
    overpass_url = "https://overpass-api.de/api/interpreter"
    query = """
    [out:json][timeout:60];
    area(3600062782)->.searchArea;
    (
      node["man_made"="wastewater_plant"](area.searchArea);
      way["man_made"="wastewater_plant"](area.searchArea);
      relation["man_made"="wastewater_plant"](area.searchArea);
    );
    out center;
    """
    response = requests.get(overpass_url, params={'data': query})
    response.raise_for_status()
    data = response.json()

    facilities = []
    for el in data['elements']:
        if el['type'] == 'node':
            lat, lon = el['lat'], el['lon']
        elif 'center' in el:
            lat, lon = el['center']['lat'], el['center']['lon']
        else:
            continue

        name = el.get('tags', {}).get('name', 'Unnamed')
        facilities.append({
            'osm_id': el['id'],
            'name': name,
            'lat': lat,
            'lon': lon
        })

    return pd.DataFrame(facilities)


df = get_facilities_from_osm()
df.to_csv("nrw_facilities.csv", index=False)
print(df.head())
