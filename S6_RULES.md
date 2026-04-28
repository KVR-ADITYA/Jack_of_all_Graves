# Elden Ring Season 6 Bingo — Rules & Mechanics Reference

This document captures all S6-specific rules, game mechanics, and implementation
decisions so they don't need to be re-explained in future sessions.

---

## Bingo Format

- **Board**: 5×5 grid, 25 squares, drawn from the Base category pool in `s6_base_bingo.json`
- **Mode**: **Lockout bingo** — when a player marks a square, the opponent is permanently blocked from marking it
- **Lines**: 12 lines — 5 rows, 5 columns, 2 diagonals
- **Win conditions** (in priority order):
  1. **Bingo**: Complete any row, column, or diagonal → win immediately
  2. **Majority**: If all 25 squares are marked and no bingo exists, the player with **13+** squares wins
  - Majority trumps an available bingo (if you have 13 squares but no line, you still win)
- **No prep timer**
- **No time limit** (but the simulation uses timing to model realistic game pace)

---

## S6 Weapon Randomization

- **Weapon class is retained** — each weapon slot stays in its class (e.g. a Greatsword is always replaced by another Greatsword)
- **Specific weapon is randomized** — the exact item within the class changes every game
- **Staves are NOT randomized** — always the same world pickups (Meteorite Staff, Staff of Loss, etc.)
- **Seals are randomized by name** but a Sacred Seal is always available as a free pickup at Roundtable Hold
- **Vendors** (Sellen, Corhyn, Miriel, etc.) sell the same count of spells/incantations but the specific items are randomized
- **Starting weapons**: each player starts with a randomized weapon of a randomized class; weapon class determines primary stat assumption

### Primary stat by weapon class (default)
| Class | Stat |
|-------|------|
| Glintstone Staff | Int |
| Sacred Seal | Faith |
| Dagger, Katana, Claw, Thrusting Sword, Twinblade, Curved Sword | Dexterity |
| Everything else | Strength |

---

## Auto-Upgrade Rule (+0 Weapon Squares)

- Some squares require killing a boss **with a +0 weapon only** (e.g. "Kill Agheel with a +0 weapon only")
- **As soon as any weapon upgrade is performed** (weapon goes from +0 to +1), ALL "+0 weapon only" squares become permanently invalid for that player — they can no longer be targeted or completed
- This means players must decide early whether to pursue +0 weapon squares before upgrading

---

## Smithing Stone Model

### Standard weapons (Smithing Stones, max +24)
- **3× Stone[N] per 3 upgrade levels**: Stone[1] for +1→+3, Stone[2] for +4→+6, Stone[3] for +7→+9, etc.
- Full upgrade path to +24:

| Upgrade levels | Stone tier needed | Count |
|----------------|------------------|-------|
| +1 → +3        | Stone [1]        | 3     |
| +4 → +6        | Stone [2]        | 3     |
| +7 → +9        | Stone [3]        | 3     |
| +10 → +12      | Stone [4]        | 3     |
| +13 → +15      | Stone [5]        | 3     |
| +16 → +18      | Stone [6]        | 3     |
| +19 → +21      | Stone [7]        | 3     |
| +22 → +24      | Stone [8]        | 3     |

### Somber weapons (Somber Stones, max +9)
- **1× Somber Stone[N] per upgrade level**: Somber Stone[1] for +1, Somber Stone[2] for +2, etc.

### 100% Guaranteed Pickup Rule
- **Only guaranteed world pickups count as collectible stone nodes** — glowing items on the ground
- **Random enemy drops are excluded** (e.g. Stormveil Castle soldiers have a chance to drop stones but it is not guaranteed — excluded)
- **Fallingstar Beast boss drops ARE 100%** — always drop a Somber Stone on kill
- **Mining tunnels (Limgrave Tunnels, Raya Lucaria Crystal Tunnel, Sellia Crystal Tunnel, etc.)** contain guaranteed pickups and are included
- Source: `poi_stones` in `square_data.json`, filtered to `access_tier = "direct"` (198 nodes total)

### Upgrades happen at Roundtable Hold
- Teleport to Roundtable from any grace (~30 seconds fixed overhead)
- Also costs runes (see `SMITHING_RUNE_COST` / `SOMBER_RUNE_COST` in `constants.py`)

---

## S6 Starting Graces (Fixed Pool of 13)

These are the 13 possible starting grace locations that are randomly assigned at the start of each run:

| Grace | Zone |
|-------|------|
| Gatefront Ruins | Limgrave |
| Inner Consecrated Snowfield | Consecrated Snowfield |
| Haligtree Roots | Haligtree |
| Snow Valley Ruins Overlook | Mountaintops |
| Inner Aeonia | Caelid |
| Ailing Village Outskirts | Limgrave |
| Scenic Isle | Liurnia |
| Ruined Labyrinth | Liurnia |
| Altus Highway Junction | Altus Plateau |
| Road of Iniquity | Mt. Gelmir |
| Lake of Rot Shoreside | Ainsel River (underground) |
| Siofra River Bank | Siofra River (underground) |
| Roundtable Hold | Roundtable (pocket dimension — fixed teleport cost) |

