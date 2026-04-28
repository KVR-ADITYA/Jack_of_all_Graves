"""Comprehensive square_data.json patch — applies all 60-item audit fixes."""
import json, copy

with open('jack/data/square_data.json', encoding='utf-8') as f:
    d = json.load(f)
sq = d['squares']

# ── #59: Remove duplicate talisman (typo "Sacrifial") ────────────────────────
sq.pop('Acquire 9 different Talismans (only 1 Sacrifial Twig)', None)

# ── #60: Remove duplicate Milicent square (keep "Millicent") ─────────────────
sq.pop('Kill the Milicent invader in Caelid', None)

# ── #57: Milicent invader needs NO prerequisites ──────────────────────────────
sq['Kill the Millicent invader in Caelid']['prerequisites'] = []
sq['Kill the Millicent invader in Caelid']['notes'] = (
    "Millicent invades in the Aeonia Swamp area of Caelid, "
    "near the Heart of Aeonia. No prerequisites needed."
)

# ── #7 / #21: Margit 6+ parries — remove Leyndell (no HP bar), not remembrance
sq['Kill Margit with 6+ parries']['locations'] = [
    loc for loc in sq['Kill Margit with 6+ parries']['locations']
    if 'Leyndell' not in loc.get('name', '')
]
sq['Kill Margit with 6+ parries']['remembrance'] = None

# ── #1: Godrick Nepheli — prereq kill Margit, note higher HP ─────────────────
sq['Kill Godrick while summoning Nepheli Loux']['prerequisites'] = ['kill_margit']
sq['Kill Godrick while summoning Nepheli Loux']['notes'] = (
    "Nepheli Loux summon sign outside Godrick's fog gate. Kill Margit first "
    "to access Stormveil. Godrick has higher HP when Nepheli is summoned."
)

# ── #2: Rennala — add prereqs ─────────────────────────────────────────────────
sq['Kill Rennala after she summons 4 spirits']['prerequisites'] = [
    'academy_glintstone_key', 'kill_red_wolf_of_radagon'
]
sq['Kill Rennala after she summons 4 spirits']['notes'] = (
    "Requires Academy Glintstone Key and defeating Red Wolf of Radagon. "
    "Phase 1: wait for Rennala to summon exactly 4 spirits before breaking her shield."
)

# ── #8: Red Wolf — add academy key prereq ─────────────────────────────────────
if 'Kill a Red Wolf Boss' in sq:
    locs = sq['Kill a Red Wolf Boss'].get('locations', sq['Kill a Red Wolf Boss'].get('candidates', []))
    for loc in locs:
        if 'Raya Lucaria' in loc.get('name', '') or 'Academy' in loc.get('name', ''):
            loc.setdefault('prerequisites', [])
            if 'academy_glintstone_key' not in loc.get('prerequisites', []):
                loc['prerequisites'] = ['academy_glintstone_key']

# ── #3: Radahn — add altus grace prereq ──────────────────────────────────────
sq['Kill Radahn without summoning NPCs']['prerequisites'] = ['rest_at_non_s6_altus_grace']
sq['Kill Radahn without summoning NPCs']['notes'] = (
    "Radahn Festival is triggered by resting at an Altus Plateau grace "
    "(the S6 starting grace at Altus Highway Junction does NOT trigger it — "
    "you must physically reach and rest at another Altus grace). "
    "Do not interact with any summon signs at the battlefield."
)

# ── #4: Morgott — add Godfrey Gold Spirit prereq ─────────────────────────────
sq['Kill Morgott']['prerequisites'] = ['capital_access', 'kill_godfrey_gold_spirit']
sq['Kill Morgott']['notes'] = (
    "Must defeat Godfrey's Golden Shade first (east of the Erdtree in Leyndell). "
    "Capital access requires: 2 Great Runes OR Fia's Champions quest."
)

# ── #5: Ancestor Spirit — clarify per-location prereqs ───────────────────────
sq['Kill an Ancestor Spirit']['notes'] = (
    "Ancestor Spirit (Siofra River) — no prerequisites. "
    "Regal Ancestor Spirit (Nokron) — requires Radahn dead (nokron_access) "
    "AND killing Mimic Tear in Nokron."
)

# ── #10: Fia's Champions — fix prereq (no cursemark needed) ──────────────────
sq["Kill Fia's Champions"]['prerequisites'] = ['deeproot_access']
sq["Kill Fia's Champions"]['notes'] = (
    "Deeproot Depths (via Siofra Aqueduct after killing Valiant Gargoyles). "
    "Does NOT require giving Cursemark of Death to Fia (that is needed for "
    "Fortissax). One of the hardest NPC boss fights in the game."
)

