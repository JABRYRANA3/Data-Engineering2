"""
DE2 Final Project — Data generator for Track A (Esports).
Produces:
  - data/raw/matches_NNNN.csv  (3 CSV shards, ~2000 matchs each, batch ETL input)
  - data/streaming/source/batch_XX.json  (10 small JSON files for streaming)
  - data/corpus/esports_corpus.csv  (150 text docs for text + LLM pipeline)

Deterministic via seed=42.
"""

import csv, json, pathlib, random
from datetime import datetime, timedelta

random.seed(42)

# ============================================================
# 1) RAW MATCHES — main ETL dataset (3 CSV shards)
# ============================================================
heroes = [f"hero_{i:02d}" for i in range(1, 51)]
hero_weights = [1.0 / (i + 1) for i in range(len(heroes))]
teams = ["T1", "T2", "Gen.G", "DRX", "FNC", "G2", "C9", "TSM", "OG", "Liquid", "Secret", "EG"]
regions = ["KR", "EU", "NA", "CN", "SEA"]
patches = ["7.34", "7.34a", "7.34b", "7.35", "7.35a", "7.35b"]
roles = ["carry", "mid", "offlane", "support", "hard_support"]

raw_dir = pathlib.Path("data/raw")
raw_dir.mkdir(parents=True, exist_ok=True)

MATCHES_PER_SHARD = 2000
N_SHARDS = 3
base_time = datetime(2026, 1, 1, 0, 0, 0)

