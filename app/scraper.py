import sqlite3
import requests
import re
import os

DB = "app/database.db"
TXT = "input/lectures.txt"

os.makedirs("app", exist_ok=True)

conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS lectures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    video TEXT
)
""")

with open(TXT, "r", encoding="utf-8") as f:
    lines = f.read().splitlines()

for line in lines:
    if "|" not in line:
        continue

    title, url = [x.strip() for x in line.split("|", 1)]

    try:
        html = requests.get(url, timeout=15).text
    except:
        continue

    match = re.search(r'"videoUrl":"(.*?)"', html)
    if not match:
        continue

    video = match.group(1).replace("\\/", "/")

    cur.execute(
        "INSERT INTO lectures(title, video) VALUES (?,?)",
        (title, video)
    )

conn.commit()
conn.close()

print("✅ Lectures updated")
