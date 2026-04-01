#!/usr/bin/env python3
"""
Parchea los stats de armas beam en fps-items.json y ship-items.json.

Scunpacked no calcula DPS para armas beam (muestra 0). Este script:
1. Descarga los JSONs individuales de armas beam desde scunpacked-data
2. Extrae damagePerSecond, fullDamageRange, zeroDamageRange, etc.
3. Parchea los JSONs agregados con los datos reales

Uso:
    python patch_beam_stats.py [--scunpacked-dir DIR]
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error


GITHUB_API = "https://api.github.com/repos/StarCitizenWiki/scunpacked-data/contents/items"


def find_beam_weapons(items):
    """Encuentra armas beam en el JSON agregado."""
    beams = []
    for item in items:
        weapon = item.get("stdItem", {}).get("Weapon", {})
        fire_mode = weapon.get("FireMode", "")
        modes = weapon.get("Modes", [])
        is_beam = "beam" in fire_mode.lower()
        if not is_beam:
            for mode in modes:
                if "beam" in mode.get("FireType", "").lower():
                    is_beam = True
                    break
        if is_beam:
            beams.append(item)
    return beams


def find_key_recursive(obj, target):
    """Busca una key recursivamente en un dict/list."""
    if isinstance(obj, dict):
        if target in obj:
            return obj[target]
        for v in obj.values():
            r = find_key_recursive(v, target)
            if r is not None:
                return r
    elif isinstance(obj, list):
        for v in obj:
            r = find_key_recursive(v, target)
            if r is not None:
                return r
    return None


def download_item_json(classname, cache_dir):
    """Descarga el JSON individual de un item desde scunpacked-data."""
    cache_path = os.path.join(cache_dir, f"{classname}.json")
    if os.path.exists(cache_path) and os.path.getsize(cache_path) > 100:
        with open(cache_path, "r", encoding="utf-8") as f:
            return json.load(f)

    url = f"{GITHUB_API}/{classname}.json"
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github.v3.raw",
        "User-Agent": "StarCitizen-ES-Plus"
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(data, f)
        return data
    except urllib.error.HTTPError as e:
        print(f"  Error descargando {classname}: {e.code} {e.reason}")
        return None


def extract_beam_stats(item_json):
    """Extrae stats de beam del JSON individual."""
    dps_raw = find_key_recursive(item_json, "damagePerSecond")
    if not dps_raw:
        return None

    dps_info = dps_raw.get("DamageInfo", dps_raw)

    stats = {
        "BeamDps": {
            "Physical": dps_info.get("DamagePhysical", 0),
            "Energy": dps_info.get("DamageEnergy", 0),
            "Distortion": dps_info.get("DamageDistortion", 0),
            "Thermal": dps_info.get("DamageThermal", 0),
            "Biochemical": dps_info.get("DamageBiochemical", 0),
            "Stun": dps_info.get("DamageStun", 0),
        },
        "FullDamageRange": find_key_recursive(item_json, "fullDamageRange"),
        "ZeroDamageRange": find_key_recursive(item_json, "zeroDamageRange"),
        "HeatPerSecond": find_key_recursive(item_json, "heatPerSecond"),
        "ChargeUpTime": find_key_recursive(item_json, "chargeUpTime"),
        "ChargeDownTime": find_key_recursive(item_json, "chargeDownTime"),
        "HitRadius": find_key_recursive(item_json, "hitRadius"),
    }

    total = sum(v for v in stats["BeamDps"].values() if isinstance(v, (int, float)))
    stats["BeamDpsTotal"] = total

    return stats


def patch_item(item, beam_stats):
    """Parchea un item del JSON agregado con los stats de beam."""
    si = item.get("stdItem", {})
    weapon = si.get("Weapon", {})
    damage = weapon.get("Damage", {})

    # Parchear DPS
    damage["DpsTotal"] = beam_stats["BeamDpsTotal"]
    damage["AlphaTotal"] = beam_stats["BeamDpsTotal"]  # Para beams, alpha = dps
    damage["Burst"] = beam_stats["BeamDpsTotal"]
    damage["Dps"] = {k: v for k, v in beam_stats["BeamDps"].items()}
    damage["Alpha"] = {k: v for k, v in beam_stats["BeamDps"].items()}

    # Parchear modos
    for mode in weapon.get("Modes", []):
        mode["DamagePerSecond"] = beam_stats["BeamDpsTotal"]
        mode["Dps"] = beam_stats["BeamDpsTotal"]
        mode["Alpha"] = beam_stats["BeamDpsTotal"]
        for dtype in ["Physical", "Energy", "Distortion", "Thermal", "Biochemical", "Stun"]:
            mode[f"Dps{dtype}"] = beam_stats["BeamDps"].get(dtype, 0)
            mode[f"Alpha{dtype}"] = beam_stats["BeamDps"].get(dtype, 0)

    # Añadir datos beam-específicos
    si["BeamData"] = {
        "FullDamageRange": beam_stats["FullDamageRange"],
        "ZeroDamageRange": beam_stats["ZeroDamageRange"],
        "HeatPerSecond": beam_stats["HeatPerSecond"],
        "ChargeUpTime": beam_stats["ChargeUpTime"],
        "ChargeDownTime": beam_stats["ChargeDownTime"],
        "HitRadius": beam_stats["HitRadius"],
    }

    weapon["Damage"] = damage


def main():
    parser = argparse.ArgumentParser(description="Parchea stats de armas beam en JSONs de scunpacked")
    parser.add_argument("--scunpacked-dir", default=None,
                        help="Directorio con fps-items.json y ship-items.json")
    args = parser.parse_args()

    # Auto-detectar directorio
    if args.scunpacked_dir:
        base = args.scunpacked_dir
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Buscar en versions/*/sources/scunpacked/
        for root, dirs, files in os.walk(os.path.join(script_dir, "versions")):
            if "scunpacked" in dirs:
                candidate = os.path.join(root, "scunpacked")
                if os.path.exists(os.path.join(candidate, "fps-items.json")):
                    base = candidate
                    break
        else:
            print("No se encontró directorio scunpacked. Usa --scunpacked-dir")
            sys.exit(1)

    cache_dir = os.path.join(base, "items_beam")
    os.makedirs(cache_dir, exist_ok=True)

    patched_total = 0

    for json_file in ["fps-items.json", "ship-items.json"]:
        filepath = os.path.join(base, json_file)
        if not os.path.exists(filepath):
            continue

        print(f"\nProcesando {json_file}...")
        with open(filepath, "r", encoding="utf-8") as f:
            items = json.load(f)

        beams = find_beam_weapons(items)
        print(f"  Armas beam encontradas: {len(beams)}")

        # Agrupar por className base (sin skins)
        seen_base = {}
        for item in beams:
            cn = item.get("className", "")
            # Intentar descargar el individual
            if cn not in seen_base:
                item_json = download_item_json(cn, cache_dir)
                if item_json:
                    stats = extract_beam_stats(item_json)
                    if stats:
                        seen_base[cn] = stats
                        print(f"  {cn}: DPS={stats['BeamDpsTotal']} "
                              f"(E:{stats['BeamDps']['Energy']} D:{stats['BeamDps']['Distortion']}) "
                              f"Range:{stats['FullDamageRange']}-{stats['ZeroDamageRange']}m")
                    else:
                        # Probar con el base className (sin tints)
                        seen_base[cn] = None
                else:
                    seen_base[cn] = None

            beam_stats = seen_base.get(cn)
            if beam_stats:
                patch_item(item, beam_stats)
                patched_total += 1

        # Guardar
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False)
        print(f"  Guardado: {filepath}")

    print(f"\nTotal items parcheados: {patched_total}")


if __name__ == "__main__":
    main()
