# Traduccion BluePrints — Star Citizen ES

## Proyecto

Localización al español de Star Citizen. Combina la traducción de Thord82 con la info de blueprints de MrKraken/StarStrings, datos de componentes de ExoAE/BeltaKoda y los textos oficiales del juego (Data.p4k) para generar un `global.ini` final completo.

## Fuentes

| Fuente | Origen | Descripción |
|---|---|---|
| Traducción ES (Thord82) | https://github.com/Thord82/Star_citizen_ES/ | Traducción comunitaria al español |
| Blueprints EN (MrKraken) | https://github.com/MrKraken/StarStrings | Inglés con datos técnicos de blueprints |
| Componentes EN (ExoAE) | https://github.com/ExoAE/ScCompLangPack/ | Clase/grado de componentes + blueprints + QoL tweaks |
| Componentes EN (BeltaKoda) | https://github.com/BeltaKoda/ScCompLangPackRemix | Prefijos compactos de clase/tamaño/grado en componentes |
| Stats testeados in-game | Spreadsheet comunitario (privado) | DPS/Alpha/FR medidos in-game, sin y con crafteo |
| Stats (scunpacked-data) | https://github.com/StarCitizenWiki/scunpacked-data | Fuente alternativa desactivada. Pendiente: --source game desde Game2.dcb |
| Data.p4k (CIG) | Instalación local del juego | Textos oficiales EN/ES extraídos con `extract_p4k.py` |

## Estructura del proyecto

```
extract_p4k.py                          # Script para extraer global.ini del Data.p4k
versions/
└── {version}/                          # Ej: 4.7.0-hotfix_11545720
    ├── sources/
    │   ├── global_thord82.ini          # Traducción ES de Thord82
    │   ├── global_blueprints.ini       # MrKraken con blueprints (EN)
    │   ├── global_mrkraken_delta.ini   # MrKraken contracts.ini (solo delta)
    │   ├── global_exoae.ini            # ExoAE global.ini completo (EN)
    │   ├── global_exoae_delta.ini      # ExoAE modified_global.ini (solo delta)
    │   ├── global_beltakoda.ini        # BeltaKoda global.ini completo (EN)
    │   ├── global_p4k_en.ini           # Inglés oficial extraído del Data.p4k
    │   ├── global_p4k_es.ini           # Español oficial de CIG (parcial)
    │   ├── Star_citizen_ES_Thord82.zip # Zip original de Thord82
    │   ├── MrKrakenStarStrings-*.zip   # Zip release de MrKraken
    │   ├── ScCompLangPack_ExoAE.zip    # Zip release de ExoAE
    │   ├── ScCompLangPackRemix_BeltaKoda.zip # Zip release de BeltaKoda
    │   ├── scunpacked/
    │   │   ├── fps-items.json          # Stats armas FPS, armaduras, accesorios
    │   │   ├── ship-items.json         # Stats armas nave, componentes, misiles
    │   │   ├── ships.json              # Stats de naves/vehículos
    │   │   └── items_beam/             # JSONs individuales de armas beam (caché)
    │   └── tested/                     # Stats testeados in-game (fuente alternativa)
    │       ├── sin_crafteo/            # 23 pestañas: Item, TTK, Armor, Recoil, etc.
    │       └── con_crafteo/            # Mismas pestañas con crafteo calidad 1000
    ├── diff/
    │   ├── global_diff.ini             # Blueprints extraídos (EN)
    │   ├── global_diff_es.ini          # Blueprints traducidos (ES)
    │   ├── global_diff_p4k.ini         # Claves del p4k que faltan/sin traducir (EN)
    │   └── global_diff_p4k_es.ini      # Claves del p4k traducidas (ES)
    └── output/
        ├── global.ini                  # Final: Thord82 + Blueprints + p4k
        └── Star_citizen_ES_BluePrints.zip
```

## Flujo de actualización

Cuando se actualicen las fuentes (nueva versión del juego, Thord82 o MrKraken):

### 1. Extracción de fuentes
- Extraer `global_p4k_en.ini` y `global_p4k_es.ini` del Data.p4k con `extract_p4k.py`
- Descargar `global_thord82.ini` del repo de Thord82
- Descargar `global_blueprints.ini` y `contracts.ini` del repo de MrKraken
- Descargar release y `modified_global.ini` de ExoAE
- Descargar release de BeltaKoda

