from fastapi import FastAPI
from fastapi.responses import StreamingResponse, HTMLResponse
import sqlite3, requests

app = FastAPI()
DB = "app/database.db"

@app.get("/")
def home():
    return HTMLResponse(open("static/index.html", encoding="utf-8").read())

@app.get("/play/{id}")
def play(id: int):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT video FROM lectures WHERE id=?", (id,))
    row = cur.fetchone()
    con.close()

    if not row:
        return {"error": "not found"}

    r = requests.get(row[0], stream=True)
    return StreamingResponse(r.iter_content(1024*1024), media_type="video/webm")
