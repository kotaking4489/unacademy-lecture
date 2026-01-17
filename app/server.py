from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
import sqlite3
import requests
import os

app = FastAPI()
DB = "app/database.db"


def init_db():
    if not os.path.exists(DB):
        import app.scraper


init_db()


@app.get("/")
def home():
    with open("static/index.html", encoding="utf-8") as f:
        return HTMLResponse(f.read())


@app.get("/api/lectures")
def lectures():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT id, title FROM lectures")
    rows = cur.fetchall()
    con.close()
    return rows


@app.get("/play/{lecture_id}")
def play(lecture_id: int):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT video FROM lectures WHERE id=?", (lecture_id,))
    row = cur.fetchone()
    con.close()

    if not row:
        return {"error": "Lecture not found"}

    real_url = row[0]
    r = requests.get(real_url, stream=True)

    return StreamingResponse(
        r.iter_content(chunk_size=1024 * 1024),
        media_type="video/webm"
    )
