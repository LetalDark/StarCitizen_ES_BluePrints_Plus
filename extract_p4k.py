#!/usr/bin/env python3
"""
Extrae global.ini de localización desde el Data.p4k de Star Citizen.

Uso:
    python extract_p4k.py                          # Extrae english, autodetecta ruta SC
    python extract_p4k.py --lang spanish_(spain)   # Extrae español oficial
    python extract_p4k.py --list                   # Lista idiomas disponibles
    python extract_p4k.py --sc-path "D:/Games/StarCitizen/LIVE"
"""

import argparse
import os
import struct
import sys

try:
    import zstandard
except ImportError:
    print("Error: necesitas instalar zstandard:")
    print("  pip install zstandard")
    sys.exit(1)


# Rutas comunes de instalación de Star Citizen
SC_SEARCH_PATHS = [
    r"C:\Program Files\Roberts Space Industries\StarCitizen",
    r"D:\Program Files\Roberts Space Industries\StarCitizen",
    r"E:\Program Files\Roberts Space Industries\StarCitizen",
    r"D:\Roberts Space Industries\StarCitizen",
    r"E:\Roberts Space Industries\StarCitizen",
]

# Carpetas de versión en orden de prioridad
SC_CHANNELS = ["HOTFIX", "LIVE", "PTU", "EPTU"]


def find_data_p4k(sc_path=None):
    """Busca Data.p4k en la instalación de Star Citizen."""
    if sc_path:
        p4k = os.path.join(sc_path, "Data.p4k")
        if os.path.exists(p4k):
            return p4k
        # Quizá pasaron la carpeta padre (StarCitizen/)
        for channel in SC_CHANNELS:
            p4k = os.path.join(sc_path, channel, "Data.p4k")
            if os.path.exists(p4k):
                return p4k
        print(f"Error: no se encontró Data.p4k en {sc_path}")
        sys.exit(1)

    for base in SC_SEARCH_PATHS:
        for channel in SC_CHANNELS:
            p4k = os.path.join(base, channel, "Data.p4k")
            if os.path.exists(p4k):
                print(f"Encontrado: {p4k}")
                return p4k

    print("Error: no se encontró la instalación de Star Citizen.")
    print("Usa --sc-path para indicar la ruta manualmente.")
    sys.exit(1)


def parse_zip64_extra(extra_data):
    """Extrae tamaños y offset reales del campo extra ZIP64."""
    offset = 0
    while offset < len(extra_data) - 4:
        tag, size = struct.unpack("<HH", extra_data[offset : offset + 4])
        if tag == 0x0001:  # ZIP64 extended info
            field = extra_data[offset + 4 : offset + 4 + size]
            vals = {}
            pos = 0
            if pos + 8 <= size:
                vals["uncomp_size"] = struct.unpack("<Q", field[pos : pos + 8])[0]
                pos += 8
            if pos + 8 <= size:
                vals["comp_size"] = struct.unpack("<Q", field[pos : pos + 8])[0]
                pos += 8
            if pos + 8 <= size:
                vals["offset"] = struct.unpack("<Q", field[pos : pos + 8])[0]
                pos += 8
            return vals
        offset += 4 + size
    return {}


def find_eocd(f, file_size):
    """Localiza el End of Central Directory (ZIP64)."""
    search_size = min(65536 + 100, file_size)
    f.seek(file_size - search_size)
    data = f.read(search_size)

    # Buscar ZIP64 EOCD locator
    loc_pos = data.rfind(b"PK\x06\x07")
    if loc_pos < 0:
        # Intentar EOCD normal
        eocd_pos = data.rfind(b"PK\x05\x06")
        if eocd_pos < 0:
            print("Error: no se pudo leer la estructura ZIP del Data.p4k")
            sys.exit(1)
        eocd = data[eocd_pos : eocd_pos + 22]
        _, _, _, _, _, cd_size, cd_offset, _ = struct.unpack("<4sHHHHIIH", eocd)
        return cd_offset, cd_size, 0  # total_entries desconocido

    loc_data = data[loc_pos : loc_pos + 20]
    _, _, eocd64_offset, _ = struct.unpack("<4sIQI", loc_data)

    f.seek(eocd64_offset)
    eocd64 = f.read(56)
    (_, _, _, _, _, _, _, entries_total, cd_size, cd_offset) = struct.unpack(
        "<4sQHHIIQQQQ", eocd64
    )

    return cd_offset, cd_size, entries_total