# ── #27: Alecto evergaol — add Astel Lake of Rot prereq ──────────────────────
evergaol = sq.get('Complete %num% evergaols', {})
for loc in evergaol.get('locations', []):
    if 'Alecto' in loc.get('name', ''):
        loc['prerequisites'] = ['kill_astel_lake_of_rot']
        loc['notes'] = "Ringleader's Evergaol (Moonlight Altar). Requires killing Astel, Naturalborn of the Void to unlock Moonlight Altar area."
        loc['zone'] = 'liurnia'

# ── #44 / #16: Lansseax — remove the Abandoned Coffin flee location ──────────
# Keep only "Rampartside Path" (x≈-95.88, y≈95.93)
def _remove_lansseax_flee(locations):
    return [
        loc for loc in locations
        if not ('Lansseax' in loc.get('name', '') and
                abs(loc.get('x', 0) - (-100.5625)) < 1.0 and
                abs(loc.get('y', 0) - 71.10258) < 1.0)
    ]

sq['Kill Lansseax']['locations'] = _remove_lansseax_flee(sq['Kill Lansseax']['locations'])
sq['Kill Lansseax']['notes'] = (
    "Ancient Dragon Lansseax at Rampartside Path, Altus Plateau. "
    "The other encounter (near Ruin-Strewn Precipice) has Lansseax fly away — "
    "does not count. Kill at Rampartside Path only."
)
sq['Kill Lansseax']['locations'][0]['zone'] = 'altus_plateau'

dh = sq.get('Kill %numofbosses% Dragon Heart bosses', {})
dh['locations'] = _remove_lansseax_flee(dh.get('locations', []))
if 'candidates' in dh:
    dh['candidates'] = _remove_lansseax_flee(dh['candidates'])

# ── #16: Dragon Hearts — add per-boss prereqs ────────────────────────────────
dh_notes_add = {
    'Fortissax': 'Requires: Fia quest (give Cursemark of Death to Fia at Deeproot Depths).',
    'Placidusax': 'Requires: lie down at the coffin in Crumbling Farum Azula (Beside the Great Bridge area).',
    'Adula': 'Glintstone Dragon Adula flees after ~30% HP at Three Sisters; must finish at Cathedral of Manus Celes. Requires killing Astel, Naturalborn of the Void to unlock Moonlight Altar.',
}
for loc in dh.get('locations', []) + dh.get('candidates', []):
    for key, note in dh_notes_add.items():
        if key in loc.get('name', ''):
            loc['notes'] = note

# ── #9: Godskin Apostle — fix wrong entries ───────────────────────────────────
apostle = sq.get('Kill a Godskin Apostle', {})
# Remove the Spiritcaller snail entry (not a Godskin Apostle fight)
# Remove the mountaintops zone entry with wrong coords (x=-76.5625, y=100.1641)
def _clean_apostle(locs):
    clean = []
    for loc in locs:
        name = loc.get('name', '')
        if 'Noble' in name and 'Apostle' not in name:
            continue  # skip Noble-only entries
        if 'Spiritcaller' in name:
            continue  # skip snail summon
        if abs(loc.get('x', 0) - (-76.5625)) < 0.1:
            # Fix the Windmill Village entry zone and coords
            loc['name'] = 'Godskin Apostle (Windmill Village, Altus Plateau)'
            loc['zone'] = 'altus_plateau'
            loc['x'] = -106.6
            loc['y'] = 83.8
        clean.append(loc)
    return clean

apostle['locations'] = _clean_apostle(apostle.get('locations', []))
apostle['notes'] = (
    "Caelid: Divine Tower of Caelid basement (accessible from Dragonbarrow). "
    "Altus Plateau: Windmill Village (field boss, no dungeon). "
    "Spiritcaller Cave summons do NOT count — those are phantoms from the snail boss."
)

# ── #14: Magma Wyrm — add Theodorix, fix notes ───────────────────────────────
magma = sq.get('Kill a Magma Wyrm boss', {})
# Add Theodorix if not present
theodorix_present = any('Theodorix' in l.get('name', '') for l in magma.get('locations', []))
if not theodorix_present:
    magma['locations'].append({
        "name": "Great Wyrm Theodorix",
        "x": -68.335937,
        "y": 149.168542,
        "level": 1,
        "zone": "consecrated"
    })
magma['notes'] = (
    "Gael Tunnel (Caelid border, easiest), Magma Wyrm Makar (Ruin-Strewn Precipice, drops Moonveil), "
    "Magma Wyrm (Volcano Manor area), Magma Wyrm (Mt. Gelmir lava pool, Seethewater Terminus), "
    "Great Wyrm Theodorix (Consecrated Snowfield). Note: Great Wyrm Theodorix is NOT in the Magma Wyrm "
    "square — it is in Dragon Hearts."
)

