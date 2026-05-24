"""
Generate synthetic match-picks data for DE2 Assignment 3 - Track A (Esports).
Produces data/match_picks.csv with 200 matches x 5 heroes = 1000 picks.
"""

import csv
import pathlib
import random

random.seed(42)

heroes = [f"hero_{i:02d}" for i in range(1, 51)]
weights = [1.0 / (i + 1) for i in range(len(heroes))]

n_matches = 200
heroes_per_match = 5

out_dir = pathlib.Path("data")
out_dir.mkdir(parents=True, exist_ok=True)
out_file = out_dir / "match_picks.csv"

with open(out_file, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["match_id", "hero_id"])
    for match_id in range(1, n_matches + 1):
        chosen = set()
        attempts = 0
        while len(chosen) < heroes_per_match and attempts < 200:
            h = random.choices(heroes, weights=weights, k=1)[0]
            chosen.add(h)
            attempts += 1
        for h in chosen:
            w.writerow([match_id, h])

print(f"Wrote {n_matches} matches with {heroes_per_match} heroes each to {out_file}")
print(f"Total picks: {n_matches * heroes_per_match}")
