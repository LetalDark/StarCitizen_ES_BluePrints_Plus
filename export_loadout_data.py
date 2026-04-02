#!/usr/bin/env python3
"""
export_loadout_data.py — Genera loadout-calculator.json desde los CSVs testeados.

Lee tab_Item.csv, tab_Armor.csv y tab_Magazine.csv del directorio sources/tested/sin_crafteo/
y genera un JSON con todos los items, fórmulas de velocidad y slots del loadout.

Uso:
    python export_loadout_data.py                    # Genera el JSON
    python export_loadout_data.py --verify           # Genera y verifica
    python export_loadout_data.py --dry-run          # Preview sin escribir
    python export_loadout_data.py --output otro.json # Ruta de salida personalizada
"""

import argparse
import csv
import json
import math
import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuración
# ---------------------------------------------------------------------------

GAME_VERSION = "4.7.0-LIVE"

# Fórmulas verificadas contra el Calculator de Calculator spreadsheet (4.7)
FORMULAS = {
    "speed_factor": {
        "description": "Speed factor based on total loadout mass. Uses threshold table: first matching threshold (>=) from top to bottom.",
        "thresholds": [
            {"min_mass": 80, "factor": 0.50},
            {"min_mass": 75, "factor": 0.55},
            {"min_mass": 70, "factor": 0.60},
            {"min_mass": 65, "factor": 0.65},
            {"min_mass": 60, "factor": 0.70},
            {"min_mass": 55, "factor": 0.75},
            {"min_mass": 45, "factor": 0.80},
            {"min_mass": 35, "factor": 0.85},
            {"min_mass": 25, "factor": 0.90},
            {"min_mass": 15, "factor": 0.95},
            {"min_mass": 0, "factor": 1.00},
        ],
    },
    "sprint_speed": {
        "description": "Sprint speed in m/s = base * speed_factor",
        "base": 6.85,
    },
    "run_speed": {
        "description": "Run speed in m/s = base * speed_factor",
        "base": 5.0,
    },
    "ads_speed": {
        "description": "ADS movement speed in m/s = base * speed_factor * direction_mult",
        "base": 2.7,
        "direction_multiplier": {"forward": 1.0, "lateral_back": 0.75},
    },
    "sprint_duration": {
        "description": "Sprint duration in seconds = 0.9 / (A * (1 + mass * B) * buff_mult - C * buff_decay). Without buff: buff_mult=1, buff_decay=1",
        "A": 0.0768,
        "B": 0.005,
        "C": 0.07,
        "buff": {
            "description": "Hypertrophic + Energizing buff",
            "multiplier": 0.95,
            "decay": 1.05,
        },
    },
}

SLOTS = {
    "clothing": ["hat", "shirt", "jacket", "torso_2", "gloves", "pants", "footwear"],
    "armor": ["undersuit", "helmet", "torso", "backpack", "arms", "legs"],
    "weapons": {
        "primary": {"weapon": 1, "magazine": 1, "optic": 1, "barrel": 1, "underbarrel": 1},
        "secondary": {"weapon": 1, "magazine": 1, "optic": 1, "barrel": 1, "underbarrel": 1},
        "sidearm": {"weapon": 1, "magazine": 1, "optic": 1, "barrel": 1, "underbarrel": 1},
    },
    "items": {"grenades": 4, "consumables": 4, "extra_magazines": 8},
    "utility": {
        "undersuit_slot": {"weapon": 1, "module": 1, "magazine_1": 1, "magazine_2": 1},
        "legs_slot": {"weapon": 1, "module": 1, "magazine_1": 1, "magazine_2": 1},
    },
    "gadget": 1,
    "mobiglas": 1,
}

ACCESSORIES = {
    "description": "All weapon accessories (optics, barrels, underbarrel) weigh 0.1 kg each",
    "optic": {"mass_kg": 0.1},
    "barrel": {"mass_kg": 0.1},
    "underbarrel": {"mass_kg": 0.1},
}

# Categorías de armas (van al array "weapons")
WEAPON_CATEGORIES = {
    "ASSAULT RIFLE", "LMG", "PISTOL", "SHOTGUN", "SMG", "SNIPER RIFLE",
    "GRENADE LAUNCHER", "RAILGUN", "MOUNTED GUN", "ROCKET LAUNCHER",
    "MISSILE LAUNCHER",
}

