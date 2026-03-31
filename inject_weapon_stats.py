#!/usr/bin/env python3
"""
inject_weapon_stats.py — Inject real weapon stats into global.ini descriptions.

Reads fps-items.json from scunpacked and patches the description lines in
global.ini so they show accurate DPS, alpha, penetration, etc.

Sources:
  --source scunpacked (default): stats from scunpacked fps-items.json
  --source tested: stats from tested spreadsheet CSVs (tab_Item.csv),
                   with only penetration data from scunpacked

Usage:
    python inject_weapon_stats.py [--version 4.7.0-LIVE_11545720] [--dry-run]
    python inject_weapon_stats.py --source tested [--dry-run]
"""

import argparse
import csv
import json
import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
VERSIONS_DIR = BASE_DIR / "versions"

# Header prefixes — lines that belong to the "header" section of a description
# All comparisons are done case-insensitive (see _startswith_any)
HEADER_PREFIXES = (
    "fabricante:",
    "tipo de artículo:",
    "tipo de articulo:",
    "tipo de ítem:",
    "tipo de item:",
    "clase:",
    "tamaño:",
    "item type:",
    "manufacturer:",
    "class:",
    "size:",
    "attachment",
    "attachments:",
    "accesorios:",
    "accesorio:",
    "acoples:",
    "tamaño del cargador:",
    "tamaño de cargador:",
    "tamaño de la bateria:",
    "tamaño de la batería:",
    "tamaño de bateria:",
    "tamaño de batería:",
    "capacidad del cargador:",
    "magazine size:",
    "battery size:",
)

# Old stats prefixes — CIG's descriptive stats to replace
# Only cadencia/alcance — NOT cargador/batería (those stay)
# All comparisons are done case-insensitive
OLD_STATS_PREFIXES = (
    "cadencia de fuego:",
    "cadencia de tiro:",
    "cadencia de disparo:",
    "alcance efectivo:",
    "alcance eficaz:",
    "rate of fire:",
    "effective range:",
    "tasa de fuego:",
    "tasa de disparo:",
    "tasa de flujo:",
    "velocidad de disparo:",
    "velocidad de incendio:",
    "rango efectivo:",
)

# Also match our own previously-injected stats so re-runs update them
OWN_STATS_PREFIXES = (
    "DPS:",
    "Alpha:",
    "Dmg/Cargador:",
    "Vel. Proyectil:",
    "Penetración:",
    "Daño completo:",
    "Caída daño:",
    "Cero daño:",
)

DAMAGE_LABELS = {
    "Physical": "Físico",
    "Energy": "Energía",
    "Distortion": "Distorsión",
    "Thermal": "Térmico",
    "Biochemical": "Bioquímico",
    "Stun": "Aturdimiento",
}

