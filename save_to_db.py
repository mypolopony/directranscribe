# save_to_db.py

import sqlite3
import sys
import datetime

def save_transcript(label, transcript):
    conn = sqlite3.connect("transcripts.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS transcripts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            label TEXT,
            transcript TEXT
        );
    """)
    cur.execute("INSERT INTO transcripts (timestamp, label, transcript) VALUES (?, ?, ?)", (
        datetime.datetime.now().isoformat(),
        label,
        transcript.strip()
    ))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    label = sys.argv[1] if len(sys.argv) > 1 else "unknown"
    transcript = sys.stdin.read()
    if transcript.strip():
        save_transcript(label, transcript)