# Mapeo de nombre de categoría CSV → category en JSON
CATEGORY_MAP = {
    "ASSAULT RIFLE": "assault_rifle",
    "LMG": "lmg",
    "PISTOL": "pistol",
    "SHOTGUN": "shotgun",
    "SMG": "smg",
    "SNIPER RIFLE": "sniper_rifle",
    "GRENADE LAUNCHER": "grenade_launcher",
    "RAILGUN": "railgun",
    "MOUNTED GUN": "mounted_gun",
    "ROCKET LAUNCHER": "rocket_launcher",
    "MISSILE LAUNCHER": "missile_launcher",
    "GRENADE": "grenade",
    "UTILITY": "utility",
    "CONSUMABLE": "consumable",
    "MELEE": "melee",
    "MINE": "mine",
    "GADGET": "gadget",
}

# Sub-categorías para consumibles
DRUG_NAMES = {"SLAM1", "SLAM2", "Drema Injector", "Tigersclaw"}
HACKING_NAMES = {"Re-Authorizer", "icePick", "FUNT debug", "FUNT",
                 "LOC_PLACEHOLDER", "Ripper", "Walesko", "Decryption Key"}

# Items debug/placeholder que no se exportan
SKIP_ITEMS = {"FUNT debug", "LOC_PLACEHOLDER", "Treat Injuries\n(Arena Commander MedPen)"}

# Nombres de flares (sub-categoría de grenade)
FLARE_PATTERN = re.compile(r"(QuikFlare|Light Stick|Luminalia)", re.IGNORECASE)


def clean_name(name):
    """Limpia non-breaking spaces y whitespace extra."""
    return name.replace("\xa0", " ").replace("\n", " ").strip()


def parse_float(val):
    """Convierte string a float, retorna None si vacío."""
    val = val.strip()
    if not val:
        return None
    try:
        return float(val)
    except ValueError:
        return None


# ---------------------------------------------------------------------------
# Parsers de CSV
# ---------------------------------------------------------------------------

def parse_items(csv_path):
    """Parsea tab_Item.csv → weapons, grenades, utilities, consumables, melee, gadgets."""
    weapons = []
    grenades = []
    utilities = []
    consumables = []
    melee = []
    gadgets = []

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        current_cat = None
        for i, row in enumerate(reader):
            if len(row) < 6:
                continue
            name_raw = row[0].strip()
            if not name_raw:
                continue
            mass_str = row[5].strip() if len(row) > 5 else ""
            mass_loaded_str = row[6].strip() if len(row) > 6 else ""

            # Detectar filas de categoría (MAYÚSCULAS sin masa)
            if name_raw.isupper() and not mass_str:
                current_cat = name_raw
                continue

            # Filas de datos
            if current_cat is None or not mass_str:
                continue

            name = clean_name(name_raw)
            mass = parse_float(mass_str)
            mass_loaded = parse_float(mass_loaded_str)

            if mass is None:
                continue

            # Saltar items debug
            if name in SKIP_ITEMS or clean_name(row[0]) in SKIP_ITEMS:
                continue

            cat_key = CATEGORY_MAP.get(current_cat, current_cat.lower())

            if current_cat in WEAPON_CATEGORIES:
                item = {"name": name, "category": cat_key, "mass_kg": mass}
                if mass_loaded is not None:
                    item["mass_loaded_kg"] = mass_loaded
                weapons.append(item)

            elif current_cat == "GRENADE":
                sub = "flare" if FLARE_PATTERN.search(name) else "grenade"
                grenades.append({"name": name, "category": sub, "mass_kg": mass})

            elif current_cat == "UTILITY":
                item = {"name": name, "mass_kg": mass}
                if mass_loaded is not None:
                    item["mass_loaded_kg"] = mass_loaded
                utilities.append(item)

            elif current_cat == "CONSUMABLE":
                if name in DRUG_NAMES or name.startswith("SLAM"):
                    sub = "drug"
                    # Unificar SLAM1/SLAM2 → SLAM
                    if name.startswith("SLAM"):
                        name = "SLAM"
                        # Evitar duplicados
                        if any(c["name"] == "SLAM" for c in consumables):
                            continue
                elif name in HACKING_NAMES:
                    sub = "hacking"
                else:
                    sub = "medical"
                consumables.append({"name": name, "category": sub, "mass_kg": mass})

            elif current_cat == "MELEE":
                # Evitar duplicados (FSK-8 Gun Game vs normal)
                if "(Gun Game)" in name:
                    continue
                melee.append({"name": name, "mass_kg": mass})

            elif current_cat == "GADGET":
                gadgets.append({"name": name, "mass_kg": mass})

            elif current_cat == "MINE":
                grenades.append({"name": name, "category": "mine", "mass_kg": mass})

    return weapons, grenades, utilities, consumables, melee, gadgets


