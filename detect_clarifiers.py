import base64
import os
import pandas as pd
from tqdm import tqdm
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def encode_image(path):
    return base64.b64encode(open(path, "rb").read()).decode("utf-8")

def ask_gpt4_with_vision(image_path, prompt):
    img_b64 = encode_image(image_path)
    resp = client.chat.completions.create(
        model="gpt-4o",  # or gpt-4o, gpt-4o-mini, gpt-4-turbo-vision
        messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": [
            {"type": "text", "text": "Count the circular clarifiers visible in this satellite image. And return only the number."},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}}
        ]},
        ],
        max_tokens=200
    )
    return resp.choices[0].message.content

# Run on each image
directory = "facility_images_azure"
prompt = (
    "Count the circular clarifiers visible in this satellite image "
    "of a water treatment facility."
)

rows = []
for fname in tqdm(os.listdir(directory)):
    if fname.lower().endswith((".png", ".jpg", ".jpeg")):
        content = ask_gpt4_with_vision(os.path.join(directory, fname), prompt)
        rows.append({"image": fname, "response": content})

# Save results
pd.DataFrame(rows).to_csv("clarifier_counts.csv", index=False)
print("Done processing", len(rows), "images.")




import sqlite3

# Connect to SQLite DB (will create if doesn't exist)
conn = sqlite3.connect("clarifiers.db")
cur = conn.cursor()

# Create table
cur.execute("""
CREATE TABLE IF NOT EXISTS clarifier_counts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    image TEXT NOT NULL,
    clarifier_count INTEGER,
    response TEXT
);
""")

import re
def extract_count(response):
    match = re.search(r'\\d+', response)
    return int(match.group()) if match else None

# Insert each record
for row in rows:
    count = row["response"]
    cur.execute(
        "INSERT INTO clarifier_counts (image, clarifier_count, response) VALUES (?, ?, ?)",
        (row["image"], count, row["response"])
    )

conn.commit()
conn.close()
print("Saved to clarifiers.db ✅")