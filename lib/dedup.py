#!/usr/bin/env python3
# Contract: read JSON from stdin; exit 0 if new (not duplicate)
import json, hashlib, sqlite3, sys, os

DB = os.environ.get("DEDUP_DB", "dedup.db")

def md5(s):
    return hashlib.md5(s.encode()).hexdigest()

def main():
    raw = sys.stdin.read()
    try:
        obj = json.loads(raw)
    except Exception:
        sys.exit(1)
    payload = json.dumps({"prompt": obj.get("prompt",""), "response": obj.get("response","")}, sort_keys=True)
    key = md5(payload)

    conn = sqlite3.connect(DB)
    conn.execute("CREATE TABLE IF NOT EXISTS seen (key TEXT PRIMARY KEY)")
    try:
        conn.execute("INSERT INTO seen (key) VALUES (?)", (key,))
        conn.commit()
        conn.close()
        print(json.dumps(obj))
        sys.exit(0)
    except sqlite3.IntegrityError:
        conn.close()
        sys.exit(1)

if __name__ == "__main__":
    main()