# ── #13: "God" bosses — remove Liurnia Divine Tower (not a boss) ─────────────
god_sq = sq.get('Kill 4 Bosses with the word God in it', {})
god_sq['candidates'] = [
    c for c in god_sq.get('candidates', [])
    if 'Divine Tower of Liurnia' not in c.get('name', '')
]
god_sq['notes'] = (
    "Candidates: Godrick, Godfrey (Gold Shade), Godfrey (Real/Hoarah Loux), Godefroy, "
    "God-Devouring Serpent/Rykard, Godskin Apostle, Godskin Noble (Volcano Manor only — "
    "Divine Tower of Liurnia version is NOT a boss), Godskin Duo, Soldier of Godrick. "
    "Pick any 4."
)

# ── #19: Horse bosses — remove Niall (not a horse) and Farum DTS (not a boss) ─
horse = sq.get('Kill 5 bosses that ride a horse', {})
horse['candidates'] = [
    c for c in horse.get('candidates', [])
    if 'Niall' not in c.get('name', '')
    and not ('Draconic Tree Sentinel' in c.get('name', '') and 'farum' in c.get('zone', '').lower())
]
horse['notes'] = (
    "Night's Cavalry (multiple locations, night only), Tree Sentinel (Limgrave, Leyndell gate), "
    "Tree Sentinel Duo (Leyndell gate — counts as 2), Draconic Tree Sentinel (Altus — counts), "
    "Starscourge Radahn, Commander O'Neil. "
    "Commander Niall does NOT ride a horse. Farum Azula Draconic Tree Sentinel is NOT a boss."
)

# ── #18: Duo/trio bosses — add prereqs + fix Valiant Gargoyle + add missing ───
duo = sq.get('Kill 3 duo/trio bosses', {})

# Add prereqs to Fell Twins
for c in duo.get('candidates', []):
    if 'Fell Twin' in c.get('name', ''):
        c['prerequisites'] = ['capital_access', 'kill_morgott']
        c['notes'] = 'Behind Divine Tower Bridge in Leyndell. Requires Morgott dead and capital access.'
    if 'Godskin Duo' in c.get('name', '') or ('Godskin' in c.get('name','') and 'Farum' in c.get('name','')):
        if c.get('zone') == 'farum_azula':
            c['prerequisites'] = ['kill_fire_giant']
            c['notes'] = 'Crumbling Farum Azula. Requires Fire Giant dead to progress.'
    if 'Valiant Gargoyle (Twinblade)' in c.get('name', ''):
        c['_remove'] = True
    if 'Valiant Gargoyle' in c.get('name', '') and 'Twinblade' not in c.get('name', ''):
        c['prerequisites'] = ['nokron_access']
        c['notes'] = 'Siofra Aqueduct (Nokron access required via Radahn).'

duo['candidates'] = [c for c in duo.get('candidates', []) if not c.pop('_remove', False)]

# Add missing: Misbegotten Warrior + Crucible Knight
already_has_misb_cru = any('Misbegotten' in c.get('name','') and 'Crucible' in c.get('name','')
                            for c in duo.get('candidates', []))
if not already_has_misb_cru:
    duo['candidates'].append({
        "name": "Misbegotten Warrior & Crucible Knight (Redmane Castle)",
        "x": -192.0, "y": 159.0, "level": 1, "zone": "caelid",
        "notes": "Redmane Castle, Caelid. Available once Radahn Festival is triggered."
    })

# Add Miranda + Omenkiller (Perfumer's Grotto)
already_has_miranda = any('Miranda' in c.get('name','') for c in duo.get('candidates', []))
if not already_has_miranda:
    duo['candidates'].append({
        "name": "Omenkiller & Miranda the Blighted Bloom (Perfumer's Grotto)",
        "x": -93.765625, "y": 60.524902, "level": 1, "zone": "mt_gelmir",
        "notes": "Perfumer's Grotto, Mt. Gelmir."
    })

# Add Abductor Virgin Duo
already_has_abductor = any('Abductor' in c.get('name','') for c in duo.get('candidates', []))
if not already_has_abductor:
    duo['candidates'].append({
        "name": "Abductor Virgin Duo (Volcano Manor)",
        "x": -85.476562, "y": 61.743591, "level": 1, "zone": "volcano_manor",
        "notes": "Subterranean Inquisition Chamber, Volcano Manor."
    })

# Add Beastman of Farum Azula Duo
already_has_beastman = any('Beastman' in c.get('name','') and 'Duo' in c.get('name','')
                            for c in duo.get('candidates', []))
if not already_has_beastman:
    duo['candidates'].append({
        "name": "Beastman of Farum Azula Duo (Dragonbarrow Cave)",
        "x": -150.59375, "y": 162.0, "level": 1, "zone": "dragonbarrow",
        "notes": "Dragonbarrow Cave."
    })