### 2. Diff de blueprints
- Comparar Thord82 vs MrKraken → `global_diff.ini` (EN)
- Traducir → `global_diff_es.ini` (ES)
- **Revisión del usuario**

### 3. Diff del p4k
- Comparar global.ini (nuestro) vs p4k inglés → `global_diff_p4k.ini` (EN)
- Traducir → `global_diff_p4k_es.ini` (ES)
- **Revisión del usuario**

### 4. Merge
- Thord82 + diff_es + diff_p4k_es → `global.ini`

### 5. Inyección de stats reales
- `python inject_weapon_stats.py --source tested` — inyectar stats desde Excel testeado + Data.p4k
- Aplica: armas FPS (328), cargadores (41), armaduras (774), 10 name fixes
- **Revisión del usuario** in-game

### 6. Verificación contra DCB
- Extraer Game2.dcb del Data.p4k
- Verificar que todos los BlueprintPoolRecords (45 pools) están cubiertos
- Cruzar misión → pool → blueprints contra los diffs
- Herramientas: `parse_dcb.py`, `extract_mission_blueprints.py`, `verify_blueprints.py`

### 7. QA y distribución
- Validar consistencia del archivo final (sin GUIDs nulos, sin duplicados)
- Generar zip de distribución

## Tabla de routing

| Tarea | Agente |
|---|---|
| Comparar fuentes, detectar diferencias, extraer diffs | Extractor |
| Traducir al español siguiendo estilo Thord82 | Traductor |
| Combinar archivos en global.ini final | Merger |
| Validar consistencia, detectar errores | QA (transversal) |

## Herramientas

### extract_p4k.py — Extraer localización del Data.p4k

```bash
python extract_p4k.py --list                        # Ver idiomas disponibles
python extract_p4k.py                               # Extraer inglés
python extract_p4k.py --lang spanish_(spain)         # Extraer español oficial de CIG
python extract_p4k.py -o archivo.ini                 # Elegir nombre de salida
python extract_p4k.py --sc-path "D:/Games/SC/LIVE"   # Ruta manual
```

Requisito: `pip install zstandard`

### explore_p4k.py — Explorar contenido del Data.p4k

```bash
python explore_p4k.py --stats                       # Carpetas de primer nivel
python explore_p4k.py --search blueprint             # Buscar archivos por nombre
python explore_p4k.py --extract "Data\Game2.dcb" -o Game2.dcb  # Extraer archivo
```

### parse_dcb.py — Datamining del Game2.dcb (DataCore Binary)

```bash
python parse_dcb.py                                 # Resumen general
python parse_dcb.py --search loot                    # Buscar structs/records
python parse_dcb.py --struct BlueprintRewards        # Ver propiedades de un struct
python parse_dcb.py --dump BlueprintPoolRecord -o x.json  # Exportar a JSON
```

Referencia completa de datos del DCB: `.claude/guides/dcb-data.md`

### patch_beam_stats.py — Parchear DPS de armas beam (fuente alternativa)

Solo necesario para `--source scunpacked` (desactivado). Con `--source tested` los beams vienen del Excel.

```bash
python patch_beam_stats.py                          # Parchear fps-items.json y ship-items.json
```

### inject_weapon_stats.py — Inyectar stats en descripciones

```bash
python inject_weapon_stats.py --source tested       # Datos testeados in-game (recomendado)
python inject_weapon_stats.py --source game           # Pendiente: desde archivos del juego
python inject_weapon_stats.py --dry-run             # Preview sin escribir
python inject_weapon_stats.py --version 4.7.0-LIVE_11545720  # Versión específica
```

Fuentes: Excel testeado (DPS, Alpha, modos) + Data.p4k (mapeo nombres).
Inyecta: armas FPS (328), cargadores (42), armaduras (774).

Formato de stats inyectados — ver guía: `.claude/guides/weapon-stats-format.md`

## Reglas globales

- El usuario siempre valida las traducciones antes del merge
- Los nombres propios del juego (Parallax, Antium, Karna...) nunca se traducen
- Seguir el estilo de Thord82 — ver guía: `.claude/guides/thord82-style.md`
- Datos de gameplay del DCB — ver guía: `.claude/guides/dcb-data.md`
- Formato de archivos: `clave=valor`, codificación UTF-8 con BOM
- Prioridad de traducción: Thord82 > Blueprints traducidos > p4k traducido > inglés original
