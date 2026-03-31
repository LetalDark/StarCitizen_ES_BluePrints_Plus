# Star Citizen - Traduccion ES + BluePrints

Traduccion al español de Star Citizen que combina multiples fuentes para ofrecer la experiencia mas completa posible en español.

## Que hace este proyecto

Star Citizen no tiene traduccion oficial completa al español. Existen proyectos comunitarios que traducen los textos del juego, pero ninguno incluye toda la informacion disponible. Este proyecto:

1. **Parte de la traduccion de Thord82**, la traduccion comunitaria al español mas completa
2. **Añade datos de blueprints** de las misiones que dan planos, con la lista de posibles recompensas traducida al español
3. **Añade clase/grado a los componentes** de naves (coolers, power plants, quantum drives, shields, radars) con prefijo compacto (ej: `[Mil-2A] Bracer` = Militar, Tamaño 2, Grado A)
4. **Añade tracking type a misiles** (IR/EM/CS) y tamaño a bombas (B3/B5/B10) para saber que contramedida usar
5. **Marca misiones con blueprints** con `[BP]` en el titulo para identificarlas rapidamente
6. **Marca sustancias ilegales** con `[!]` para avisar antes de transportarlas
7. **Mejora titulos de hauling** añadiendo la ruta (origen>destino) al titulo del contrato
8. **Acorta nombres largos** en el HUD de mineria para evitar solapamiento (Hephaestanite → Heph, Inestabilidad → Inest:)
9. **Inyecta stats reales de armas FPS** (DPS, Alpha, Velocidad, Rango, Peso, Penetracion) con datos testeados in-game
10. **Inyecta stats de armaduras** (Peso, Reduccion Stun, Reduccion Impacto) y peso de cargadores
11. **Completa claves que faltan** extrayendo los textos oficiales directamente del Data.p4k del juego
12. **Corrige errores** de las fuentes originales (GUIDs nulos, pools faltantes, nombres de armadura incorrectos)

## Fuentes