duo['notes'] = (
    "Fell Twins (Leyndell, needs Morgott + capital access), "
    "Nox Swordstress & Nox Priest (Sellia), Crucible Knight & Ordovis (Leyndell), "
    "Godskin Duo (Farum Azula, needs Fire Giant dead), Crystalian Trio (Sellia Hideaway), "
    "Cleanrot Knight Duo (Abandoned Cave), Valiant Gargoyles (Nokron, needs Radahn), "
    "Misbegotten Warrior + Crucible Knight (Redmane), Miranda + Omenkiller (Perfumer's Grotto), "
    "Abductor Virgin Duo (Volcano Manor), Beastman Duo (Dragonbarrow Cave)."
)

# ── #38: Scarseal — fix location (Siofra, NOT War-Dead area) ─────────────────
scarseal = sq.get('Acquire both Scarseal talismans', {})
for loc in scarseal.get('locations', []):
    if 'Radagon' in loc.get('name', ''):
        loc['x'] = -185.671875
        loc['y'] = 130.566475
        loc['level'] = 2
        loc['zone'] = 'siofra'
        loc['notes'] = 'On a corpse near the Dragonkin Soldier in Siofra River (underground).'
    if "Marika" in loc.get('name', ''):
        loc['zone'] = 'siofra'
        loc['prerequisites'] = ['nokron_access']
scarseal['notes'] = (
    "Radagon's Scarseal: Siofra River (underground, near Dragonkin Soldier — no prerequisites). "
    "Marika's Scarseal: Nokron, Eternal City (requires Radahn dead for nokron_access)."
)
scarseal['prerequisites'] = []  # Radagon's is free

# ── #23: Explosive physick — remove Exalted Flesh ────────────────────────────
physick = sq.get('Finish off a boss with the explosive physick', {})
physick['locations'] = [
    loc for loc in physick.get('locations', [])
    if 'Exalted' not in loc.get('name', '')
]
physick['notes'] = (
    "Obtain Flask of Wondrous Physick (Third Church of Marika) and mix with an "
    "explosive Crystal Tear (e.g. Flame-Shrouding Cracked Tear from Erdtree Avatars, "
    "or Cerulean Hidden Tear). Deal the killing blow to any boss using the physick burst."
)

# ── #24: Catacomb dungeon zones — fill all null zones ────────────────────────
zone_map = {
    'Stormfoot': 'limgrave', 'Tombsward': 'weeping_peninsula',
    'Deathtouched': 'limgrave', 'Murkwater': 'limgrave',
    "Impaler's": 'weeping_peninsula', 'Cliffbottom': 'liurnia',
    "Road's End": 'liurnia', 'Black Knife': 'liurnia',
    'Wyndham': 'altus_plateau', 'Unsightly': 'altus_plateau',
    'Minor Erdtree Catacombs': 'caelid', 'Caelid Catacombs': 'caelid',
    'War-Dead': 'caelid', 'Spiritcaller': 'mountaintops',
    'Giants\' Mountaintop': 'mountaintops', 'Giant-Conquering': 'mountaintops',
    'Mountaintop Catacombs': 'mountaintops', 'Consecrated Snowfield': 'consecrated',
    'Sainted Hero': 'altus_plateau', 'Gelmir Hero': 'mt_gelmir',
    'Azuria Hero': 'leyndell', 'Fringefolk': 'limgrave',
}
loc_zone_map = {
    'Limgrave Tunnels': 'limgrave', 'Morne Tunnel': 'weeping_peninsula',
    'Raya Lucaria Crystal Tunnel': 'liurnia', 'Academy Crystal Cave': 'liurnia',
    'Stillwater Cave': 'liurnia', 'Lakeside Crystal Cave': 'liurnia',
    'Earthbore Cave': 'weeping_peninsula', 'Tombsward Cave': 'weeping_peninsula',
    'Coastal Cave': 'limgrave', 'Highroad Cave': 'limgrave',
    'Groveside Cave': 'limgrave', 'Sage\'s Cave': 'altus_plateau',
    'Seethewater Cave': 'mt_gelmir', 'Volcano Cave': 'mt_gelmir',
    'Perfumer\'s Grotto': 'mt_gelmir', 'Gaol Cave': 'caelid',
    'Abandoned Cave': 'caelid', 'Sellia Hideaway': 'caelid',
    'Sellia Crystal Tunnel': 'caelid', 'Gael Tunnel': 'caelid',
    'Dragonbarrow Cave': 'dragonbarrow', 'Sellia Evergaol': 'caelid',
    'Cave of the Forlorn': 'consecrated', 'Yelough Anix Tunnel': 'consecrated',
    'Sealed Tunnel': 'altus_plateau', 'Old Altus Tunnel': 'altus_plateau',
    'Altus Tunnel': 'altus_plateau',
    'Ainsel River': 'ainsel', 'Nokstella': 'ainsel',
    'Deeproot': 'deeproot', 'Siofra': 'siofra', 'Nokron': 'siofra',
    'Ruin-Strewn Precipice': 'altus_plateau',
}

