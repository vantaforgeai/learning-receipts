#!/usr/bin/env python3
"""Learning Receipts — prove that corrections changed behavior."""
import json, os, sys, sqlite3
from datetime import datetime

DB_PATH = os.path.expanduser("~/learning-receipts/receipts.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS corrections (id INTEGER PRIMARY KEY AUTOINCREMENT, source TEXT, claim TEXT, correction TEXT, confidence REAL, timestamp TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS decisions (id INTEGER PRIMARY KEY AUTOINCREMENT, action TEXT, reasoning TEXT, related_correction_id INTEGER, changed INTEGER DEFAULT 0, timestamp TEXT)")
    conn.commit()
    conn.close()

def add_correction(source, claim, correction, confidence=0.5):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO corrections (source, claim, correction, confidence, timestamp) VALUES (?, ?, ?, ?, ?)", (source, claim, correction, confidence, datetime.now().isoformat()))
    conn.commit()
    cid = c.lastrowid
    conn.close()
    print(f"Correction #{cid} recorded from {source}")

def add_decision(action, reasoning, correction_id=None, changed=False):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO decisions (action, reasoning, related_correction_id, changed, timestamp) VALUES (?, ?, ?, ?, ?)", (action, reasoning, correction_id, 1, datetime.now().isoformat()))
    conn.commit()
    did = c.lastrowid
    conn.close()
    print(f"Decision #{did} recorded (changed: {changed})")

def receipt():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT d.id, d.action, d.reasoning, c.source, c.correction, d.timestamp FROM decisions d JOIN corrections c ON d.related_correction_id = c.id WHERE d.changed = 1 ORDER BY d.timestamp DESC")
    rows = c.fetchall()
    conn.close()
    if not rows:
        print("No behavior changes on record yet.")
        return
    print("=" * 60)
    print("LEARNING RECEIPTS — Proven Behavior Changes")
    print("=" * 60)
    for r in rows:
        print(f"\nDecision #{r[0]} at {r[5][:19]}")
        print(f"  Action: {r[1]}")
        print(f"  Reason: {r[2]}")
        print(f"  Changed because {r[3]} said: \"{r[4][:80]}...\"")

def list_all():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM corrections")
    cc = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM decisions WHERE changed = 1")
    dc = c.fetchone()[0]
    conn.close()
    print(f"Corrections: {cc}")
    print(f"Proven behavior changes: {dc}")

if __name__ == "__main__":
    init_db()
    if len(sys.argv) < 2:
        print("Usage: learning_receipts.py [add-correction|add-decision|receipt|stats]")
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "add-correction" and len(sys.argv) >= 5:
        add_correction(sys.argv[2], sys.argv[3], sys.argv[4], float(sys.argv[5]) if len(sys.argv) > 5 else 0.5)
    elif cmd == "add-decision" and len(sys.argv) >= 4:
        cid = int(sys.argv[4]) if len(sys.argv) > 4 and sys.argv[4] != "-" else None
        changed = sys.argv[5].lower() == "true" if len(sys.argv) > 5 else False
        add_decision(sys.argv[2], sys.argv[3], cid, changed)
    elif cmd == "receipt":
        receipt()
    elif cmd == "stats":
        list_all()
    else:
        print("Unknown command")