match_id_counter = 1
for shard in range(1, N_SHARDS + 1):
    out_file = raw_dir / f"matches_{shard:04d}.csv"
    with open(out_file, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        w.writerow([
            "match_id", "match_end_time", "team", "hero", "role",
            "kills", "deaths", "duration_sec", "region", "patch_version",
            "commentary_text"
        ])
        for _ in range(MATCHES_PER_SHARD):
            mtime = base_time + timedelta(minutes=random.randint(0, 60*24*120))
            team = random.choice(teams)
            region = random.choice(regions)
            patch = random.choice(patches)
            # 5 picks per match → 5 rows per match_id
            chosen_heroes = set()
            while len(chosen_heroes) < 5:
                chosen_heroes.add(random.choices(heroes, weights=hero_weights, k=1)[0])
            for hero in chosen_heroes:
                role = random.choice(roles)
                kills = random.randint(0, 35)
                deaths = random.randint(0, 35)
                duration = random.randint(900, 3600)
                # Inject some null/dirty data ~3%
                if random.random() < 0.02:
                    duration = None
                commentary = (
                    f"In this match between {team} and a rival on patch {patch}, "
                    f"the {hero} {role} ended with {kills} kills and {deaths} deaths. "
                    f"The team coordinated objectives effectively and used the {hero} ultimate ability "
                    f"to swing crucial team fights. Match duration was approximately "
                    f"{duration if duration else 'unknown'} seconds."
                )
                w.writerow([
                    match_id_counter,
                    mtime.strftime("%Y-%m-%dT%H:%M:%S"),
                    team, hero, role, kills, deaths,
                    duration if duration is not None else "",
                    region, patch, commentary
                ])
            match_id_counter += 1
    print(f"Wrote {out_file} with ~{MATCHES_PER_SHARD * 5} rows")

print(f"\nTotal raw rows: ~{N_SHARDS * MATCHES_PER_SHARD * 5}")

# ============================================================
# 2) STREAMING SOURCE — 10 small JSON files
# ============================================================
stream_dir = pathlib.Path("data/streaming/source")
stream_dir.mkdir(parents=True, exist_ok=True)
landing_dir = pathlib.Path("data/streaming/landing")
landing_dir.mkdir(parents=True, exist_ok=True)
# clean landing
for f in landing_dir.glob("*.json"):
    f.unlink()

stream_base = datetime(2026, 5, 9, 10, 0, 0)
for batch_idx in range(1, 11):
    events = []
    batch_start = stream_base + timedelta(minutes=30 * (batch_idx - 1))
    n_events = random.randint(5, 12)
    for _ in range(n_events):
        ts = batch_start + timedelta(seconds=random.randint(0, 30*60))
        events.append({
            "match_id": match_id_counter,
            "match_end_time": ts.strftime("%Y-%m-%dT%H:%M:%S"),
            "team": random.choice(teams),
            "kills": random.randint(0, 35),
            "deaths": random.randint(0, 35),
            "duration_sec": random.randint(900, 3600),
        })
        match_id_counter += 1
    out_file = stream_dir / f"batch_{batch_idx:02d}.json"
    with open(out_file, "w") as f:
        for ev in events:
            f.write(json.dumps(ev) + "\n")
    print(f"Wrote streaming {out_file} ({len(events)} events)")

# ============================================================
# 3) TEXT CORPUS — 150 docs (for text pipeline + LLM prep)
# ============================================================
corpus_dir = pathlib.Path("data/corpus")
corpus_dir.mkdir(parents=True, exist_ok=True)

hero_lore = [
    ("dragon_knight", "The Dragon Knight is a tanky melee hero who uses fire breath as his ultimate ability. His mana pool is small but his damage output scales with strength. The hero excels at pushing lanes and controlling team fights."),
    ("crystal_maiden", "Crystal Maiden is a ranged support hero with strong mana regeneration. Her ultimate ability deals magical damage in a wide area. The hero is fragile but provides crucial vision and slows."),
    ("invoker", "Invoker is a complex intelligence hero with ten different abilities combined from three orbs. He requires high skill to play but rewards mastery with massive damage and utility."),
    ("phantom_assassin", "Phantom Assassin is an agility carry with critical strike passive ability. Her damage scales with attack speed and items. The hero deals physical damage and can solo kill heroes."),
    ("pudge", "Pudge is a strength hero famous for his hook ability that pulls enemies. His ultimate ability deals high magical damage to a single target. The hero builds tanky and roams the map."),
    ("anti_mage", "Anti Mage is an agility carry hero who counters mana-dependent enemies. His passive burns enemy mana and deals damage based on mana burned. His ultimate teleports him short distances."),
    ("axe", "Axe is a melee strength hero who excels at initiation. His ultimate ability culls low health enemies instantly. The hero builds tanky armor and uses his call ability to taunt nearby enemies."),
    ("lina", "Lina is an intelligence hero who deals fire damage. Her ultimate ability is a single target magical nuke. The hero combines stuns and damage to burst down targets quickly in team fights."),
    ("juggernaut", "Juggernaut is an agility carry hero with strong solo kill potential. His ultimate spins blades dealing physical damage. The hero is mobile and can dodge spells with omnislash."),
    ("witch_doctor", "Witch Doctor is an intelligence support hero with paralyzing cask stun. His ultimate ability targets a single enemy dealing massive damage over time."),
]

actions = ["nerfed", "buffed", "reworked", "tweaked", "balanced", "adjusted"]
attrs = ["damage", "mana cost", "cooldown", "range", "duration", "armor", "movement speed", "attack speed"]
items = ["divine rapier", "battle fury", "black king bar", "shadow blade", "manta style", "butterfly", "monkey king bar", "satanic", "heart of tarrasque"]

docs = []
doc_id = 1
for hero_id, lore in hero_lore:
    docs.append((f"hero_{doc_id:03d}", lore))
    doc_id += 1
for _ in range(60):
    hero = random.choice(hero_lore)[0]
    text = (f"Patch update {hero} ability has been {random.choice(actions)}. "
            f"The {random.choice(attrs)} value was changed by {random.choice([5,10,15,20])} percent. "
            f"This adjustment aims to bring the hero in line with the current meta. "
            f"Players should expect different gameplay strategies in upcoming matches.")
    docs.append((f"patch_{doc_id:03d}", text))
    doc_id += 1
for _ in range(30):
    item = random.choice(items)
    text = (f"The item {item} provides bonus {random.choice(attrs)} to the hero. "
            f"It is commonly built on carry heroes that need extra survivability and damage. "
            f"The item costs significant gold but offers strong stats and passive abilities.")
    docs.append((f"item_{doc_id:03d}", text))
    doc_id += 1
for _ in range(50):
    team1, team2 = random.sample(teams, 2)
    hero = random.choice(hero_lore)[0]
    kills = random.randint(5, 30)
    text = (f"In the recent match between {team1} and {team2}, a player dominated playing {hero} "
            f"with {kills} kills. The team coordinated objectives and secured map control. "
            f"Their ultimate timings were perfect throughout the team fights.")
    docs.append((f"match_{doc_id:03d}", text))
    doc_id += 1

out_corpus = corpus_dir / "esports_corpus.csv"
with open(out_corpus, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, quoting=csv.QUOTE_ALL)
    w.writerow(["doc_id", "text"])
    for did, text in docs:
        w.writerow([did, text])
print(f"Wrote corpus {out_corpus} ({len(docs)} docs)")

print("\nAll project data generated.")