def _fix_zone(loc):
    if loc.get('zone') is not None:
        return
    name = loc.get('name', '')
    for key, zone in zone_map.items():
        if key in name:
            loc['zone'] = zone
            return
    for key, zone in loc_zone_map.items():
        if key in name:
            loc['zone'] = zone
            return

for key, data in sq.items():
    for loc in data.get('locations', []) + data.get('candidates', []):
        _fix_zone(loc)

# ── #26: Tunnels — add missing entries ───────────────────────────────────────
tunnel = sq.get('Complete %num% tunnel or precipice dungeons', {})
existing_tunnel_names = {l.get('name','') for l in tunnel.get('locations', [])}
new_tunnels = [
    {"name": "Stonedigger Troll (Limgrave Tunnels)", "x": -183.8, "y": 103.1, "level": 1, "zone": "limgrave"},
    {"name": "Stonedigger Troll (Old Altus Tunnel)", "x": -91.1, "y": 78.7, "level": 1, "zone": "altus_plateau"},
    {"name": "Crystalian Duo (Altus Tunnel)", "x": -85.5, "y": 80.2, "level": 1, "zone": "altus_plateau"},
    {"name": "Magma Wyrm Makar (Ruin-Strewn Precipice)", "x": -103.4375, "y": 75.798981, "level": 1, "zone": "altus_plateau"},
    {"name": "Demi-Human Chief Duo (Coastal Cave)", "x": -212.09375, "y": 108.671576, "level": 1, "zone": "limgrave"},
    {"name": "Beastman of Farum Azula (Groveside Cave)", "x": -190.195312, "y": 108.546562, "level": 1, "zone": "limgrave"},
]
for t in new_tunnels:
    if t['name'] not in existing_tunnel_names:
        tunnel.setdefault('locations', []).append(t)
tunnel['notes'] = (
    "Tunnels and Precipices contain smithing stones — very important for upgrades. "
    "Bosses: Limgrave Tunnels (Stonedigger Troll), Morne Tunnel (Scaly Misbegotten), "
    "Raya Lucaria Crystal Tunnel (Crystalian), Gael Tunnel (Magma Wyrm), "
    "Sellia Crystal Tunnel (Fallingstar Beast), Old Altus Tunnel (Stonedigger Troll), "
    "Altus Tunnel (Crystalian Duo), Ruin-Strewn Precipice (Magma Wyrm Makar), "
    "Sealed Tunnel (Onyx Lord), Yelough Anix Tunnel (Astel Stars of Darkness)."
)

# ── #51: NPC Bosses — add actual bosses ───────────────────────────────────────
npc_sq = sq.get('Kill 4 NPC Bosses', {})
npc_sq['locations'] = [
    {"name": "Patches (Murkwater Cave)", "x": -192.054687, "y": 108.039062, "level": 1, "zone": "limgrave",
     "notes": "Fight Patches after he ambushes you in Murkwater Cave. Spare him after to access his shop."},
    {"name": "Mimic Tear (Nokron)", "x": -184.914062, "y": 128.390623, "level": 2, "zone": "siofra",
     "notes": "Nokron, Eternal City. Requires Radahn dead (nokron_access). Unequip all gear before fog gate."},
    {"name": "Stray Mimic Tear (Hidden Path to the Haligtree)", "x": -81.64375, "y": 143.11789, "level": 1, "zone": "consecrated",
     "notes": "Hidden Path to the Haligtree, Consecrated Snowfield area."},
    {"name": "Roundtable Knight Vyke (Volcano Manor)", "x": -71.640625, "y": 168.464157, "level": 1, "zone": "mountaintops",
     "notes": "Lurnia of the Lakes adjacent (via Volcano Manor quest). Accessible via Ryke's questline."},
    {"name": "Esgar, Priest of Blood (Leyndell Sewers)", "x": -93.1875, "y": 114.777053, "level": 1, "zone": "leyndell",
     "prerequisites": ["capital_access"],
     "notes": "Leyndell Royal Capital sewers. Requires capital access."},
    {"name": "Bell-Bearing Hunter (Warmaster's Shack)", "x": -188.007812, "y": 110.531601, "level": 1, "zone": "limgrave",
     "notes": "Appears at night at Warmaster's Shack, Limgrave."},
]
npc_sq['notes'] = (
    "NPC bosses include: Patches (Murkwater Cave), Mimic Tear (Nokron), "
    "Stray Mimic Tear (Consecrated Snowfield), Roundtable Knight Vyke, "
    "Esgar Priest of Blood (Leyndell sewers, needs capital access), "
    "Bell-Bearing Hunters."
)

