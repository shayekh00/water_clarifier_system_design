from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# CORS to allow frontend calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/clarifiers")
def get_clarifiers(min: int = 0, max: int = 100):
    conn = sqlite3.connect("clarifiers.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT image, clarifier_count FROM clarifier_counts WHERE clarifier_count BETWEEN ? AND ?",
        (min, max)
    )
    rows = cursor.fetchall()
    conn.close()
    return [{"image": row[0], "clarifier_count": row[1]} for row in rows]