---

## Roundtable Hold

- **Always accessible** via fast travel from any grace (not a physical map location)
- Fixed teleport cost: **~30 seconds** regardless of current position
- **Free Sacred Seal pickup** — always available, always collected first visit (supports "Collect unique Seals" squares)
- **Upgrade station** — spend stones + runes to upgrade weapon
- Acts as an additional warp point once visited

---

## Flask Mechanics

- **Sacred Flask +N** squares: requires upgrading the flask to that level using Golden Seeds
- **10 Sacred Flask charges**: requires collecting enough Sacred Tears + Golden Seeds
- Starting charges: 4 (base game starting amount)

---

## Key Bingo Squares and Their Types

| Type | Description | Example |
|------|-------------|---------|
| `boss_specific` | Kill a specific boss with specific conditions | "Kill Godrick while summoning Nepheli" |
| `boss_any` | Kill one of several valid boss types | "Kill an Ancestor Spirit" |
| `boss_count` | Kill N bosses from a candidate pool | "Kill 4 Crucible Knights" |
| `boss_region` | Kill N bosses in a specific region | "Kill 6 bosses in Limgrave" |
| `boss_tag` | Kill N bosses matching a tag | "Kill 3 Dragon Heart bosses" |
| `acquire_count` | Collect N spells/items (includes vendor stops) | "Learn 12 sorceries" |
| `acquire_multi` | Collect specific items | "Acquire 10 Cracked Pots" |
| `restore_rune` | Restore a Great Rune at a Divine Tower | "Restore Godrick's Great Rune" |
| `dungeon_count` | Complete N dungeons of a type | "Complete 3 catacombs" |
| `passive_runes` | Passive — no active route needed | "Rune Level 60" |
| `passive_stat` | Passive — no active route needed | "30 Faith" |

---

## Zone Routing Model

Zones are ordered by difficulty/accessibility. The routing cost uses both zone penalty (accessibility) and zone speed (terrain):

| Zone | Tier | Penalty | Speed Mult |
|------|------|---------|-----------|
| Limgrave | 0 | 0.00 | 1.0× |
| Weeping Peninsula | 1 | 0.05 | 1.1× |
| Stormveil Castle | 1 | 0.05 | 2.5× (interior) |
| Siofra River | 2 | 0.15 | 2.0× (underground) |
| Liurnia | 3 | 0.15 | 1.1× |
| Caria Manor | 4 | 0.20 | 2.2× |
| Caelid | 4 | 0.20 | 1.1× |
| Dragonbarrow | 5 | 0.25 | 1.0× |
| Altus Plateau | 5 | 0.30 | 1.0× |
| Mt. Gelmir | 6 | 0.35 | 1.4× |
| Volcano Manor | 6 | 0.35 | 2.5× |
| Leyndell | 7 | 0.45 | 1.8× |
| Deeproot Depths | 7 | 0.45 | 2.2× |
| Ainsel River | 7 | 0.40 | 2.0× |
| Mohgwyn Palace | 8 | 0.55 | 2.0× |
| Mountaintops | 8 | 0.60 | 1.1× |
| Consecrated Snowfield | 9 | 0.65 | 1.1× |
| Haligtree | 10 | 0.70 | 2.8× |
| Farum Azula | 10 | 0.75 | 2.5× |

Travel base rate: **8.3 seconds per map unit** (calibrated from Gatefront→Margit ~75s).

---

## RL Agent Design (jack/rl/)

- **Algorithm**: MaskablePPO (sb3-contrib) — self-play against frozen snapshots
- **Action space**: 893 discrete locations (all square locations + 198 direct stone nodes + Roundtable)
- **Key constraint**: Routes are **fully learned** — the agent picks each stop one by one; no hardcoded routes
- **Opponent**: Frozen snapshot of past policy, updated every 50k timesteps
- Run training: `python -m jack.rl.train --timesteps 1_000_000`
- Evaluate: `python -m jack.rl.train --eval checkpoints/bingo_agent_final`

---

## Data Files

| File | Contents |
|------|----------|
| `jack/data/s6_base_bingo.json` | All 130 base bingo square templates with %num% variants |
| `jack/data/square_data.json` | Locations, types, boss HP, stone nodes (`poi_stones`), prerequisites for all squares |
| `jack/js/timing.js` | Boss HP, weapon DPS model, travel speed, upgrade costs |
| `jack/js/router.js` | Zone penalties, grace pools, route clustering, bingo line scoring |
| `jack/test/calc_square_times.py` | Python mirror of timing + router for offline analysis |