def scan_central_directory(f, cd_offset, total_entries, target_prefix="Data\\Localization\\"):
    """Escanea el Central Directory buscando archivos de localización."""
    f.seek(cd_offset)
    results = {}

    for _ in range(total_entries):
        header = f.read(46)
        if len(header) < 46 or header[:4] != b"PK\x01\x02":
            break

        (
            _, _, _, flags, method, _, _, crc,
            comp_size, uncomp_size, name_len, extra_len, comment_len,
            _, _, _, local_offset,
        ) = struct.unpack("<4sHHHHHHIIIHHHHHII", header)

        name_bytes = f.read(name_len)
        extra_bytes = f.read(extra_len)
        f.read(comment_len)

        name = name_bytes.decode("utf-8", errors="replace")

        if not name.startswith(target_prefix):
            continue
        if not name.lower().endswith("global.ini"):
            continue

        zip64 = parse_zip64_extra(extra_bytes)
        results[name] = {
            "method": method,
            "comp_size": zip64.get("comp_size", comp_size),
            "uncomp_size": zip64.get("uncomp_size", uncomp_size),
            "offset": zip64.get("offset", local_offset),
        }

    return results


def extract_file(f, file_info):
    """Extrae y descomprime un archivo del p4k."""
    f.seek(file_info["offset"])
    local_header = f.read(30)
    (_, _, _, _, _, _, _, _, _, lname_len, lextra_len) = struct.unpack(
        "<4sHHHHHIIIHH", local_header
    )
    f.read(lname_len + lextra_len)

    compressed = f.read(file_info["comp_size"])

    if file_info["method"] == 100:  # ZSTD
        dctx = zstandard.ZstdDecompressor()
        return dctx.decompress(compressed, max_output_size=file_info["uncomp_size"] + 4096)
    elif file_info["method"] == 0:  # STORE
        return compressed
    elif file_info["method"] == 8:  # DEFLATE
        import zlib
        return zlib.decompress(compressed, -15)
    else:
        print(f"Error: método de compresión desconocido ({file_info['method']})")
        sys.exit(1)


def get_language_from_path(path):
    """Extrae el nombre del idioma de la ruta."""
    parts = path.replace("/", "\\").split("\\")
    for i, p in enumerate(parts):
        if p == "Localization" and i + 1 < len(parts):
            return parts[i + 1]
    return path


def main():
    parser = argparse.ArgumentParser(description="Extrae global.ini del Data.p4k de Star Citizen")
    parser.add_argument("--lang", default="english", help="Idioma a extraer (default: english)")
    parser.add_argument("--list", action="store_true", help="Lista idiomas disponibles")
    parser.add_argument("--sc-path", help="Ruta a la carpeta de SC (ej: D:\\Games\\StarCitizen\\LIVE)")
    parser.add_argument("-o", "--output", help="Archivo de salida (default: global_from_p4k.ini)")
    args = parser.parse_args()

    p4k_path = find_data_p4k(args.sc_path)
    file_size = os.path.getsize(p4k_path)
    print(f"Data.p4k: {file_size / (1024**3):.1f} GB")

    with open(p4k_path, "rb") as f:
        print("Leyendo estructura ZIP64...")
        cd_offset, cd_size, total_entries = find_eocd(f, file_size)
        print(f"Entradas totales: {total_entries:,}")

        print("Buscando archivos de localización...")
        loc_files = scan_central_directory(f, cd_offset, total_entries)

        if not loc_files:
            print("No se encontraron archivos de localización.")
            sys.exit(1)

        if args.list:
            print(f"\nIdiomas disponibles ({len(loc_files)}):")
            for path, info in sorted(loc_files.items()):
                lang = get_language_from_path(path)
                size_mb = info["uncomp_size"] / (1024 * 1024)
                print(f"  {lang:30s} ({size_mb:.1f} MB)")
            return

        # Buscar el idioma solicitado
        target = None
        for path, info in loc_files.items():
            if args.lang.lower() in path.lower():
                target = (path, info)
                break

        if not target:
            print(f"Error: idioma '{args.lang}' no encontrado.")
            print("Idiomas disponibles:")
            for path in sorted(loc_files.keys()):
                print(f"  {get_language_from_path(path)}")
            sys.exit(1)

        path, info = target
        lang = get_language_from_path(path)
        print(f"\nExtrayendo: {lang}")
        print(f"  Tamaño comprimido: {info['comp_size'] / (1024*1024):.1f} MB")
        print(f"  Tamaño original:   {info['uncomp_size'] / (1024*1024):.1f} MB")

        data = extract_file(f, info)

    text = data.decode("utf-8-sig")
    lines = text.splitlines()
    print(f"  Líneas: {len(lines):,}")

    output = args.output or "global_from_p4k.ini"
    with open(output, "w", encoding="utf-8-sig", newline="\r\n") as out:
        out.write(text)

    print(f"\nGuardado: {output}")


if __name__ == "__main__":
    main()