# ── #41: Friendly NPCs — remove Roderika (unkillable in this format) ──────────
friendly = sq.get('Kill 3 friendly NPCs (no hermit merchants)', {})
friendly['locations'] = [
    loc for loc in friendly.get('locations', [])
    if 'Roderika' not in loc.get('name', '')
]
# Add Yura if missing
has_yura = any('Yura' in l.get('name','') for l in friendly.get('locations', []))
if not has_yura:
    friendly['locations'].append({
        "name": "Bloody Finger Hunter Yura (Murkwater Cave area)",
        "x": -193.0, "y": 114.0, "level": 1, "zone": "limgrave",
        "notes": "Yura can be found near Murkwater Cave and later near the Raya Lucaria Main Academy Gate."
    })
has_blaidd = any('Blaidd' in l.get('name','') for l in friendly.get('locations', []))
if not has_blaidd:
    friendly['locations'].append({
        "name": "Blaidd (Mistwood Ruins / Ranni's Rise)",
        "x": -113.1875, "y": 50.56891, "level": 1, "zone": "liurnia",
        "notes": "Blaidd is found near Ranni's Rise after completing Ranni's quest or killing him there. Check if Rya/Boggart kill-lock applies before selecting."
    })
friendly['notes'] = (
    "Kill 3 friendly NPCs (not hermit merchants). Options include: Varre, Boc, Miriel, "
    "Yura, Blaidd, Iji, Millicent, Rogier, D, Nepheli, Rya, Boggart. "
    "Note: Roderika is unkillable. If squares exist for Rya or Boggart interactions, "
    "do NOT kill them before completing those squares."
)

# ── #52: Moon of Nokstella — remove prereqs ───────────────────────────────────
sq['Acquire Moon of Nokstella']['prerequisites'] = []
sq['Acquire Moon of Nokstella']['notes'] = (
    "Moon of Nokstella is in Ainsel River Main, close to the Lake of Rot Shoreside grace "
    "(an S6 starting grace). No prerequisites needed — short run from the grace."
)

# ── #50: Astel Lake of Rot — fix Ranni quest prereq ──────────────────────────
astel_sq = sq.get('Kill Astel and Astel, Stars of Darkness', {})
for b in astel_sq.get('bosses', []):
    if 'Naturalborn' in b.get('name', ''):
        b['prerequisites'] = []  # lake of rot grace available, no need for Ranni quest
        b['notes'] = 'Ainsel River Main / Grand Cloister. Lake of Rot Shoreside grace is S6 starting grace — no Ranni quest needed.'

# ── #49: Haligtree Medallion — per-piece prereqs ─────────────────────────────
hali = sq.get('Collect the full Haligtree Medallion', {})
for loc in hali.get('locations', []):
    if 'Left' in loc.get('name', ''):
        loc['prerequisites'] = ['kill_commander_niall']
        loc['notes'] = 'Castle Sol, Mountaintops of the Giants. Requires killing Commander Niall.'
    if 'Right' in loc.get('name', ''):
        loc['zone'] = 'liurnia'
        loc['notes'] = 'Given by Albus (disguised as jar) at Village of the Albinaurics, Liurnia. No prerequisites.'
hali['notes'] = (
    "Right half: Village of the Albinaurics, Liurnia (no prereqs). "
    "Left half: Castle Sol, Mountaintops — requires killing Commander Niall."
)

# ── #29: Ghost Glovewort BB [1] — add nokron_access prereq ───────────────────
gg1 = sq.get('Acquire Grave and Ghost Glovewort Bell Bearings [1]', {})
for loc in gg1.get('locations', []):
    if 'Ghost' in loc.get('name', ''):
        loc['prerequisites'] = ['nokron_access']
        loc['notes'] = 'Found in Siofra River / Nokron area. Requires Radahn dead for nokron_access.'
gg1['prerequisites'] = []  # Grave glovewort [1] is free

# ── #31: Mohg's Shackle — add capital_access ──────────────────────────────────
shackles = sq.get("Acquire Margit's and Mohg's Shackles", {})
shackles['locations'] = [
    {"name": "Margit's Shackle (Patches - Murkwater Cave)", "x": -192.054687, "y": 108.039062, "level": 1, "zone": "limgrave",
     "notes": "Buy from Patches in Murkwater Cave after sparing him."},
    {"name": "Mohg's Shackle (Leyndell Sewers)", "x": -93.65625, "y": 115.10, "level": 1, "zone": "leyndell",
     "prerequisites": ["capital_access"],
     "notes": "Found in the Leyndell Royal Capital sewers. Requires capital access."},
]
shackles['prerequisites'] = []
shackles['notes'] = (
    "Margit's Shackle: Patches at Murkwater Cave (buy after sparing him). "
    "Mohg's Shackle: Leyndell sewers (requires capital access)."
)

