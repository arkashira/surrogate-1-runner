# Keep existing central md5 store behavior; this file is imported by the runner.
import hashlib, json, sys, argparse, sqlite3, os

DB_PATH = os.getenv("DEDUP_DB", "/tmp/dedup_hashes.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("CREATE TABLE IF NOT EXISTS hashes (md5 TEXT PRIMARY KEY)")
    conn.commit()
    return conn

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default=sys.stdin, type=argparse.FileType("r"))
    ap.add_argument("--output", default=sys.stdout, type=argparse.FileType("w"))
    args = ap.parse_args()

    conn = init_db()
    seen = set(r[0] for r in conn.execute("SELECT md5 FROM hashes").fetchall())
    new_hashes = []

    for line in args.input:
        line = line.strip()
        if not line:
            continue
        md5 = hashlib.md5(line.encode()).hexdigest()
        if md5 in seen:
            continue
        seen.add(md5)
        new_hashes.append(md5)
        args.output.write(line + "\n")

    if new_hashes:
        conn.executemany("INSERT OR IGNORE INTO hashes (md5) VALUES (?)", [(h,) for h in new_hashes])
        conn.commit()
    conn.close()

if __name__ == "__main__":
    main()