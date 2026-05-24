"""
Generate 10 synthetic JSON files for DE2 Lab 1 - Track A (Esports).
"""

import json
import pathlib
import random
from datetime import datetime, timedelta

random.seed(42)

teams = ["T1", "T2", "Gen.G", "DRX", "FNC", "G2", "C9", "TSM"]
out_dir = pathlib.Path("data/source")
out_dir.mkdir(parents=True, exist_ok=True)

base = datetime(2026, 5, 9, 10, 0, 0)

match_id = 1
for batch_idx in range(1, 11):
    events = []
    batch_start = base + timedelta(minutes=30 * (batch_idx - 1))
    n_events = random.randint(5, 12)
    for _ in range(n_events):
        offset_sec = random.randint(0, 30 * 60)
        ts = batch_start + timedelta(seconds=offset_sec)
        events.append({
            "match_id": match_id,
            "match_end_time": ts.strftime("%Y-%m-%dT%H:%M:%S"),
            "team": random.choice(teams),
            "kills": random.randint(0, 35),
            "deaths": random.randint(0, 35),
            "duration_sec": random.randint(900, 3600),
        })
        match_id += 1

    out_file = out_dir / f"batch_{batch_idx:02d}.json"
    with open(out_file, "w") as f:
        for ev in events:
            f.write(json.dumps(ev) + "\n")
    print(f"Wrote {out_file} with {len(events)} events")

print("\nDone. 10 JSON files in data/source/")