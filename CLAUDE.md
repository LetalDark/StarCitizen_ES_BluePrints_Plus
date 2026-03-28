# Traduccion BluePrints — Star Citizen ES

## Proyecto

Localización al español de Star Citizen. Combina la traducción de Thord82 con la info de blueprints de MrKraken/StarStrings y los textos oficiales del juego (Data.p4k) para generar un `global.ini` final completo.

## Fuentes

| Fuente | Origen | Descripción |
|---|---|---|
| Traducción ES (Thord82) | https://github.com/Thord82/Star_citizen_ES/ | Traducción comunitaria al español |
| Blueprints EN (MrKraken) | https://github.com/MrKraken/StarStrings | Inglés con datos técnicos de blueprints |
| Data.p4k (CIG) | Instalación local del juego | Textos oficiales EN/ES extraídos con `extract_p4k.py` |

## Estructura del proyecto

```
extract_p4k.py                          # Script para extraer global.ini del Data.p4k
versions/
└── {version}/                          # Ej: 4.7.0-hotfix_11545720
    ├── sources/
    │   ├── global_thord82.ini          # Traducción ES de Thord82
    │   ├── global_blueprints.ini       # MrKraken con blueprints (EN)
    │   ├── global_p4k_en.ini           # Inglés oficial extraído del Data.p4k
    │   ├── global_p4k_es.ini           # Español oficial de CIG (parcial)
    │   └── Star_citizen_ES_Thord82.zip # Zip original de Thord82
    ├── diff/
    │   ├── global_diff.ini             # Blueprints extraídos (EN)
    │   ├── global_diff_es.ini          # Blueprints traducidos (ES)
    │   ├── global_diff_p4k.ini         # Claves del p4k que faltan/sin traducir (EN)
    │   └── global_diff_p4k_es.ini      # Claves del p4k traducidas (ES)
    └── output/
        ├── global.ini                  # Final: Thord82 + Blueprints
        ├── global_plus.ini             # Final: Thord82 + Blueprints + p4k traducido
        ├── Star_citizen_ES_BluePrints.zip
        └── Star_citizen_ES_BluePrints_Plus.zip
```

## Flujo de actualización

Cuando se actualicen las fuentes (nueva versión del juego, Thord82 o MrKraken):

### 1. Extracción de fuentes
- Extraer `global_p4k_en.ini` y `global_p4k_es.ini` del Data.p4k con `extract_p4k.py`
- Descargar `global_thord82.ini` del repo de Thord82
- Descargar `global_blueprints.ini` del repo de MrKraken

### 2. Diff de blueprints
- Comparar Thord82 vs MrKraken → `global_diff.ini` (EN)
- Traducir → `global_diff_es.ini` (ES)
- **Revisión del usuario**

### 3. Diff del p4k
- Comparar global.ini (nuestro) vs p4k inglés → `global_diff_p4k.ini` (EN)
- Traducir → `global_diff_p4k_es.ini` (ES)
- **Revisión del usuario**

### 4. Merge
- Thord82 + diff_es → `global.ini`
- global.ini + diff_p4k_es → `global_plus.ini`

### 5. QA y distribución
- Validar consistencia del archivo final
- Generar zips de distribución

## Tabla de routing

| Tarea | Agente |
|---|---|
| Comparar fuentes, detectar diferencias, extraer diffs | Extractor |
| Traducir al español siguiendo estilo Thord82 | Traductor |
| Combinar archivos en global.ini final | Merger |
| Validar consistencia, detectar errores | QA (transversal) |

## extract_p4k.py

Script Python para extraer `global.ini` directamente del `Data.p4k` de Star Citizen.

```bash
python extract_p4k.py --list                        # Ver idiomas disponibles
python extract_p4k.py                               # Extraer inglés
python extract_p4k.py --lang spanish_(spain)         # Extraer español oficial de CIG
python extract_p4k.py -o archivo.ini                 # Elegir nombre de salida
python extract_p4k.py --sc-path "D:/Games/SC/LIVE"   # Ruta manual
```

Requisito: `pip install zstandard`

## Reglas globales

- El usuario siempre valida las traducciones antes del merge
- Los nombres propios del juego (Parallax, Antium, Karna...) nunca se traducen
- Seguir el estilo de Thord82 — ver guía: `.claude/guides/thord82-style.md`
- Formato de archivos: `clave=valor`, codificación UTF-8 con BOM
- Prioridad de traducción: Thord82 > Blueprints traducidos > p4k traducido > inglés original
