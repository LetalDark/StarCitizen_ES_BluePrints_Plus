# Star Citizen - ES Plus

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
9. **Inyecta stats reales de armas FPS** (DPS, Alpha, Velocidad, Peso, Caida de daño) con datos testeados in-game
10. **Inyecta stats de armaduras** (Peso, Reduccion Stun, Reduccion Impacto), peso de cargadores, mochilas, ropa, accesorios y mas (1,996 items en total)
11. **Inyecta stats de armas de nave** (DPS, Alpha, RPM, Velocidad, Rango, Penetracion, Capacitor, Masa, HP, EM, AoE) extraidos directamente del Game2.dcb (125 armas)
12. **Completa claves que faltan** extrayendo los textos oficiales directamente del Data.p4k del juego
13. **Corrige errores** de las fuentes originales (GUIDs nulos, pools faltantes, nombres de armadura incorrectos)

## Fuentes

| Fuente | Descripcion | Enlace |
|---|---|---|
| **Thord82** | Traduccion comunitaria al español. Base principal del proyecto | [github.com/Thord82/Star_citizen_ES](https://github.com/Thord82/Star_citizen_ES/) |
| **MrKraken / StarStrings** | Blueprints de misiones, clase/grado de componentes, mejoras de hauling y QoL | [github.com/MrKraken/StarStrings](https://github.com/MrKraken/StarStrings) |
| **ExoAE / ScCompLangPack** | Clase/grado de componentes, blueprints, avisos de sustancias ilegales | [github.com/ExoAE/ScCompLangPack](https://github.com/ExoAE/ScCompLangPack/) |
| **BeltaKoda / ScCompLangPackRemix** | Tracking type de misiles/bombas, prefijos compactos de componentes | [github.com/BeltaKoda/ScCompLangPackRemix](https://github.com/BeltaKoda/ScCompLangPackRemix) |
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
| 12 | Stats armas FPS | DPS, Alpha, Vel, Peso, Caida de daño, modos de fuego | 295 | Tests in-game + Data.p4k |
| 13 | Stats cargadores | Peso del cargador | 47 | Tests in-game |
| 14 | Stats armaduras | Peso, Reduccion Stun, Reduccion Impacto | 774 | Tests in-game + Data.p4k |
| 15 | Stats ropa | Peso de camisetas, chaquetas, pantalones, gorros, calzado, guantes | 615 | Tests in-game |
| 16 | Stats mochilas | Peso 6 kg | 102 | Tests in-game |
| 17 | Stats items FPS | Peso de granadas, multitools, gadgets, flares | 111 | Tests in-game |
| 18 | Stats accesorios arma | Stats de miras, cañones, suppressors | 48 | Tests in-game |
| 19 | Stats accesorios multitool | Peso de cutter, mining, salvage, healing, tractor beam | 5 | Tests in-game |
| 20 | Correcciones nombres | Nombres de armadura incorrectos (pieza equivocada) | 10 | Verificacion manual |
| 21 | Stats armas de nave | DPS, Alpha, RPM, Vel, Rango, Penetracion, Dispersión, Capacitor, Masa, HP, EM, Energía, AoE | 125 | Game2.dcb |

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
[Auto] DPS: 173.3 | Alpha: 13 | 600 m/s
[Burst] DPS: 48.8 | Alpha: 39 | 600 m/s
[Full] DPS: 44.6 | Alpha: 171.6 | 600 m/s
Dmg/Cargador: 780
Cargado: 3.18 kg | Descargado: 2.75 kg
[Red. daño] 100% 15m | 73% 77m | 0% 950m
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

Cada pieza de armadura muestra peso, reduccion de stun y reduccion de impacto justo despues de los metadatos:

```
Mochilas: Medianas, Ligeras
5 kg | Stun: 45% | Impacto: 31%

Fuerza y velocidad se combinan...
```

Las armaduras con descripcion compartida (sin pieza especifica) muestran tabla de pesos:

```
Stun: 45% | Impacto: 31%
*Descripción compartida entre piezas
Casco: 5 | Pechera: 5 | Brazos: 4 | Piernas: 6 kg
```

## Formato de stats de armas de nave

Stats extraidos directamente del Game2.dcb del juego. 6 lineas agrupadas por tipo:

```
DPS: 817.9 | Alpha: 65.43 | 750 RPM
1800 m/s | 3006m | Disp: 0.6
Pen: 1 | Radio: 0.05-0.1
Cap: 75 | Coste: 72.7 | Reg: 15/s | CD: 0.84s
375 kg | HP: 1650 | EM: 304 | Energía: 0.9
```

| Linea | Grupo | Contenido |
|---|---|---|
| 1 | Daño | DPS burst, Alpha por disparo, cadencia |
| 2 | Proyectil | Velocidad, rango maximo, dispersion |
| 3 | Penetracion | Distancia de penetracion, radio de impacto |
| 4 | Sustain | Capacitor (energia) o Municion (balistica) |
| 5 | Fisico/firma | Masa, vida, firma EM, consumo energia |
| 6 | Solo distortion | Radio de explosion (AoE) |

Armas balisticas muestran `Mun: X` en vez de capacitor. Armas de distorsion muestran `Alpha: X Dist` y linea AoE. Scatterguns muestran pellets: `Alpha: 560 (8×70)`.

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

Inyecta stats reales en el global.ini: armas FPS, armaduras, cargadores, mochilas, ropa, accesorios y mas.

```bash
python inject_weapon_stats.py --source tested       # Armas FPS (datos testeados in-game)
python inject_weapon_stats.py --source dcb          # Armas de nave (datos del Game2.dcb)
python inject_weapon_stats.py --dry-run             # Preview sin escribir
python inject_weapon_stats.py --output test.ini     # Escribir a otro fichero
python inject_weapon_stats.py --verify              # 6 checks de calidad + idempotencia
```

### extract_ship_weapons.py — Extraer stats de armas de nave

Extrae stats de todas las armas de nave del Game2.dcb (125 armas, 19 tipos).

```bash
python extract_ship_weapons.py                      # Tabla resumen
python extract_ship_weapons.py --dry-run            # Preview de stats formateados
python extract_ship_weapons.py --json -o out.json   # Exportar datos completos
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
