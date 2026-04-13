# Star Citizen - ES Plus

Traduccion al español de Star Citizen que combina multiples fuentes para ofrecer la experiencia mas completa posible en español.

## Que hace este proyecto

Star Citizen no tiene traduccion oficial completa al español. Existen proyectos comunitarios que traducen los textos del juego, pero ninguno incluye toda la informacion disponible. Este proyecto:

1. **Hereda y construye sobre la traduccion comunitaria de Thord82** como base evolutiva. Desde v1.9.0 el proyecto es independiente: cada version arranca de la anterior y aplica solo el delta del juego, sin re-mergear automaticamente fuentes externas
2. **Añade datos de blueprints** de las misiones que dan planos, con la lista de posibles recompensas traducida al español
3. **Añade clase/grado a los componentes** de naves (coolers, power plants, quantum drives, shields, radars) con prefijo compacto (ej: `[MIL|2|A] Bracer` = Militar, Tamaño 2, Grado A)
4. **Añade tracking type a misiles** (IR/EM/CS) y tamaño a bombas (B3/B5/B10) para saber que contramedida usar
5. **Marca misiones con blueprints** con `[BP]` al principio del titulo para identificarlas rapidamente
6. **Marca sustancias ilegales** con `[!]` para avisar antes de transportarlas
7. **Mejora titulos de hauling** añadiendo la ruta (origen>destino) al titulo del contrato
8. **Acorta nombres largos** en el HUD de mineria para evitar solapamiento (Hephaestanite → Heph, ore → (Mnl), raw → (Bto), Inestabilidad → Inest:)
9. **Reestructura el compendio de mineria** del diario del juego en 6 secciones por rareza (Legendario, Epico, Raro, Poco comun, Comun, Minables a mano) con orden alfabetico dentro
10. **Inyecta stats reales de armas FPS** (DPS, Alpha, Velocidad, Peso, Caida de daño) con datos testeados in-game
11. **Inyecta stats de armaduras** (Peso, Reduccion Stun, Reduccion Impacto), peso de cargadores, mochilas, ropa, accesorios y mas
12. **Inyecta stats de armas de nave** (DPS, Alpha, RPM, Velocidad, Rango, Penetracion, Capacitor, Masa, HP, EM, AoE) extraidos directamente de los datos del juego (122 armas)
13. **Inyecta stats de componentes de nave** (334 componentes): Power Plants, Quantum Drives, Jump Drives, Shields, Coolers y Radars con datos del juego
14. **Completa claves que faltan** extrayendo los textos oficiales directamente del Data.p4k del juego
15. **Corrige errores** de las fuentes originales (GUIDs nulos, pools faltantes, nombres de armadura incorrectos)
16. **Limpieza automatica** de claves obsoletas que el juego ya no usa (renombres antiguos, contenido retirado), con migracion automatica de las traducciones a los nombres nuevos

## Fuentes y agradecimientos

Aunque desde v1.9.0 el proyecto es independiente y solo recibe deltas automaticos del juego, su base y la inspiracion para muchas de las funcionalidades vienen de los siguientes proyectos comunitarios. Sin su trabajo este parche no existiria — el credito y el reconocimiento les pertenecen.

