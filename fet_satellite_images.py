import requests, os
from tqdm import tqdm
import pandas as pd
from dotenv import load_dotenv

# Load your OpenAI API key
load_dotenv()
AZURE_MAPS_KEY = os.getenv("AZURE_MAPS_KEY")

IMG_DIR = "facility_images_azure"
os.makedirs(IMG_DIR, exist_ok=True)

def download_image(lat, lon, osm_id, zoom=15, size=(512, 512)):
    if pd.isna(lat) or pd.isna(lon):
        print(f"Skipping {osm_id}: Invalid coordinates")
        return

    url = (
        "https://atlas.microsoft.com/map/static/png?api-version=1.0"
        f"&layer=hybrid&style=main&zoom={zoom}"
        f"&center={lon},{lat}&width={size[0]}&height={size[1]}"
        f"&subscription-key={AZURE_MAPS_KEY}"
    )
    resp = requests.get(url)
    if resp.ok:
        with open(f"{IMG_DIR}/{osm_id}.png", "wb") as f:
            f.write(resp.content)
    else:
        print(f"Error {resp.status_code} for {osm_id}: {resp.text}")


df = pd.read_csv("nrw_facilities.csv")
for _, row in tqdm(df.iterrows(), total=len(df)):
    download_image(row.lat, row.lon, row.osm_id)
