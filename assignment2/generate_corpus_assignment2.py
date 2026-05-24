"""
Generate a synthetic esports text corpus for DE2 Assignment 2 - Track A.
Produces data/corpus/esports_corpus.csv with ~150 documents
(hero lore + patch notes + item descriptions + match commentary).
"""

import csv
import pathlib
import random

random.seed(42)

out_dir = pathlib.Path("data/corpus")
out_dir.mkdir(parents=True, exist_ok=True)
out_file = out_dir / "esports_corpus.csv"

heroes = [
    ("dragon_knight", "The Dragon Knight is a tanky melee hero who uses fire breath as his ultimate ability. His mana pool is small but his damage output scales with strength. The hero excels at pushing lanes and controlling team fights."),
    ("crystal_maiden", "Crystal Maiden is a ranged support hero with strong mana regeneration. Her ultimate ability deals magical damage in a wide area. The hero is fragile but provides crucial vision and slows for the team."),
    ("invoker", "Invoker is a complex intelligence hero with ten different abilities combined from three orbs. He requires high skill to play but rewards mastery with massive damage and utility. His ultimate gives him scaling stats."),
    ("phantom_assassin", "Phantom Assassin is an agility carry with critical strike passive ability. Her damage scales with attack speed and items. The hero deals physical damage and can solo kill heroes with low health."),
    ("pudge", "Pudge is a strength hero famous for his hook ability that pulls enemies. His ultimate ability deals high magical damage to a single target. The hero builds tanky and roams the map looking for kills."),
    ("anti_mage", "Anti Mage is an agility carry hero who counters mana-dependent enemies. His passive burns enemy mana and deals damage based on mana burned. His ultimate teleports him short distances allowing fast farming."),
    ("axe", "Axe is a melee strength hero who excels at initiation. His ultimate ability culls low health enemies instantly. The hero builds tanky armor and uses his call ability to taunt nearby enemies."),
    ("lina", "Lina is an intelligence hero who deals fire damage. Her ultimate ability is a single-target magical nuke. The hero combines stuns and damage to burst down targets quickly in team fights."),
    ("juggernaut", "Juggernaut is an agility carry hero with strong solo kill potential. His ultimate spins blades dealing physical damage to a single target. The hero is mobile and can dodge spells with omnislash."),
    ("witch_doctor", "Witch Doctor is an intelligence support hero with paralyzing cask stun. His ultimate ability targets a single enemy dealing massive damage over time. The hero is fragile but deals high magical damage early."),
]

actions = ["nerfed", "buffed", "reworked", "tweaked", "balanced", "adjusted", "modified", "increased", "decreased", "removed"]
attributes = ["damage", "mana cost", "cooldown", "range", "duration", "armor", "movement speed", "attack speed", "health", "regeneration"]
items = ["divine rapier", "battle fury", "black king bar", "shadow blade", "manta style", "butterfly", "monkey king bar", "satanic", "heart of tarrasque", "skull basher"]

teams = ["T1", "Gen.G", "DRX", "FNC", "G2", "Cloud9", "TSM", "OG", "Liquid", "Secret"]
players = ["Faker", "Caps", "ShowMaker", "Knight", "Chovy", "Ruler", "Viper", "Doinb", "Rookie", "Uzi"]

documents = []
doc_id = 1

# Hero lore docs (10)
for hero_id, lore in heroes:
    documents.append((f"hero_{doc_id:03d}", lore))
    doc_id += 1

# Patch notes docs (60)
for _ in range(60):
    hero = random.choice(heroes)[0]
    action = random.choice(actions)
    attr = random.choice(attributes)
    pct = random.choice([5, 10, 15, 20, 25])
    text = f"Patch update {hero} ability has been {action}. The {attr} value was changed by {pct} percent. This adjustment aims to bring the hero in line with the current meta. Players should expect different gameplay strategies in upcoming matches."
    documents.append((f"patch_{doc_id:03d}", text))
    doc_id += 1

# Item descriptions (30)
for _ in range(30):
    item = random.choice(items)
    attr = random.choice(attributes)
    text = f"The item {item} provides bonus {attr} to the hero. It is commonly built on carry heroes that need extra survivability and damage. The item costs significant gold but offers strong stats and passive abilities."
    documents.append((f"item_{doc_id:03d}", text))
    doc_id += 1

# Match commentary (50)
for _ in range(50):
    team1 = random.choice(teams)
    team2 = random.choice([t for t in teams if t != team1])
    player = random.choice(players)
    hero = random.choice(heroes)[0]
    kills = random.randint(5, 30)
    text = f"In the recent match between {team1} and {team2}, player {player} dominated the game playing {hero} with {kills} kills. The team coordinated objectives and secured map control. Their ultimate timings were perfect throughout the team fights."
    documents.append((f"match_{doc_id:03d}", text))
    doc_id += 1

with open(out_file, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, quoting=csv.QUOTE_ALL)
    w.writerow(["doc_id", "text"])
    for did, text in documents:
        w.writerow([did, text])

print(f"Wrote {len(documents)} documents to {out_file}")
print(f"Sample row: ('{documents[0][0]}', '{documents[0][1][:60]}...')")