# ── #28: Bell bearing zones — fix all null zones ─────────────────────────────
bb_zone_hints = {
    'Wyndham': 'altus_plateau', 'Siofra': 'siofra', 'Ainsel': 'ainsel',
    'Nokron': 'siofra', 'Mohgwyn': 'mohgwyn', 'Mountaintops': 'mountaintops',
    'Caelid': 'caelid', 'Altus': 'altus_plateau', 'Liurnia': 'liurnia',
    'Limgrave': 'limgrave', 'Leyndell': 'leyndell', 'Mt. Gelmir': 'mt_gelmir',
    'Farum': 'farum_azula', 'Consecrated': 'consecrated', 'Haligtree': 'haligtree',
}
for key in ['Acquire Smithing-stone Bell Bearing [1] and [2]',
            'Acquire Somberstone Bell Bearing [1] and [2]',
            'Acquire Grave and Ghost Glovewort Bell Bearings [1]',
            'Acquire Grave and Ghost Glovewort Bell Bearings [2]']:
    if key not in sq:
        continue
    for loc in sq[key].get('locations', []):
        if loc.get('zone') is None:
            for hint, zone in bb_zone_hints.items():
                if hint in loc.get('name', ''):
                    loc['zone'] = zone
                    break

# ── #32: Rykard's Great Rune — add Sealed Tunnel prereq ─────────────────────
rykard_rune = sq.get("Restore Rykard's Great Rune", {})
rykard_rune['prerequisites'] = ['Kill Rykard, Lord of Blasphemy', 'kill_onyx_lord_sealed_tunnel']
rykard_rune['notes'] = (
    "Kill Rykard, then defeat Onyx Lord in the Sealed Tunnel (west Altus Plateau) "
    "to unlock the Divine Tower of West Altus gate. Restore at the tower."
)

# ── #39: Thops key — add red wolf prereq ──────────────────────────────────────
thops = sq.get("Return Thop's academy key", {})
thops['prerequisites'] = ['academy_glintstone_key', 'kill_red_wolf_of_radagon']
thops['notes'] = (
    "Give a spare Academy Glintstone Key to Thops at Church of Irith. "
    "The spare key is found in Raya Lucaria Academy (after killing Red Wolf of Radagon)."
)

# ── #40: Magnus — remove Varre's questline prereq ────────────────────────────
magnus = sq.get('Invade and defeat Magnus the Beast Claw', {})
magnus['prerequisites'] = []
magnus['notes'] = (
    "Magnus the Beast Claw invades at Writheblood Ruins on Altus Plateau. "
    "No questline prerequisites needed."
)

# ── #11: Grafted Scions — add missing locations ───────────────────────────────
grafted = sq.get('Kill %num% Grafted Scions', {})
existing_scion_names = {l.get('name','') for l in grafted.get('locations', [])}
new_scions = [
    {"name": "Grafted Scion (Fringefolk Hero's Grave)", "x": -199.1, "y": 100.6, "level": 1, "zone": "limgrave",
     "notes": "First fog gate of Fringefolk Hero's Grave (Stranded Graveyard)."},
    {"name": "Grafted Scion (Chapel of Anticipation, via Four Belfries)", "x": -230.4, "y": 70.2, "level": 1, "zone": "liurnia",
     "notes": "Access via the top-most waygate at the Four Belfries in Liurnia. Counts as Liurnia kill."},
    {"name": "Grafted Scion (Mt. Gelmir)", "x": -87.5, "y": 67.0, "level": 1, "zone": "mt_gelmir",
     "notes": "On the rocky terrain of Mt. Gelmir."},
]
for s in new_scions:
    if s['name'] not in existing_scion_names:
        grafted['locations'].append(s)
grafted['notes'] = (
    "Locations: Fringefolk Hero's Grave (first fog gate), Chapel of Anticipation (via Four Belfries — counts as Liurnia), "
    "Stormveil Castle, Liurnia of the Lakes (wandering), Mt. Gelmir."
)

# ── #15: Crucible Knights — add Stormveil + pre-Gargoyle instances ────────────
crucible = sq.get('Kill %numofbosses% Crucible Knights', {})
existing_cru = {l.get('name','') for l in crucible.get('locations', [])}
new_cru = [
    {"name": "Crucible Knight (Stormveil Castle)", "x": -176.25, "y": 87.5, "level": 1, "zone": "stormveil",
     "notes": "In a room near the grafted scion in Stormveil. Not a dungeon boss but still counts."},
    {"name": "Crucible Knight (Nokron, before Gargoyles)", "x": -169.3, "y": 132.1, "level": 2, "zone": "siofra",
     "prerequisites": ["nokron_access"],
     "notes": "Two Crucible Knights before the Valiant Gargoyle fog gate in Nokron. Both count individually."},
]
for c in new_cru:
    if c['name'] not in existing_cru:
        crucible['locations'].append(c)
