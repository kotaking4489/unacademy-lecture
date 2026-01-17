import sqlite3, requests, re

DB = "app/database.db"
TXT = "input/lectures.txt"

con = sqlite3.connect(DB)
cur = con.cursor()

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

    title, subject, url = [x.strip() for x in line.split("|")]

    html = requests.get(url).text
    m = re.search(r'"videoUrl":"(.*?)"', html)

    if not m:
        continue

    video = m.group(1).replace("\\/", "/")
    cur.execute("INSERT INTO lectures(title, video) VALUES(?,?)", (title, video))

con.commit()
con.close()

print("Lectures updated")