| Fuente | Descripcion | Enlace |
|---|---|---|
| **Thord82** | Traduccion comunitaria al español. Base principal del proyecto | [github.com/Thord82/Star_citizen_ES](https://github.com/Thord82/Star_citizen_ES/) |
| **MrKraken / StarStrings** | Blueprints de misiones, clase/grado de componentes, mejoras de hauling y QoL | [github.com/MrKraken/StarStrings](https://github.com/MrKraken/StarStrings) |
| **ExoAE / ScCompLangPack** | Clase/grado de componentes, blueprints, avisos de sustancias ilegales | [github.com/ExoAE/ScCompLangPack](https://github.com/ExoAE/ScCompLangPack/) |
| **BeltaKoda / ScCompLangPackRemix** | Tracking type de misiles/bombas, prefijos compactos de componentes | [github.com/BeltaKoda/ScCompLangPackRemix](https://github.com/BeltaKoda/ScCompLangPackRemix) |
| **scunpacked-data** | Stats reales de armas, naves y componentes (mismos datos que erkul/spviewer) | [github.com/StarCitizenWiki/scunpacked-data](https://github.com/StarCitizenWiki/scunpacked-data) |
| **Tests in-game** | DPS, Alpha, Fire Rate medidos in-game (sin y con crafteo) | Spreadsheet comunitario |
| **Data.p4k** | Textos oficiales EN/ES extraidos del propio juego con `extract_p4k.py` | Instalacion local de Star Citizen |

## Que incluye el global.ini final

| # | Capa | Descripcion | Claves | Fuente |
|---|---|---|---|---|
| 1 | Traduccion base ES | Traduccion comunitaria completa al español | 87.585 | Thord82 |
| 2 | Blueprints misiones | Planos posibles en misiones, traducidos al ES + correcciones | 232 | MrKraken + nuestras |
| 3 | Traducciones p4k | Claves que faltan en Thord82, traducidas del ingles oficial | 874 | Data.p4k CIG |
| 4 | [BP] en titulos | Marca `[BP]` en misiones que dan blueprints | 216 | ExoAE |
| 5 | Componentes clase/grado | Prefijo `[Mil-2A]`, `[Civ-1C]`, etc. en componentes de naves | 368 | ExoAE |
| 6 | Misiles y bombas | Tracking type `IR`/`EM`/`CS` en misiles, tamaño `B#` en bombas | 115 | BeltaKoda |
| 7 | Sustancias ilegales | Marca `[!]` en drogas (WiDoW, SLAM, Maze, etc.) | 8 | ExoAE |
| 8 | HUD mining | Abreviaturas para evitar solapamiento (Inest:, Res:) | 2 | MrKraken/ExoAE |
| 9 | Minerales | Hephaestanite → Heph + unificacion de (Raw)/(Crudo) a (Bruto) | 19 | MrKraken/ExoAE |
| 10 | Hauling titles | Ruta origen>destino en titulos de transporte de carga | 5 | MrKraken |
| 11 | Limpieza | Trailing spaces eliminados | 604 | BeltaKoda |
| 12 | Stats armas FPS | DPS, Alpha, Vel, Rango, Peso, Penetracion, modos de fuego | 329 | Tests in-game + scunpacked |
| 13 | Stats cargadores | Peso del cargador | 42 | Tests in-game + scunpacked |
| 14 | Stats armaduras | Peso, Reduccion Stun, Reduccion Impacto | 774 | scunpacked |
| 15 | Correcciones nombres | Nombres de armadura incorrectos (pieza equivocada) | 10 | Verificacion manual |

**Total: 87.656 claves**

## Instalacion

1. Descarga el ZIP de la ultima release
2. Extrae el contenido en la carpeta de Star Citizen (ej: `C:\Program Files\Roberts Space Industries\StarCitizen\`)
3. La estructura queda asi:
```
StarCitizen/
└── LIVE/
    ├── data/Localization/spanish_(spain)/global.ini
    └── user.cfg
```

## Formato de componentes

Los componentes de naves llevan un prefijo con 3 partes: **Clase + Tamaño + Grado**

| Clase | Prefijo |
|---|---|
| Militar | `Mil` |
| Civil | `Civ` |
| Competicion | `Com` |
| Industrial | `Ind` |
| Sigilo | `Sig` |

Grado: A (mejor) a D (peor). Tamaño: 0-4.

Ejemplo: `[Mil-2A] Bracer` = Bracer, clase Militar, tamaño 2, grado A.

## Formato de misiles y bombas

Los misiles llevan un prefijo con el tipo de tracking:

| Prefijo | Tracking | Contramedida |
|---|---|---|
| `IR` | Infrarrojo | Flares |
| `EM` | Electromagnetico | Chaff |
| `CS` | Cross-Section | Sin CM directa |

Las bombas llevan prefijo de tamaño: `B3`, `B5`, `B10`.

Ejemplo: `IR Misil Marksman I` = Marksman tamaño 1, tracking infrarrojo.

## Formato de stats de armas FPS

Las armas muestran modos de fuego etiquetados con stats reales testeados in-game:

```
Fabricante: Kastak Arms
Tipo de artículo: SMG
Clase: Laser
Tamaño de la bateria: 60
Accesorios: optica (S1), Cañon (S1), Debajo del cañon (S1)
[Auto] DPS: 173.3 | Alpha: 13 | 600 m/s | 1200m
[Burst] DPS: 48.8 | Alpha: 39 | 600 m/s | 1200m
[Full] DPS: 44.6 | Alpha: 171.6 | 600 m/s | 1200m
2.8 kg | Dmg/Cargador: 780
Penetracion: 0.5m
```

| Etiqueta | Significado |
|---|---|
| `[Auto]` | Modo automatico |
| `[Semi]` | Modo semiautomatico |
| `[Burst]` | Rafaga |
| `[Beam]` | Rayo continuo |
| `[Full]` | Disparo cargado |
| `[Hot]` | Modo caliente (heat ramp) |
| `[Slug]` | Proyectil unico (escopetas) |
| `[Doble]` | Doble cañon |

Valores grandes usan K: `2.1K`, `95K`, `285K`

## Formato de stats de armaduras

Cada pieza de armadura muestra peso, reduccion de stun y reduccion de impacto:

```
7 kg | Stun: 60% | Impacto: 35%
```

## Herramientas incluidas

### rebuild_outputs.py — Generar global.ini

Regenera el `global.ini` completo desde cero aplicando las 11 capas.

```bash
python rebuild_outputs.py
```

### extract_p4k.py — Extraer localizacion del Data.p4k

Extrae el `global.ini` de cualquier idioma directamente del `Data.p4k` de tu instalacion.

```bash
pip install zstandard
python extract_p4k.py --list                        # Ver idiomas disponibles
python extract_p4k.py                               # Extraer ingles
python extract_p4k.py --lang spanish_(spain)         # Extraer español oficial de CIG
python extract_p4k.py -o archivo.ini                 # Elegir nombre de salida
python extract_p4k.py --sc-path "D:/Games/SC/LIVE"   # Ruta manual
```

### explore_p4k.py — Explorar contenido del Data.p4k

Navega y extrae archivos individuales del Data.p4k.

```bash
python explore_p4k.py --stats                       # Carpetas de primer nivel
python explore_p4k.py --search blueprint             # Buscar archivos por nombre
python explore_p4k.py --extract "Data\Game2.dcb" -o Game2.dcb  # Extraer archivo
```

### parse_dcb.py — Datamining del Game2.dcb

Explora y exporta datos del DataForge Binary (base de datos central de gameplay).

```bash
python parse_dcb.py                                 # Resumen general
python parse_dcb.py --search loot                    # Buscar structs/records
python parse_dcb.py --struct BlueprintRewards        # Ver propiedades de un struct
python parse_dcb.py --dump BlueprintPoolRecord -o x.json  # Exportar a JSON
```

### inject_weapon_stats.py — Inyectar stats en descripciones

Inyecta stats reales de armas FPS, cargadores y armaduras en el global.ini.

```bash
python inject_weapon_stats.py --source tested       # Datos testeados in-game (recomendado)
python inject_weapon_stats.py --source scunpacked    # Datos de scunpacked
python inject_weapon_stats.py --dry-run             # Preview sin escribir
```

### patch_beam_stats.py — Parchear DPS de armas beam

Scunpacked no calcula DPS para armas beam. Este script descarga los JSONs individuales y parchea los agregados.

```bash
python patch_beam_stats.py                          # Parchear fps-items.json y ship-items.json
```

### Herramientas de verificacion

```bash
python audit_diffs.py                               # Auditar diffs: GUIDs nulos, duplicados, tags rotos
python fix_diffs.py                                  # Corregir diffs automaticamente
python verify_blueprints.py                          # Verificar blueprints contra DCB
python compare_coverage.py                           # Comparar cobertura MrKraken vs DCB pool por pool
python extract_mission_blueprints.py                 # Extraer cadena mision→pool→blueprint del DCB
```

## Version actual

- **Star Citizen Alpha 4.7.0-LIVE** (build 11545720)
- Ver [CHANGELOG.md](CHANGELOG.md) para el historial completo