crucible['notes'] = (
    "Stormhill Evergaol (Crucible Knight, Limgrave), Stormveil Castle (Crucible Knight), "
    "Auriza Hero's Grave (Ordovis duo, Leyndell), Redmane Castle (Misbegotten duo, Caelid), "
    "Nokron 2x (before Valiant Gargoyles, needs Radahn), Deeproot Depths (Siluria)."
)

# ── #54: Kill 2 Elder Lions — add locations ───────────────────────────────────
lions_key = 'Kill 2 Elder Lions'
if lions_key in sq:
    sq[lions_key]['locations'] = [
        {"name": "Lion Guardian (Stormveil Castle)", "x": -174.2, "y": 88.8, "level": 1, "zone": "stormveil",
         "notes": "In the main courtyard area of Stormveil Castle."},
        {"name": "Lion Guardian (Farum Azula - Dragon Temple)", "x": -124.5, "y": 218.5, "level": 1, "zone": "farum_azula",
         "notes": "Found in Crumbling Farum Azula near the Dragon Temple."},
        {"name": "Lion Guardian (Farum Azula - Altar)", "x": -122.8, "y": 215.3, "level": 1, "zone": "farum_azula",
         "notes": "Second Lion Guardian in Farum Azula."},
    ]
    sq[lions_key]['notes'] = (
        "Lion Guardians (Elder Lions) are found in Stormveil Castle and Crumbling Farum Azula."
    )

# ── #3 / Kill 3 Tree spirits — add zones, add non-boss spirits ───────────────
trees = sq.get('Kill 3 Tree spirits', {})
for loc in trees.get('locations', []):
    if loc.get('zone') is None:
        if 'Mt. Gelmir' in loc.get('name',''):
            loc['zone'] = 'mt_gelmir'
        elif 'Limgrave' in loc.get('name',''):
            loc['zone'] = 'limgrave'
        elif 'Giants' in loc.get('name',''):
            loc['zone'] = 'mountaintops'
        elif 'Putrid' in loc.get('name',''):
            loc['zone'] = 'caelid'
# Add underground tree spirit from Fringefolk if missing
existing_tree_names = {l.get('name','') for l in trees.get('locations', [])}
extra_trees = [
    {"name": "Ulcerated Tree Spirit (Fringefolk Hero's Grave)", "x": -199.0, "y": 100.3, "level": 1, "zone": "limgrave",
     "notes": "Inside Fringefolk Hero's Grave, Stranded Graveyard."},
    {"name": "Ulcerated Tree Spirit (Deeproot Depths)", "x": -87.1, "y": 107.0, "level": 2, "zone": "deeproot",
     "prerequisites": ["deeproot_access"],
     "notes": "Deeproot Depths — requires Valiant Gargoyles killed."},
]
for t in extra_trees:
    if t['name'] not in existing_tree_names:
        trees['locations'].append(t)
trees['notes'] = (
    "Includes any Ulcerated or Putrid Tree Spirit, boss or otherwise. "
    "Non-boss instances (Fringefolk, Deeproot) also count."
)

# ── Godfrey Gold Spirit prereq is already noted in Morgott ───────────────────
# Also add him explicitly to the "God" bosses with the morgott prereq note
for c in god_sq.get('candidates', []):
    if 'Golden Shade' in c.get('name','') or 'Gold Spirit' in c.get('name',''):
        c['prerequisites'] = ['capital_access']
        c['notes'] = 'Gold phantom in Leyndell. Requires capital access. Must kill before Morgott.'

# ── Gurranq — fix zone ────────────────────────────────────────────────────────
for loc in sq.get('Kill Gurranq', {}).get('locations', []):
    if loc.get('zone') is None:
        loc['zone'] = 'dragonbarrow'

# ── Bell bearing zones on smithing/somber ─────────────────────────────────────
for loc in sq.get('Acquire Smithing-stone Bell Bearing [1] and [2]', {}).get('locations', []):
    if loc.get('zone') is None:
        if abs(loc.get('x',0) - (-124.310938)) < 1:
            loc['zone'] = 'liurnia'  # Raya Lucaria Crystal Tunnel area
        elif abs(loc.get('x',0) - (-105.515625)) < 1:
            loc['zone'] = 'leyndell'  # Leyndell area

for loc in sq.get('Acquire Somberstone Bell Bearing [1] and [2]', {}).get('locations', []):
    if loc.get('zone') is None:
        if abs(loc.get('y',0) - 145.606806) < 1:
            loc['zone'] = 'mohgwyn'  # Mohgwyn area
        elif abs(loc.get('y',0) - 91.6) < 1:
            loc['zone'] = 'altus_plateau'

# ── Save ──────────────────────────────────────────────────────────────────────
with open('jack/data/square_data.json', 'w', encoding='utf-8') as f:
    json.dump(d, f, indent=2, ensure_ascii=False)
print("Done. Squares count:", len(sq))