def parse_armor(csv_path):
    """Parsea tab_Armor.csv → armor list y clothing list."""
    armor = []
    clothing = []

    # Mapeo de tipos para simplificar y normalizar
    clothing_types = {"Feet": "footwear", "Hands": "gloves", "Hat": "hat",
                      "Torso_0": "shirt", "Torso_1": "jacket", "Torso_2": "torso_2"}
    # "Pants" en el CSV tiene Type=Legs pero es ropa, no armadura
    pants_names = {"Pants"}
    armor_types = {"Arms", "Backpack", "Helmet", "Legs", "Torso", "Undersuit", "MobiGlas"}

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)  # skip header
        for row in reader:
            if len(row) < 4:
                continue
            name = clean_name(row[0])
            item_type = row[1].strip()
            size = parse_float(row[2])
            mass = parse_float(row[3])
            if mass is None:
                continue

            if name in pants_names and item_type == "Legs":
                clothing.append({"name": "Pants", "type": "pants", "mass_kg": mass})
            elif item_type in clothing_types:
                ctype = clothing_types[item_type]
                # Usar nombre genérico del tipo de ropa
                display_name = name if name != item_type else ctype.replace("_", " ").title()
                clothing.append({
                    "name": display_name,
                    "type": ctype,
                    "mass_kg": mass,
                })
            elif item_type == "MobiGlas":
                # Se incluye como "fixed" por separado
                continue
            elif item_type in armor_types:
                # Agrupar por tipo — los backpacks tienen nombres propios
                if item_type == "Backpack":
                    armor.append({
                        "name": name,
                        "type": "backpack",
                        "size": int(size) if size else 1,
                        "mass_kg": mass,
                    })
                elif item_type == "Undersuit":
                    armor.append({
                        "name": name,
                        "type": "undersuit",
                        "mass_kg": mass,
                    })
                else:
                    # Construir nombre legible: "Heavy Helmet", "Light Arms", etc.
                    display = f"{name} {item_type}" if name != item_type else item_type
                    armor.append({
                        "name": display,
                        "type": item_type.lower(),
                        "mass_kg": mass,
                    })

    return armor, clothing


def parse_magazines(csv_path):
    """Parsea tab_Magazine.csv → magazines list."""
    magazines = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)  # skip header
        for row in reader:
            if len(row) < 13:
                continue
            name = clean_name(row[0])
            if not name:
                continue
            # col 6 = Max Ammo Count
            capacity = parse_float(row[6])
            # col 12 = Mass (kg)
            mass = parse_float(row[12])
            if mass is None:
                continue

            # Saltar duplicados AC (Arena Commander)
            if "AC" in name and any(m["name"] == name.replace(" AC", "") for m in magazines):
                continue

            magazines.append({
                "name": name,
                "capacity": int(capacity) if capacity else 0,
                "mass_kg": mass,
            })
    return magazines


# ---------------------------------------------------------------------------
# Verificación
# ---------------------------------------------------------------------------

def get_speed_factor(mass):
    """Calcula speed factor desde la tabla de thresholds."""
    for t in FORMULAS["speed_factor"]["thresholds"]:
        if mass >= t["min_mass"]:
            return t["factor"]
    return 1.0


def calc_sprint_duration(mass, with_buff=False):
    """Calcula sprint duration en segundos."""
    sd = FORMULAS["sprint_duration"]
    buff_m = sd["buff"]["multiplier"] if with_buff else 1.0
    buff_d = sd["buff"]["decay"] if with_buff else 1.0
    denom = sd["A"] * (1 + mass * sd["B"]) * buff_m - sd["C"] * buff_d
    if denom <= 0:
        return float("inf")
    return 0.9 / denom