| Fuente | Descripcion | Enlace |
|---|---|---|
| **Thord82** | Traduccion comunitaria al español. Base evolutiva heredada del proyecto | [github.com/Thord82/Star_citizen_ES](https://github.com/Thord82/Star_citizen_ES/) |
| **MrKraken / StarStrings** | Blueprints de misiones, clase/grado de componentes, mejoras de hauling y QoL | [github.com/MrKraken/StarStrings](https://github.com/MrKraken/StarStrings) |
| **ExoAE / ScCompLangPack** | Clase/grado de componentes, blueprints, avisos de sustancias ilegales | [github.com/ExoAE/ScCompLangPack](https://github.com/ExoAE/ScCompLangPack/) |
| **BeltaKoda / ScCompLangPackRemix** | Tracking type de misiles/bombas, prefijos compactos de componentes | [github.com/BeltaKoda/ScCompLangPackRemix](https://github.com/BeltaKoda/ScCompLangPackRemix) |
| **Tests in-game** | DPS, Alpha, Fire Rate medidos in-game (sin y con crafteo) | Spreadsheet comunitario |
| **Data.p4k** | Textos oficiales EN/ES extraidos del propio juego | Instalacion local de Star Citizen |

## Que incluye el global.ini final

| # | Capa | Descripcion | Claves | Fuente |
|---|---|---|---|---|
| 1 | Traduccion base ES | Traduccion comunitaria completa al español | 87.591 | Thord82 |
| 2 | Blueprints misiones | Planos posibles en misiones, traducidos al ES + correcciones | 502 | MrKraken + nuestras |
| 3 | Traducciones p4k | Claves que faltan en Thord82, traducidas del ingles oficial | 82 | Data.p4k CIG |
| 4 | [BP] en titulos | Marca `[BP]` en misiones que dan blueprints | 234 | datos del juego + ExoAE |
| 5 | Componentes clase/grado | Prefijo `[MIL\|2\|A]`, `[CIV\|1\|C]`, etc. en componentes de naves | 382 | datos del juego |
| 6 | Misiles y bombas | Tracking type `IR`/`EM`/`CS` en misiles, tamaño `B#` en bombas (estilo uniforme) | 136 | datos del juego |
| 7 | Sustancias ilegales | Marca `[!]` en drogas (WiDoW, SLAM, Maze, etc.) | 8 | ExoAE |
| 8 | HUD mining | Abreviaturas para evitar solapamiento (Inest:, Res:) | 2 | MrKraken/ExoAE |
| 9 | Minerales | Heph + ore (Mnl) + raw (Bto) + ajustes nombres largos (max 14 chars) | 47 | MrKraken/ExoAE |
| 10 | Hauling titles | Ruta origen>destino en titulos de transporte de carga | 5 | MrKraken |
| 11 | Limpieza | Trailing spaces eliminados | 607 | BeltaKoda |
| 12 | Stats armas FPS | DPS, Alpha, Vel, Peso, Caida de daño, modos de fuego | 295 | Tests in-game + Data.p4k |
| 13 | Stats cargadores | Peso del cargador | 42 | Tests in-game |
| 14 | Stats armaduras | Peso, Reduccion Stun, Reduccion Impacto | 713 | Tests in-game + Data.p4k |
| 15 | Stats ropa y accesorios | Peso de ropa, calzado, mochilas, accesorios arma, multitools, granadas y mas | 910 | Tests in-game |
| 16 | Correcciones manuales | Nombres armadura normalizados al formato `<Set> (Parte)`, descripciones, placeholders de misiones, traducciones recuperadas | 161 | Verificacion manual |
| 17 | Stats armas de nave | DPS, Alpha, RPM, Vel, Rango, Penetracion, Dispersión, Capacitor, Masa, HP, EM, Energía, AoE | 122 | Datos del juego |
| 18 | Stats componentes nave | Power Plants, Quantum Drives, Jump Drives, Shields, Coolers, Radars | 334 | Datos del juego |

**Total: 87,626 claves**

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

Los componentes de naves llevan un prefijo con 3 partes separadas por `|`: **Clase + Tamaño + Grado**

| Clase | Prefijo |
|---|---|
| Militar | `MIL` |
| Civil | `CIV` |
| Competicion | `COM` |
| Industrial | `IND` |
| Sigilo | `SIG` |

Grado: A (mejor) a D (peor). Tamaño: 0-4.

Ejemplo: `[MIL|2|A] Bracer` = Bracer, clase Militar, tamaño 2, grado A.

Las lineas de Tamaño, Grado y Clase se han eliminado de las descripciones ya que esta informacion se muestra en el prefijo del nombre y en los campos nativos del UI del juego.

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

## Formato de nombres de armadura

Desde v1.9.5 todas las piezas de armadura siguen el formato unificado `<Set> <Variante> (Parte)`, mirror del inglés oficial del juego. Las 4 partes usan etiquetas en español consistentes:

- **Pecho** (core)
- **Brazos** (arms)
- **Piernas** (legs)
- **Casco** (helmet)

Las variantes "Modificado/a/s" concuerdan en género con la parte: `(Pecho Modificado)`, `(Piernas Modificadas)`, `(Brazos Modificados)`, `(Casco Modificado)`.

Ejemplos: `Citadel Dark Red (Pecho)`, `Aves Starchaser (Piernas)`, `ADP-mk4 Big Boss (Casco)`, `DCP Camuflaje Cazador (Brazos)`, `ADP-mk4 (Pecho Modificado)`.

Los trajes tipo pantalón (Antium, Palatino) usan `(Pantalones)` como variante para reflejar que son prendas de tela, no armadura rígida.

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
Casco: 5 | Pecho: 5 | Brazos: 4 | Piernas: 6 kg
```

## Formato de stats de armas de nave

Stats extraidos directamente de los datos del juego. 6 lineas agrupadas por tipo:

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

## Formato de stats de componentes de nave

Stats extraidos de los datos del juego. Cada tipo de componente muestra stats relevantes:

**Power Plant:**
```
Energía: 25 | HP: 2700
Disto: 13K | Disipa: 866.67/s | Rec: 19.5s
EM/Seg: 496 | EM Decay: 0.15
2200 kg
```

**Quantum Drive:**
```
Vel: 324 Mm/s | Consumo: 0.024
Carga: 6s | Enfriamiento: 22.86s
Disto: 7K | Disipa: 466.67/s
440 kg | HP: 840 | EM: 26300 | Energía: 4
[Eficiencia/tanque] 1.65 SCU: 1.2 | 5.6 SCU: 4.2
```

**Shield:**
```
Escudo: 13.2K | Regen: 1452/s | Tiempo: 9.1s
Retardo: 5.27s | Caído: 10.5s
Resist. Energía: -10%
Energía: 1-4 | EM: 1650 | HP: 750
```

**Cooler:**
```
Enfriamiento: 60
Energía: 2-5 | EM: 2480 | IR: 12700 | HP: 1800
Disto: 8.5K | Disipa: 566.67/s | Rec: 19.5s
1900 kg
```

**Radar:**
```
Asist: 1300-2184m | Margen: 90m
IR: 90% | EM: 90% | CS: 90% | RS: 100%
Energía: 2-8 | EM: 2160 | HP: 1380
```

**Jump Drive:**
```
Calibración: 0.22 | Alineación: 0.2
Combustible: x1.5
Disto: 1.2K | Disipa: 240/s
320 kg | HP: 350
```

La eficiencia del Quantum Drive depende del tanque cuantico de la nave. Se muestra el rango min-max para todas las naves compatibles con ese tamaño de QDrive.

## Version actual

- **Star Citizen Alpha 4.7.1-HOTFIX** (build 11617053)
- Ver [CHANGELOG.md](CHANGELOG.md) para el historial completo