# Manual overrides for weapons with complex mechanics that scunpacked can't parse.
# Calculated from individual JSONs in items_beam/.
MANUAL_OVERRIDES = {
    # Parallax: hybrid projectile(210 DPS)->beam(260 DPS)
    "volt_rifle_energy_01": {
        "category": "custom",
        "stats_line": "DPS: 210-260 | Alpha: 21\\nDmg/Cargador: 1680 | Vel. Proyectil: 600 m/s\\nPenetración: 0.5m",
    },
    # Fresnel: sequence x3 barrels, heat ramp (RPM baja, alpha sube)
    "volt_lmg_energy_01": {
        "category": "energy",
        "DpsTotal": 82.5, "AlphaTotal": 9,
        "Dps": {"Physical": 0, "Energy": 82.5, "Distortion": 0},
        "MaxPerMag": 1485, "Speed": 1100, "Penetration": 0.3,
    },
    # Prism: heat ramp, 200-450 rpm, 5.75 dmg/shot
    "volt_shotgun_energy_01": {
        "category": "custom",
        "stats_line": "DPS: 19.2-43.1 | Alpha: 5.8\\nDmg/Cargador: 115 | Vel. Proyectil: 300 m/s",
    },
    # Tripledown: parallel x3 barrels, 12 dmg * 3 * 60 rpm / 60
    "none_pistol_ballistic_01": {
        "category": "ballistic",
        "DpsTotal": 36, "AlphaTotal": 36,
        "Dps": {"Physical": 36, "Energy": 0, "Distortion": 0},
        "MaxPerMag": 432, "Speed": 550, "Penetration": 0.5,
        "DamageDropDist": 10,
    },
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def fmt_num(v):
    """Format a number: integer if whole, else 1 decimal."""
    if v is None:
        return "0"
    if isinstance(v, float) and v != int(v):
        return f"{v:.1f}"
    return str(int(v))


def fmt_k(v):
    """Format a number with K suffix for values >= 1000. For DPS, Alpha, Dmg/Cargador."""
    if v is None:
        return "0"
    if isinstance(v, str):
        try:
            v = float(v)
        except ValueError:
            return v
    if abs(v) >= 1000:
        k = v / 1000
        rounded = round(k, 1)
        if rounded == int(rounded):
            return f"{int(rounded)}K"
        return f"{rounded:.1f}K"
    if isinstance(v, float) and v != int(v):
        return f"{v:.1f}"
    return str(int(v))


def detect_latest_version():
    """Return the most recently modified version directory name."""
    if not VERSIONS_DIR.is_dir():
        return None
    versions = [d for d in VERSIONS_DIR.iterdir() if d.is_dir()]
    if not versions:
        return None
    # Sort by modification time, newest first
    versions.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return versions[0].name


def get_damage_drop_distance(ammo):
    """Get the first non-zero DamageDropMinDistance value."""
    drop = ammo.get("DamageDropMinDistance", {})
    if not drop:
        return 0
    for key in ("Physical", "Energy", "Distortion", "Thermal", "Biochemical", "Stun"):
        v = drop.get(key, 0)
        if v and v > 0:
            return v
    return 0


def get_pellets(weapon_data):
    """Get PelletsPerShot from the first fire mode, default 1."""
    modes = weapon_data.get("Modes", [])
    if modes:
        return modes[0].get("PelletsPerShot", 1) or 1
    return weapon_data.get("PelletsPerShot", 1) or 1


def build_damage_label(dps_dict, alpha_dict):
    """Build the damage type label based on which types have DPS > 0."""
    active = {}
    for key, label in DAMAGE_LABELS.items():
        v = dps_dict.get(key, 0) or 0
        if v > 0:
            active[label] = v
    return active


def classify_weapon(item):
    """
    Classify a weapon into a category for stat formatting.
    Returns: 'beam', 'shotgun', 'ballistic', 'energy', 'mixed', 'launcher', or None to skip.
    """
    si = item.get("stdItem", {})
    weapon = si.get("Weapon", {})
    damage = weapon.get("Damage", {})
    ammo = si.get("Ammunition", {})
    beam = si.get("BeamData")

    dps_total = damage.get("DpsTotal") or 0
    alpha_total = damage.get("AlphaTotal") or 0
    dps_dict = damage.get("Dps", {})

    # Beam weapons
    if beam and (beam.get("FullDamageRange", 0) > 0 or beam.get("ZeroDamageRange", 0) > 0):
        if dps_total > 0:
            return "beam"

    if dps_total <= 0:
        return None

    # Count active damage types
    active_types = {k: v for k, v in dps_dict.items() if (v or 0) > 0}

    # Shotgun (check before launcher — shotguns have high alpha due to pellets)
    pellets = get_pellets(weapon)
    if pellets > 1:
        return "shotgun"

    # Launcher / Railgun: very high alpha, single damage type
    if alpha_total > 100 and len(active_types) <= 1:
        return "launcher"

    # Mixed damage
    if len(active_types) >= 2:
        return "mixed"

    # Ballistic vs Energy
    drop_dist = get_damage_drop_distance(ammo)
    if drop_dist > 0:
        return "ballistic"

    # Check if physical damage
    if (dps_dict.get("Physical") or 0) > 0:
        return "ballistic"

    return "energy"


def build_stats_block(item, category):
    """Build the stats lines for a weapon."""
    si = item.get("stdItem", {})
    weapon = si.get("Weapon", {})
    damage = weapon.get("Damage", {})
    ammo = si.get("Ammunition", {})
    beam = si.get("BeamData")

    dps_total = damage.get("DpsTotal") or 0
    alpha_total = damage.get("AlphaTotal") or 0
    max_per_mag = damage.get("MaxPerMag") or 0
    dps_dict = damage.get("Dps", {})
    alpha_dict = damage.get("Alpha", {})

    speed = ammo.get("Speed", 0) or 0
    penetration = ammo.get("MaxPenetrationThickness", 0) or 0
    drop_dist = get_damage_drop_distance(ammo)
    pellets = get_pellets(weapon)

    # Detect burst fire mode
    is_burst = False
    modes = weapon.get("Modes", [])
    if modes:
        fire_type = modes[0].get("FireType", "")
        if fire_type == "burst":
            is_burst = True

    # Sanitize absurd penetration values (data errors in scunpacked)
    # P4-AR: 5000m, Prism: 20m — clearly wrong
    if penetration > 10:
        penetration = 0

    active_dps = build_damage_label(dps_dict, alpha_dict)
    lines = []
    burst_tag = " (burst)" if is_burst else ""

    if category == "beam":
        # DPS line with breakdown
        if len(active_dps) == 1:
            label = list(active_dps.keys())[0]
            lines.append(f"DPS: {fmt_num(dps_total)} ({label})")
        else:
            parts = [f"{fmt_num(v)} {k}" for k, v in active_dps.items()]
            lines.append(f"DPS: {fmt_num(dps_total)} ({' + '.join(parts)})")
        full_range = beam.get("FullDamageRange", 0) or 0
        zero_range = beam.get("ZeroDamageRange", 0) or 0
        lines.append(f"Daño completo: 0-{fmt_num(full_range)}m | Cero daño: {fmt_num(zero_range)}m")

    elif category == "shotgun":
        if len(active_dps) >= 2:
            parts = [f"{fmt_num(v)} {k}" for k, v in active_dps.items()]
            lines.append(f"DPS: {fmt_num(dps_total)}{burst_tag} ({' + '.join(parts)}) | Alpha: {fmt_num(alpha_total)} | {pellets} perdigones")
        else:
            lines.append(f"DPS: {fmt_num(dps_total)}{burst_tag} | Alpha: {fmt_num(alpha_total)} | {pellets} perdigones")
        lines.append(f"Dmg/Cargador: {fmt_num(max_per_mag)} | Vel. Proyectil: {fmt_num(speed)} m/s")
        extras = []
        if 0 < penetration <= 10:
            extras.append(f"Penetración: {fmt_num(penetration)}m")
        if drop_dist > 0:
            extras.append(f"Caída daño: desde {fmt_num(drop_dist)}m")
        if extras:
            lines.append(" | ".join(extras))

    elif category == "ballistic":
        lines.append(f"DPS: {fmt_num(dps_total)}{burst_tag} | Alpha: {fmt_num(alpha_total)}")
        lines.append(f"Dmg/Cargador: {fmt_num(max_per_mag)} | Vel. Proyectil: {fmt_num(speed)} m/s")
        extras = []
        if penetration > 0:
            extras.append(f"Penetración: {fmt_num(penetration)}m")
        if drop_dist > 0:
            extras.append(f"Caída daño: desde {fmt_num(drop_dist)}m")
        if extras:
            lines.append(" | ".join(extras))

    elif category == "energy":
        lines.append(f"DPS: {fmt_num(dps_total)}{burst_tag} | Alpha: {fmt_num(alpha_total)}")
        lines.append(f"Dmg/Cargador: {fmt_num(max_per_mag)} | Vel. Proyectil: {fmt_num(speed)} m/s")
        if penetration > 0:
            lines.append(f"Penetración: {fmt_num(penetration)}m")

    elif category == "mixed":
        parts = [f"{fmt_num(v)} {k}" for k, v in active_dps.items()]
        lines.append(f"DPS: {fmt_num(dps_total)} ({' + '.join(parts)})")
        lines.append(f"Alpha: {fmt_num(alpha_total)} | Dmg/Cargador: {fmt_num(max_per_mag)}")
        lines.append(f"Vel. Proyectil: {fmt_num(speed)} m/s | Penetración: {fmt_num(penetration)}m")

    elif category == "launcher":
        lines.append(f"DPS: {fmt_num(dps_total)}{burst_tag} | Alpha: {fmt_num(alpha_total)}")
        lines.append(f"Dmg/Cargador: {fmt_num(max_per_mag)} | Vel. Proyectil: {fmt_num(speed)} m/s")
        lines.append(f"Penetración: {fmt_num(penetration)}m")

    return "\\n".join(lines)


def _startswith_any(text, prefixes):
    """Case-insensitive check if text starts with any of the prefixes."""
    lower = text.lower()
    return any(lower.startswith(p) for p in prefixes)


def parse_description(desc):
    """
    Parse a weapon description into (header_lines, old_stats_lines, flavor_text).
    Lines are separated by literal '\\n' in the ini value.
    """
    parts = desc.split("\\n")

    header = []
    old_stats = []
    flavor_parts = []
    section = "header"  # header -> stats -> flavor

    for part in parts:
        stripped = part.strip()

        if section == "header":
            if stripped == "":
                continue  # skip blank lines (will be compacted)
            is_header = _startswith_any(stripped, HEADER_PREFIXES)
            is_old_stat = _startswith_any(stripped, OLD_STATS_PREFIXES)
            is_own_stat = any(stripped.startswith(p) for p in OWN_STATS_PREFIXES)

            if is_header:
                header.append(part)
            elif is_old_stat or is_own_stat:
                section = "stats"
                old_stats.append(part)
            else:
                # No stats found, this is already flavor text
                section = "flavor"
                flavor_parts.append(part)
        elif section == "stats":
            is_old_stat = _startswith_any(stripped, OLD_STATS_PREFIXES)
            is_own_stat = any(stripped.startswith(p) for p in OWN_STATS_PREFIXES)
            is_header = _startswith_any(stripped, HEADER_PREFIXES)
            if is_old_stat or is_own_stat:
                old_stats.append(part)
            elif is_header:
                header.append(part)
            elif stripped == "":
                # Empty line — skip it (will be compacted later)
                continue
            else:
                section = "flavor"
                flavor_parts.append(part)
        elif section == "flavor":
            flavor_parts.append(part)

    # Clean up: simplify "Clase: energía (Laser)" -> "Clase: Laser"
    for i, h in enumerate(header):
        m = re.match(r'^(Clase:\s*)(?:[Ee]nerg[ií]a\s*\((.+?)\))(.*)$', h)
        if m:
            header[i] = m.group(1) + m.group(2) + m.group(3)

    # Clean up: remove trailing empty strings from header
    while header and header[-1].strip() == "":
        header.pop()

    # Clean up: remove leading empty strings from flavor
    while flavor_parts and flavor_parts[0].strip() == "":
        flavor_parts.pop(0)

    header_str = "\\n".join(header)
    flavor_str = "\\n".join(flavor_parts)

    return header_str, old_stats, flavor_str


def rebuild_description(header_str, stats_block, flavor_str):
    """Rebuild the full description value. Compact: no blank lines except before flavor."""
    # Remove any blank lines within header
    header_lines = [l for l in header_str.split("\\n") if l.strip() != ""]
    top = "\\n".join(header_lines)
    if stats_block:
        top += "\\n" + stats_block
    if flavor_str:
        return top + "\\n\\n" + flavor_str
    return top


# ---------------------------------------------------------------------------
# Tested source: load stats from spreadsheet CSV
# ---------------------------------------------------------------------------

# Category headers in the CSV to skip
EXCEL_CATEGORY_HEADERS = {
    "ASSAULT RIFLE", "LMG", "PISTOL", "SHOTGUN", "SMG", "SNIPER RIFLE",
    "HEAVY / MOUNTED", "GRENADE", "GADGET", "GRENADE LAUNCHER", "RAILGUN",
    "MOUNTED GUN", "ROCKET LAUNCHER",
}


def _parse_csv_float(val):
    """Parse a CSV numeric value, handling commas and empty strings."""
    if not val or not val.strip():
        return 0.0
    return float(val.strip().replace(",", ""))


def _build_scunpacked_name_map(fps_items):
    """
    Build a mapping from simplified display name -> base className.

    From scunpacked fps-items.json, extract WeaponPersonal items,
    strip quoted skin names from stdItem.Name, normalize nbsp,
    and pick the shortest className (base variant) for each name.
    """
    from collections import defaultdict
    name_to_cns = defaultdict(list)

    for item in fps_items:
        if item.get("type") != "WeaponPersonal":
            continue
        cn = item.get("className", "")
        name = item.get("stdItem", {}).get("Name", "")
        if not name or "PLACEHOLDER" in name:
            continue
        # Remove quoted skin suffix: "Rager", "Boneyard", etc.
        simplified = re.sub(r'"[^"]*"\s*', '', name).strip()
        # Normalize non-breaking spaces
        simplified = simplified.replace('\xa0', ' ')
        name_to_cns[simplified.lower()].append(cn)

    # For each name, pick the shortest className (base variant without skin suffix)
    name_map = {}
    for sname, cns in name_to_cns.items():
        cns.sort(key=len)
        name_map[sname] = cns[0]

    return name_map


def _build_penetration_map(fps_items):
    """Build className -> MaxPenetrationThickness from scunpacked data."""
    pen_map = {}
    for item in fps_items:
        if item.get("type") != "WeaponPersonal":
            continue
        cn = item.get("className", "").lower()
        ammo = item.get("stdItem", {}).get("Ammunition", {})
        pen = ammo.get("MaxPenetrationThickness", 0) or 0
        if pen > 100:
            pen = 0  # Sanitize absurd values
        if pen > 0:
            pen_map[cn] = pen
    return pen_map


def _match_excel_name(excel_name, name_map):
    """
    Try to match an Excel weapon name to a scunpacked className.

    First tries exact match, then tries matching with common extra words
    removed (Energy, Laser, Energy Assault, etc.).
    """
    key = excel_name.lower()

    # Collect all matches (exact + variants), pick shortest className
    candidates = []
    if key in name_map:
        candidates.append(name_map[key])

    # Try adding common prefixes/infixes that scunpacked uses
    # e.g., "Fresnel LMG" -> "Fresnel Energy LMG"
    #        "Prism Shotgun" -> "Prism Laser Shotgun"
    #        "Parallax Rifle" -> "Parallax Energy Assault Rifle"
    #        "Pulse Pistol" -> "Pulse Laser Pistol"
    variants = []
    words = key.split()
    if len(words) >= 2:
        base = words[0]
        weapon_type = words[-1]
        # Try "Base Energy Type", "Base Laser Type", "Base Energy Assault Type"
        for infix in ["energy", "laser", "energy assault"]:
            variant = f"{base} {infix} {weapon_type}"
            variants.append(variant)
        # Try "Base Laser Type" for compound names like "Pulse Pistol"
        # Also try just the first word + type with all known infixes
    for v in variants:
        if v in name_map:
            candidates.append(name_map[v])

    if not candidates:
        return None
    # Pick shortest className (base variant)
    candidates.sort(key=len)
    return candidates[0]


def classify_weapon_tested(fire_mode, pellets, alpha, dps_sustained, dps_burst, drop_dist):
    """
    Classify a weapon from tested/Excel data.

    Returns: 'beam', 'shotgun', 'ballistic', 'energy', 'launcher', or None.
    """
    mode_lower = fire_mode.lower()

    if "beam" in mode_lower:
        return "beam"

    if "charge" in mode_lower and alpha > 100:
        return "launcher"

    if pellets > 1:
        return "shotgun"

    if drop_dist > 0:
        return "ballistic"

    return "energy"


def _fire_mode_label(mode_str):
    """Convert raw fire mode string to a clean label."""
    ml = mode_str.lower().strip()
    if "charge burst" in ml:
        return "Full"
    if "charge" in ml:
        return "Full"
    if "combined s" in ml:
        return "Hot"  # combined slug mode = hot (Prism)
    if "combined" in ml:
        return "Auto"  # combined damage types = auto mode
    if "heat 50%" in ml or "hot" in ml:
        return "Hot"
    if ml.startswith("rapid") or ml.startswith("auto"):
        return "Auto"
    if ml.startswith("single") or ml.startswith("semi"):
        return "Semi"
    if "burst 5" in ml:
        return "Burst5"
    if "burst 3" in ml or ml.startswith("burst"):
        return "Burst"
    if "rapid burst" in ml:
        return "Burst"
    if ml.startswith("beam"):
        return "Beam"
    if ml.startswith("slug"):
        return "Slug"
    if ml.startswith("double"):
        return "Doble"
    return ml.split()[0].capitalize()


def build_stats_block_tested(item, category):
    """
    Build stats block for tested source data.

    Format: one line per fire mode with label, then shared stats lines.
    """
    si = item.get("stdItem", {})
    weapon = si.get("Weapon", {})
    damage = weapon.get("Damage", {})
    ammo = si.get("Ammunition", {})

    dps_total = damage.get("DpsTotal") or 0
    alpha_total = damage.get("AlphaTotal") or 0
    max_per_mag = damage.get("MaxPerMag") or 0
    speed = ammo.get("Speed", 0) or 0
    penetration = ammo.get("MaxPenetrationThickness", 0) or 0
    if penetration > 10:
        penetration = 0
    drop_dist = get_damage_drop_distance(ammo)

    # Get all modes from item
    all_modes = item.get("_all_modes", [])

    lines = []

    if all_modes and len(all_modes) >= 1:
        for m in all_modes:
            label = _fire_mode_label(m["mode"])
            if label is None:
                continue
            m_speed = m.get("speed", 0) or 0
            m_range = m.get("range", 0) or 0
            parts = [f"[{label}] DPS: {fmt_k(m['dps_sus'])} | Alpha: {fmt_k(m['alpha'])}"]
            if m_speed > 0:
                parts.append(f"{fmt_num(m_speed)} m/s")
            if m_range > 0:
                parts.append(f"{fmt_num(m_range)}m")
            lines.append(" | ".join(parts))
    else:
        fire_mode = weapon.get("FireMode", "")
        label = _fire_mode_label(fire_mode) or "Auto"
        parts = [f"[{label}] DPS: {fmt_k(dps_total)} | Alpha: {fmt_k(alpha_total)}"]
        if speed > 0:
            parts.append(f"{fmt_num(speed)} m/s")
        ammo_range = ammo.get("Range", 0) or 0
        if ammo_range > 0:
            parts.append(f"{fmt_num(ammo_range)}m")
        lines.append(" | ".join(parts))

    # Shared stats: Mass | Dmg/Cargador
    mass = si.get("Mass", 0) or 0
    mass_parts = []
    if mass > 0:
        mass_parts.append(f"{fmt_num(mass)} kg")
    if max_per_mag > 0:
        mass_parts.append(f"Dmg/Cargador: {fmt_k(max_per_mag)}")
    if mass_parts:
        lines.append(" | ".join(mass_parts))

    # Shared stats: Penetración | Caída daño
    extras3 = []
    if 0 < penetration <= 10:
        extras3.append(f"Penetración: {fmt_num(penetration)}m")
    if drop_dist > 0:
        extras3.append(f"Caída daño: desde {fmt_num(drop_dist)}m")
    if extras3:
        lines.append(" | ".join(extras3))

    return "\\n".join(lines)


def load_tested_weapons(version_dir, fps_items):
    """
    Load weapon stats from tested spreadsheet CSV.

    Returns: dict of className -> (item_dict, category, stats_block)
    """
    csv_path = version_dir / "sources" / "tested" / "sin_crafteo" / "tab_Item.csv"
    if not csv_path.is_file():
        print(f"ERROR: {csv_path} not found.", file=sys.stderr)
        sys.exit(1)

    print(f"CSV: {csv_path}")

    # Build name mapping and penetration data from scunpacked
    name_map = _build_scunpacked_name_map(fps_items)
    pen_map = _build_penetration_map(fps_items)

    # Parse CSV: group rows by weapon (sub-rows have empty col 0)
    raw_weapons = []  # list of (name, [(row_data), ...])
    current_name = None
    current_rows = []

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # skip header

        for row in reader:
            if len(row) < 20:
                continue

            name = row[0].strip().replace('\xa0', ' ')

            if name:
                # Check if it's a category header
                if name in EXCEL_CATEGORY_HEADERS:
                    # Save previous weapon if any
                    if current_name and current_rows:
                        raw_weapons.append((current_name, current_rows))
                    current_name = None
                    current_rows = []
                    continue

                # Check if it looks like a sub-header row (all 1's or empty DPS)
                dps_val = row[19].strip() if len(row) > 19 else ''
                fire_mode = row[7].strip() if len(row) > 7 else ''
                if not fire_mode or dps_val in ('', '1'):
                    # Sub-header or separator row
                    if current_name and current_rows:
                        raw_weapons.append((current_name, current_rows))
                    current_name = None
                    current_rows = []
                    continue

                # New weapon
                if current_name and current_rows:
                    raw_weapons.append((current_name, current_rows))
                current_name = name
                current_rows = [row]
            else:
                # Sub-row (alternate fire mode)
                if current_name:
                    current_rows.append(row)

        # Don't forget last weapon
        if current_name and current_rows:
            raw_weapons.append((current_name, current_rows))

    # Process each weapon: select best fire mode
    weapons = {}
    skipped_zero_dps = 0
    skipped_no_match = 0
    matched = 0

    for weapon_name, rows in raw_weapons:
        # Parse all modes for this weapon
        parsed_modes = []
        weapon_mass = 0  # mass from first row, propagate to sub-rows
        for row in rows:
            fm = row[7].strip() if len(row) > 7 else ''
            if not fm:
                continue
            try:
                dps_s = _parse_csv_float(row[19]) if len(row) > 19 and row[19].strip() else 0
            except ValueError:
                continue
            try:
                dps_b = _parse_csv_float(row[20]) if len(row) > 20 and row[20].strip() else 0
            except ValueError:
                dps_b = 0
            try:
                a = _parse_csv_float(row[16]) if len(row) > 16 and row[16].strip() else 0
            except ValueError:
                a = 0
            pel = int(_parse_csv_float(row[12])) if len(row) > 12 and row[12].strip() else 1
            if pel < 1:
                pel = 1
            m_speed = _parse_csv_float(row[8]) if len(row) > 8 else 0
            m_range = _parse_csv_float(row[10]) if len(row) > 10 else 0
            m_mass = _parse_csv_float(row[5]) if len(row) > 5 and row[5].strip() else 0
            if m_mass > 0:
                weapon_mass = m_mass  # first row sets the mass
            parsed_modes.append({"row": row, "mode": fm, "dps_sus": dps_s, "dps_burst": dps_b, "alpha": a, "pellets": pel, "speed": m_speed, "range": m_range, "mass": weapon_mass})

        if not parsed_modes:
            skipped_zero_dps += 1
            continue

        # Detect multi-mode type and select primary/secondary
        mode_types = [m["mode"].lower() for m in parsed_modes]
        has_combined = any("combined" in mt for mt in mode_types)
        has_heat = any("heat 50%" in mt for mt in mode_types)
        has_charge = any("charge" in mt for mt in mode_types)

        # Force heat detection for weapons with slug->pellet heat ramp (Prism)
        if not has_heat and "slug" in mode_types and len(parsed_modes) >= 2:
            has_heat = True

        # Select primary mode
        if has_combined:
            primary = next(m for m in parsed_modes if "combined" in m["mode"].lower())
        else:
            primary = max(parsed_modes, key=lambda m: m["dps_sus"])

        if primary["dps_sus"] <= 0:
            skipped_zero_dps += 1
            continue

        # Build multi-mode DPS tag
        multi_mode_tag = ""
        multi_mode_alpha = ""
        if has_heat and len(parsed_modes) >= 2:
            # Standard heat: "Heat" + "Heat 50%"
            cold = next((m for m in parsed_modes if "heat" in m["mode"].lower() and "50%" not in m["mode"]), None)
            hot = next((m for m in parsed_modes if "50%" in m["mode"]), None)
            # Slug->pellet heat (Prism): "Slug" is cold, other mode is hot
            if not cold or not hot:
                slug = next((m for m in parsed_modes if "slug" in m["mode"].lower()), None)
                other = next((m for m in parsed_modes if "slug" not in m["mode"].lower() and "combined" not in m["mode"].lower()), None)
                if slug and other:
                    cold = slug
                    hot = other
            if cold and hot and abs(cold["dps_sus"] - hot["dps_sus"]) > 1:
                primary = cold  # Use cold as primary (starting DPS)
                multi_mode_tag = f" (caliente: {fmt_num(hot['dps_sus'])})"
                if abs(cold["alpha"] - hot["alpha"]) > 0.5:
                    multi_mode_alpha = f"{fmt_num(cold['alpha'])}-{fmt_num(hot['alpha'])}"
        elif has_charge and not has_combined:
            normal = next((m for m in parsed_modes if "charge" not in m["mode"].lower()), None)
            charged = next((m for m in parsed_modes if "charge" in m["mode"].lower()), None)
            if normal and charged and charged["dps_sus"] > 0:
                primary = normal  # Use normal as primary
                multi_mode_tag = f" (cargado: {fmt_num(charged['dps_sus'])})"
        elif len(parsed_modes) >= 2 and not has_combined:
            # Selectable modes (Rapid/Single, Double/Single, etc.)
            modes_by_dps = sorted(parsed_modes, key=lambda m: m["dps_sus"], reverse=True)
            primary = modes_by_dps[0]
            secondary = modes_by_dps[1]
            if secondary["dps_sus"] > 0 and secondary["dps_sus"] != primary["dps_sus"]:
                # Describe secondary mode briefly
                sec_name = secondary["mode"].split()[0].lower()
                if sec_name in ("single", "semi"):
                    sec_label = "semi"
                elif sec_name in ("burst"):
                    sec_label = "burst"
                elif sec_name in ("rapid", "auto"):
                    sec_label = "auto"
                elif sec_name in ("double"):
                    sec_label = "doble"
                else:
                    sec_label = sec_name
                multi_mode_tag = f" / {fmt_num(secondary['dps_sus'])} ({sec_label})"

        # Extract stats from primary row
        best_row = primary["row"]
        fire_mode = primary["mode"]
        alpha = primary["alpha"]
        pellets = primary["pellets"]
        dps_sustained = primary["dps_sus"]
        dps_burst = primary["dps_burst"]
        speed = _parse_csv_float(best_row[8]) if len(best_row) > 8 else 0
        range_m = _parse_csv_float(best_row[10]) if len(best_row) > 10 else 0
        drop_dist = _parse_csv_float(best_row[26]) if len(best_row) > 26 else 0
        drop_pm = _parse_csv_float(best_row[27]) if len(best_row) > 27 else 0
        drop_min = _parse_csv_float(best_row[28]) if len(best_row) > 28 else 0
        dmg_mag = _parse_csv_float(best_row[98]) if len(best_row) > 98 else 0

        # Match to className
        class_name = _match_excel_name(weapon_name, name_map)
        if not class_name:
            skipped_no_match += 1
            print(f"  WARNING: No className match for '{weapon_name}'")
            continue

        class_name_lower = class_name.lower()

        # Get penetration from scunpacked
        penetration = pen_map.get(class_name_lower, 0)
        # Also check base className (without skin suffix)
        if penetration == 0:
            for pcn, pval in pen_map.items():
                if class_name_lower == pcn or class_name_lower.startswith(pcn + "_"):
                    penetration = pval
                    break
                if pcn.startswith(class_name_lower):
                    penetration = pval
                    break

        # Classify weapon
        category = classify_weapon_tested(fire_mode, pellets, alpha, dps_sustained, dps_burst, drop_dist)
        if category is None:
            skipped_zero_dps += 1
            continue

        # Detect burst
        is_burst = "burst" in fire_mode.lower()

        # Build list of all displayable modes
        # If a Combined mode exists, use it instead of the individual damage types
        combined = [m for m in parsed_modes if "combined" in m["mode"].lower() and m["dps_sus"] > 0]
        has_slug = any("slug" in m["mode"].lower() for m in parsed_modes)
        if combined and not has_slug:
            # Pure combined (e.g., Killshot): only show combined
            all_modes = combined
        elif combined and has_slug:
            # Slug + Combined (e.g., Prism): show Slug as cold, Combined as hot
            slug_modes = [m for m in parsed_modes if "slug" in m["mode"].lower() and m["dps_sus"] > 0]
            all_modes = slug_modes + combined
        else:
            all_modes = [m for m in parsed_modes if m["dps_sus"] > 0]

        # Remove duplicate modes with same DPS (e.g., Quartz Beam Heat + Beam Heat 50% both 225)
        deduped = []
        seen_dps = set()
        for m in all_modes:
            key = (round(m["dps_sus"], 1), round(m["alpha"], 1))
            if key not in seen_dps:
                seen_dps.add(key)
                deduped.append(m)
        all_modes = deduped

        # Get mass from primary mode
        mass = primary.get("mass", 0) or 0

        # Build item dict in scunpacked-compatible format
        item = {
            "className": class_name,
            "_all_modes": all_modes,
            "stdItem": {
                "Mass": mass,
                "Weapon": {
                    "Damage": {
                        "DpsTotal": dps_sustained,
                        "AlphaTotal": alpha,
                        "MaxPerMag": dmg_mag,
                        "Dps": {},
                        "Alpha": {},
                    },
                    "Modes": [{"FireType": "burst" if is_burst else fire_mode.lower(), "PelletsPerShot": pellets}],
                    "FireMode": fire_mode,
                },
                "Ammunition": {
                    "Speed": speed,
                    "Range": range_m,
                    "MaxPenetrationThickness": penetration,
                    "DamageDropMinDistance": {"Physical": drop_dist} if drop_dist > 0 else {},
                    "DamageDropPerMeter": {"Physical": drop_pm} if drop_pm > 0 else {},
                    "DamageDropMinDamage": {"Physical": drop_min} if drop_min > 0 else {},
                },
            },
        }

        # Build stats block
        stats_block = build_stats_block_tested(item, category)
        if stats_block is None:
            continue

        # Store for ALL skins of this base weapon
        # The base className maps to the item_Desc key
        weapons[class_name_lower] = (item, category, stats_block)

        # Also map all skin variants
        for sname, cn in name_map.items():
            cn_lower = cn.lower()
            if cn_lower.startswith(class_name_lower) and cn_lower != class_name_lower:
                # Skin variant — copy same stats
                skin_item = dict(item)
                skin_item["className"] = cn
                weapons[cn_lower] = (skin_item, category, stats_block)

        matched += 1

    # Also map all skins from scunpacked that share a base className
    # We need to find ALL classNames in fps_items that share the same base
    base_classes = {}  # base_cn_lower -> stats tuple
    for cn_lower, val in list(weapons.items()):
        base_classes[cn_lower] = val

    for fps_item in fps_items:
        if fps_item.get("type") != "WeaponPersonal":
            continue
        cn = fps_item.get("className", "").lower()
        if cn in weapons:
            continue
        # Check if any base className is a prefix
        for base_cn, val in base_classes.items():
            if cn.startswith(base_cn + "_") or cn == base_cn:
                skin_item = dict(val[0])
                skin_item["className"] = fps_item.get("className", "")
                weapons[cn] = (skin_item, val[1], val[2])
                break

    print(f"Weapons matched from CSV: {matched}")
    print(f"  Total entries (incl. skins): {len(weapons)}")
    print(f"  Skipped (zero DPS): {skipped_zero_dps}")
    print(f"  Skipped (no className match): {skipped_no_match}")
    print()

    return weapons


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def load_scunpacked_weapons(fps_items):
    """
    Load weapon stats from scunpacked fps-items.json (original behavior).

    Returns: dict of className -> (item_dict, category, stats_block)
    """
    weapons = {}
    skipped_no_data = 0
    skipped_zero_dps = 0
    skipped_penetration = 0

    for item in fps_items:
        if item.get("type") != "WeaponPersonal":
            continue

        class_name = item.get("className", "").lower()
        si = item.get("stdItem", {})
        weapon = si.get("Weapon")

        # Check for manual override (base className, strip skin suffixes)
        override = None
        for base_cn, ov in MANUAL_OVERRIDES.items():
            if class_name == base_cn or class_name.startswith(base_cn + "_"):
                override = ov
                break

        if override:
            category = override["category"]
            if category == "custom":
                stats_block = override["stats_line"]
            else:
                if not weapon:
                    weapon = {"Damage": {}, "Modes": []}
                    si["Weapon"] = weapon
                damage = weapon.setdefault("Damage", {})
                damage["DpsTotal"] = override["DpsTotal"]
                damage["AlphaTotal"] = override["AlphaTotal"]
                damage["Dps"] = override["Dps"]
                damage["MaxPerMag"] = override.get("MaxPerMag", 0)
                ammo = si.setdefault("Ammunition", {})
                if "Speed" in override:
                    ammo["Speed"] = override["Speed"]
                if "Penetration" in override:
                    ammo["MaxPenetrationThickness"] = override["Penetration"]
                if "DamageDropDist" in override:
                    ammo["DamageDropMinDistance"] = {"Physical": override["DamageDropDist"]}
                if "BeamData" in override:
                    si["BeamData"] = override["BeamData"]
                stats_block = build_stats_block(item, category)
        else:
            if not weapon:
                skipped_no_data += 1
                continue

            damage = weapon.get("Damage", {})
            dps_total = damage.get("DpsTotal") or 0
            has_beam = "BeamData" in si

            if dps_total <= 0 and not has_beam:
                skipped_zero_dps += 1
                continue

            if has_beam and dps_total <= 0:
                beam = si.get("BeamData", {})
                if not beam.get("FullDamageRange") and not beam.get("ZeroDamageRange"):
                    skipped_zero_dps += 1
                    continue

            category = classify_weapon(item)
            if category is None:
                skipped_zero_dps += 1
                continue

            stats_block = build_stats_block(item, category)

        if stats_block is None:
            skipped_penetration += 1
            continue

        weapons[class_name] = (item, category, stats_block)

    print(f"Weapons with stats: {len(weapons)}")
    print(f"  Skipped (no weapon data): {skipped_no_data}")
    print(f"  Skipped (zero DPS / non-combat): {skipped_zero_dps}")
    print(f"  Skipped (bad penetration data): {skipped_penetration}")
    print()

    return weapons


def main():
    parser = argparse.ArgumentParser(description="Inject real weapon stats into global.ini")
    parser.add_argument("--version", type=str, default=None,
                        help="Version directory name (default: auto-detect latest)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show changes without writing")
    parser.add_argument("--source", choices=["scunpacked", "tested"], default="scunpacked",
                        help="Data source: scunpacked (default) or tested (spreadsheet CSV)")
    args = parser.parse_args()

    # Resolve version
    version = args.version or detect_latest_version()
    if not version:
        print("ERROR: No version directory found.", file=sys.stderr)
        sys.exit(1)

    version_dir = VERSIONS_DIR / version
    fps_json_path = version_dir / "sources" / "scunpacked" / "fps-items.json"
    global_ini_path = version_dir / "output" / "global.ini"

    if not fps_json_path.is_file():
        print(f"ERROR: {fps_json_path} not found.", file=sys.stderr)
        sys.exit(1)
    if not global_ini_path.is_file():
        print(f"ERROR: {global_ini_path} not found.", file=sys.stderr)
        sys.exit(1)

    print(f"Version: {version}")
    print(f"Source: {args.source}")
    print(f"FPS JSON: {fps_json_path}")
    print(f"global.ini: {global_ini_path}")
    print()

    # Load FPS items (always needed — for scunpacked stats or for name/penetration mapping)
    with open(fps_json_path, "r", encoding="utf-8") as f:
        fps_items = json.load(f)

    # Load weapons based on source
    if args.source == "tested":
        weapons = load_tested_weapons(version_dir, fps_items)
    else:
        weapons = load_scunpacked_weapons(fps_items)

    # Load global.ini (UTF-8 with BOM)
    with open(global_ini_path, "r", encoding="utf-8-sig") as f:
        lines = f.readlines()

    # Build index: lowercase className -> set of line indices
    # Pattern: item_Desc{className}=
    desc_pattern = re.compile(r"^item_Desc(.+?)=", re.IGNORECASE)

    patched = 0
    not_found = []
    modified_lines = list(lines)

    for i, line in enumerate(lines):
        m = desc_pattern.match(line)
        if not m:
            continue

        key_classname = m.group(1).lower()
        if key_classname not in weapons:
            continue

        item, category, stats_block = weapons[key_classname]

        # Extract key=value
        eq_pos = line.index("=")
        key_part = line[:eq_pos + 1]
        value_part = line[eq_pos + 1:].rstrip("\n").rstrip("\r")

        # Parse description
        header_str, old_stats, flavor_str = parse_description(value_part)

        # Rebuild with new stats
        new_value = rebuild_description(header_str, stats_block, flavor_str)
        new_line = key_part + new_value + "\n"

        if new_line != line:
            if args.dry_run and patched < 5:
                print(f"--- {item['className']} [{category}]")
                print(f"  OLD: ...{value_part[:200]}...")
                print(f"  NEW: ...{new_value[:200]}...")
                print()

            modified_lines[i] = new_line
            patched += 1

        # Mark as found
        weapons[key_classname] = None  # consumed

    # --- Patch magazine descriptions with mass ---
    mag_patched = 0
    if args.source == "tested":
        mag_csv = version_dir / "sources" / "tested" / "sin_crafteo" / "tab_Magazine.csv"
        if mag_csv.is_file():
            mag_mass = {}
            with open(mag_csv, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    filename = row[13].strip().lower() if len(row) > 13 else ""
                    mass_str = row[12].strip() if len(row) > 12 else ""
                    if filename and mass_str:
                        try:
                            mag_mass[filename] = float(mass_str)
                        except ValueError:
                            pass

            # Also build from scunpacked for fallback
            for fps_item in fps_items:
                si = fps_item.get("stdItem", {})
                if si.get("Type", "").startswith("WeaponAttachment.Magazine"):
                    cn = fps_item.get("className", "").lower()
                    m = si.get("Mass", 0)
                    if cn and m and cn not in mag_mass:
                        mag_mass[cn] = m

            mag_pattern = re.compile(r"^item_Desc(.+_mag[^=]*)=", re.IGNORECASE)
            for i, line in enumerate(modified_lines):
                mm = mag_pattern.match(line)
                if not mm:
                    continue
                mag_cn = mm.group(1).lower()
                mass = mag_mass.get(mag_cn, 0)
                if mass <= 0:
                    continue

                eq_pos = line.index("=")
                key_part = line[:eq_pos + 1]
                value_part = line[eq_pos + 1:].rstrip("\n").rstrip("\r")

                # Check if mass already injected
                if f"{fmt_num(mass)} kg" in value_part:
                    continue

                # Find "Capacidad: X" or "Capacity: X" and append mass
                new_value = re.sub(
                    r"(Capacidad:\s*\d+|Capacity:\s*\d+)",
                    rf"\1 | {fmt_num(mass)} kg",
                    value_part,
                    count=1
                )
                if new_value != value_part:
                    modified_lines[i] = key_part + new_value + "\n"
                    mag_patched += 1

    # Report unmatched weapons
    unmatched = [cn for cn, val in weapons.items() if val is not None]

    print(f"Patched: {patched} descriptions")
    if mag_patched:
        print(f"Patched: {mag_patched} magazine descriptions (mass)")
    if unmatched:
        print(f"Unmatched weapons (no item_Desc found): {len(unmatched)}")
        # Show first 20
        for cn in sorted(unmatched)[:20]:
            print(f"  - {cn}")
        if len(unmatched) > 20:
            print(f"  ... and {len(unmatched) - 20} more")

    # Write output
    if not args.dry_run:
        with open(global_ini_path, "w", encoding="utf-8-sig", newline="") as f:
            f.writelines(modified_lines)
        print(f"\nWritten: {global_ini_path}")
    else:
        print(f"\n[DRY RUN] No changes written.")


if __name__ == "__main__":
    main()
