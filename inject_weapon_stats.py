#!/usr/bin/env python3
"""
inject_weapon_stats.py — Inject real weapon stats into global.ini descriptions.

Reads fps-items.json from scunpacked and patches the description lines in
global.ini so they show accurate DPS, alpha, penetration, etc.

Usage:
    python inject_weapon_stats.py [--version 4.7.0-LIVE_11545720] [--dry-run]
"""

import argparse
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
    if penetration > 100:
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
        if len(active_dps) == 1:
            lines.append(f"DPS: {fmt_num(dps_total)}{burst_tag} | Alpha: {fmt_num(alpha_total)} | {pellets} perdigones")
        else:
            parts = [f"{fmt_num(v)} {k}" for k, v in active_dps.items()]
            lines.append(f"DPS: {fmt_num(dps_total)}{burst_tag} ({' + '.join(parts)}) | Alpha: {fmt_num(alpha_total)} | {pellets} perdigones")
        lines.append(f"Dmg/Cargador: {fmt_num(max_per_mag)} | Vel. Proyectil: {fmt_num(speed)} m/s")
        pen_line = f"Penetración: {fmt_num(penetration)}m"
        if drop_dist > 0:
            pen_line += f" | Caída daño: desde {fmt_num(drop_dist)}m"
        lines.append(pen_line)

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
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Inject real weapon stats into global.ini")
    parser.add_argument("--version", type=str, default=None,
                        help="Version directory name (default: auto-detect latest)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show changes without writing")
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
    print(f"FPS JSON: {fps_json_path}")
    print(f"global.ini: {global_ini_path}")
    print()

    # Load FPS items
    with open(fps_json_path, "r", encoding="utf-8") as f:
        fps_items = json.load(f)

    # Filter to WeaponPersonal items with stats
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
                # Direct stats line, no calculation needed
                stats_block = override["stats_line"]
            else:
                # Apply manual override to the item's data so build_stats_block works
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

            # Skip zero-DPS non-beam items (gadgets, tools, etc.)
            if dps_total <= 0 and not has_beam:
                skipped_zero_dps += 1
                continue

            # Beam weapons with DPS=0 and no useful beam data — skip
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

    # Report unmatched weapons
    unmatched = [cn for cn, val in weapons.items() if val is not None]

    print(f"Patched: {patched} descriptions")
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