def verify_json(data):
    """Ejecuta checks de verificación sobre el JSON generado."""
    errors = []
    warnings = []

    # --- Check 1: Conteos mínimos ---
    checks = [
        ("weapons", 40, 50),
        ("grenades", 8, 15),
        ("consumables", 15, 30),
        ("melee", 8, 15),
        ("gadgets", 5, 8),
        ("utilities", 5, 10),
        ("armor", 15, 50),
        ("clothing", 5, 10),
        ("magazines", 45, 60),
    ]
    for key, min_count, max_count in checks:
        count = len(data.get(key, []))
        if count < min_count:
            errors.append(f"[COUNT] {key}: {count} items (esperado >= {min_count})")
        elif count > max_count:
            warnings.append(f"[COUNT] {key}: {count} items (esperado <= {max_count})")
        else:
            print(f"  OK  {key}: {count} items")

    # --- Check 2: Todos los items tienen mass_kg > 0 (excepto mines) ---
    for section in ["weapons", "grenades", "consumables", "melee", "gadgets", "utilities", "armor", "clothing", "magazines"]:
        for item in data.get(section, []):
            mass = item.get("mass_kg", 0)
            if mass < 0:
                errors.append(f"[MASS] {section}/{item['name']}: masa negativa ({mass})")
            if mass == 0 and item.get("category") != "mine":
                warnings.append(f"[MASS] {section}/{item['name']}: masa = 0")

    # --- Check 3: No hay nombres duplicados dentro de cada sección ---
    for section in ["weapons", "grenades", "consumables", "melee", "gadgets", "utilities", "magazines"]:
        names = [item["name"] for item in data.get(section, [])]
        seen = set()
        for name in names:
            if name in seen:
                errors.append(f"[DUP] {section}: nombre duplicado '{name}'")
            seen.add(name)

    # --- Check 4: Fórmulas cuadran con valores conocidos del Calculator ---
    test_cases = [
        # (mass, expected_factor, expected_sprint, expected_run, expected_duration, expected_ads)
        (54.76, 0.80, 5.48, 4.00, 32.3, 2.16),
        (44.96, 0.85, 5.8225, 4.25, 37.4, 2.295),
    ]
    for mass, exp_factor, exp_sprint, exp_run, exp_dur, exp_ads in test_cases:
        factor = get_speed_factor(mass)
        sprint = FORMULAS["sprint_speed"]["base"] * factor
        run = FORMULAS["run_speed"]["base"] * factor
        duration = round(calc_sprint_duration(mass), 1)
        ads = FORMULAS["ads_speed"]["base"] * factor

        if factor != exp_factor:
            errors.append(f"[FORMULA] mass={mass}: speed_factor={factor}, esperado={exp_factor}")
        if abs(sprint - exp_sprint) > 0.01:
            errors.append(f"[FORMULA] mass={mass}: sprint={sprint}, esperado={exp_sprint}")
        if abs(run - exp_run) > 0.01:
            errors.append(f"[FORMULA] mass={mass}: run={run}, esperado={exp_run}")
        if abs(duration - exp_dur) > 0.1:
            errors.append(f"[FORMULA] mass={mass}: duration={duration}, esperado={exp_dur}")
        if abs(ads - exp_ads) > 0.01:
            errors.append(f"[FORMULA] mass={mass}: ads={ads}, esperado={exp_ads}")

    if not any("FORMULA" in e for e in errors):
        print("  OK  Fórmulas verificadas (2 loadouts de referencia)")

    # --- Check 5: Weapons tienen mass_loaded_kg >= mass_kg ---
    for w in data.get("weapons", []):
        if "mass_loaded_kg" in w and w["mass_loaded_kg"] < w["mass_kg"]:
            errors.append(f"[LOADED] {w['name']}: loaded ({w['mass_loaded_kg']}) < unloaded ({w['mass_kg']})")
    if not any("LOADED" in e for e in errors):
        print("  OK  Todas las armas: mass_loaded >= mass_unloaded")

    # --- Check 6: Magazines tienen capacity > 0 ---
    for m in data.get("magazines", []):
        if m["capacity"] <= 0:
            warnings.append(f"[MAG] {m['name']}: capacity = {m['capacity']}")
    if not any("MAG" in w for w in warnings):
        print("  OK  Todos los cargadores tienen capacity > 0")

    # --- Check 7: Categorías de armas cubren todos los tipos esperados ---
    weapon_cats = set(w["category"] for w in data.get("weapons", []))
    expected_cats = {"assault_rifle", "lmg", "pistol", "shotgun", "smg", "sniper_rifle"}
    missing = expected_cats - weapon_cats
    if missing:
        errors.append(f"[CATS] Categorías de arma faltantes: {missing}")
    else:
        print(f"  OK  Categorías de armas: {len(weapon_cats)} tipos")

    # --- Check 8: Secciones del JSON completas ---
    required_sections = ["version", "source", "formulas", "slots", "accessories",
                         "weapons", "grenades", "consumables", "melee", "gadgets",
                         "utilities", "armor", "clothing", "fixed", "magazines"]
    for section in required_sections:
        if section not in data:
            errors.append(f"[SECTION] Falta sección '{section}' en el JSON")
    if not any("SECTION" in e for e in errors):
        print(f"  OK  Todas las secciones presentes ({len(required_sections)})")

    # --- Check 9: Idempotencia — re-parsear los mismos CSVs da el mismo resultado ---
    # (se verifica externamente comparando el hash del output)

    return errors, warnings


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def find_version_dir():
    """Busca el directorio de versión más reciente."""
    versions_dir = Path("versions")
    if not versions_dir.exists():
        print("ERROR: No se encuentra el directorio 'versions/'", file=sys.stderr)
        sys.exit(1)
    dirs = sorted(versions_dir.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True)
    for d in dirs:
        if d.is_dir():
            return d
    print("ERROR: No hay versiones en 'versions/'", file=sys.stderr)
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Genera loadout-calculator.json desde CSVs testeados")
    parser.add_argument("--verify", action="store_true", help="Verificar el JSON generado")
    parser.add_argument("--dry-run", action="store_true", help="Preview sin escribir archivo")
    parser.add_argument("--output", "-o", type=str, help="Ruta de salida del JSON")
    parser.add_argument("--version-dir", type=str, help="Directorio de versión (auto-detecta si no se especifica)")
    args = parser.parse_args()

    # Encontrar directorio de versión
    if args.version_dir:
        version_dir = Path(args.version_dir)
    else:
        version_dir = find_version_dir()

    csv_dir = version_dir / "sources" / "tested" / "sin_crafteo"
    if not csv_dir.exists():
        print(f"ERROR: No se encuentra {csv_dir}", file=sys.stderr)
        sys.exit(1)

    item_csv = csv_dir / "tab_Item.csv"
    armor_csv = csv_dir / "tab_Armor.csv"
    magazine_csv = csv_dir / "tab_Magazine.csv"

    for f in [item_csv, armor_csv, magazine_csv]:
        if not f.exists():
            print(f"ERROR: No se encuentra {f}", file=sys.stderr)
            sys.exit(1)

    print(f"Fuentes: {csv_dir}")
    print(f"Versión: {version_dir.name}")
    print()

    # Parsear CSVs
    print("Parseando CSVs...")
    weapons, grenades, utilities, consumables, melee_items, gadgets = parse_items(str(item_csv))
    armor, clothing = parse_armor(str(armor_csv))
    magazines = parse_magazines(str(magazine_csv))

    print(f"  Armas:        {len(weapons)}")
    print(f"  Granadas:     {len(grenades)}")
    print(f"  Utilities:    {len(utilities)}")
    print(f"  Consumibles:  {len(consumables)}")
    print(f"  Cuerpo a cpo: {len(melee_items)}")
    print(f"  Gadgets:      {len(gadgets)}")
    print(f"  Armadura:     {len(armor)}")
    print(f"  Ropa:         {len(clothing)}")
    print(f"  Cargadores:   {len(magazines)}")
    total = (len(weapons) + len(grenades) + len(utilities) + len(consumables) +
             len(melee_items) + len(gadgets) + len(armor) + len(clothing) + len(magazines))
    print(f"  TOTAL:        {total}")
    print()

    # Construir JSON
    data = {
        "version": GAME_VERSION,
        "source": "FPS Data Spreadsheet (tested in-game) + StarCitizen ES Plus",
        "formulas": FORMULAS,
        "slots": SLOTS,
        "accessories": ACCESSORIES,
        "weapons": weapons,
        "grenades": grenades,
        "consumables": consumables,
        "melee": melee_items,
        "gadgets": gadgets,
        "utilities": utilities,
        "armor": armor,
        "clothing": clothing,
        "fixed": [{"name": "mobiGlas", "mass_kg": 0.5}],
        "magazines": magazines,
    }

    # Verificar
    if args.verify or not args.dry_run:
        print("Verificando...")
        errors, warnings = verify_json(data)
        print()
        if warnings:
            print(f"  {len(warnings)} warnings:")
            for w in warnings:
                print(f"    WARN  {w}")
            print()
        if errors:
            print(f"  {len(errors)} ERRORES:")
            for e in errors:
                print(f"    ERROR {e}")
            print()
            if not args.dry_run:
                print("Abortando — corrige los errores antes de generar.")
                sys.exit(1)
        else:
            print("  Verificación OK — sin errores")
            print()

    # Escribir
    if args.dry_run:
        print("--- DRY RUN (no se escribe archivo) ---")
        print(json.dumps(data, indent=2, ensure_ascii=False)[:3000])
        print("... [truncado]")
    else:
        output_path = args.output or str(version_dir / "output" / "loadout-calculator.json")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        size_kb = os.path.getsize(output_path) / 1024
        print(f"Generado: {output_path} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
