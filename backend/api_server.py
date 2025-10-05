from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

app = FastAPI()

# Allow frontend dev server to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/recipes")
def get_recipes(filter_type: str = "new"):
    conn = sqlite3.connect("user_data.db")
    c = conn.cursor()
    query = "SELECT * FROM recipes ORDER BY created_at DESC"
    if filter_type == "healthiest":
        query = "SELECT * FROM recipes WHERE instructions LIKE '%healthy%' ORDER BY created_at DESC"
    elif filter_type == "popular":
        query = "SELECT * FROM recipes ORDER BY id DESC LIMIT 10"
    c.execute(query)
    rows = c.fetchall()
    conn.close()
    # Convert to dicts for JSON response
    return [{"id": r[0], "title": r[1], "ingredients": r[2], "instructions": r[3], "created_at": r[4]} for r in rows]
