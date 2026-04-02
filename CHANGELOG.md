# Changelog

## v1.4.2 — 2026-04-01

**Prefijos [CLS|tam|grado], eliminación de líneas redundantes y Disto/masa en Coolers.**

**Nuevo formato de prefijo en nombres de componentes:**
- Antes: `[Civ-2B] Radiance` → Ahora: `[CIV|2|B] Radiance`
- 383 componentes con prefijo (antes 191)
- Bespoke/Hecho a medida = Grade A (confirmado en datos del juego)

**Eliminadas líneas redundantes de descripciones:**
- Tamaño, Grado y Clase eliminados de 377 descripciones de componentes
- Ya se muestran en el prefijo del nombre y en los campos nativos del UI

**Fix: stats de Coolers ampliados:**
- Añadido Disto/Disipa/Rec y masa a los 75 enfriadores

**Estadísticas:**
- Líneas en global.ini: 87,656
- Componentes con prefijo: 383
- Componentes de nave parcheados: 339
- Armas de nave parcheadas: 125
- Armas FPS parcheadas: 328 + 41 cargadores + 774 armaduras + ~1,996 items varios

## v1.4.1 — 2026-04-01

**Stats de componentes de nave — 339 componentes parcheados.**

**Nuevo: componentes de nave (339 descripciones):**
- 6 tipos: Power Plant (78), Quantum Drive (58), Jump Drive (8), Shield (68), Cooler (75), Radar (66)
- Stats extraídos de los datos del juego, verificados contra SPViewer y Erkul
- Quantum Drive incluye rango de eficiencia min-max según tanque QT de la nave

**Estadísticas:**
- Líneas en global.ini: 87,656
- Componentes de nave parcheados: 339
- Armas de nave parcheadas: 125
- Armas FPS parcheadas: 328 + 41 cargadores + 774 armaduras + ~1,996 items varios

## v1.4.0 — 2026-04-01

**Stats de armas de nave — 125 armas parcheadas.**

**Nuevo: armas de nave (125 descripciones):**
- Stats extraídos directamente de los archivos del juego, no de fuentes externas
- 19 tipos de arma cubiertos: LaserRepeater, LaserCannon, LaserGatling, NeutronRepeater, NeutronCannon, PlasmaCannon, BallisticGatling, BallisticRepeater, BallisticCannon, BallisticScatterGun, LaserScattergun, DistortionRepeater, DistortionCannon, DistortionScatterGun, TachyonCannon, MassDriver, MassDriverCannon, ScatterGun
- Datos verificados contra SPViewer: DPS, Alpha, RPM, velocidad, rango, penetración, dispersión, capacitor/munición, masa, HP, firma EM, consumo energía, AoE

**Estadísticas:**
- Líneas en global.ini: 87,656
- Armas de nave parcheadas: 125
- Armas FPS parcheadas: 328 + 41 cargadores + 774 armaduras + ~1,996 items varios

## v1.3.5 — 2026-04-01

**Nuevas inyecciones de stats, corrección de bugs y verificación automática.**

**Nuevas inyecciones (1,222 descripciones adicionales):**
- Ropa y accesorios (615): peso por tipo (camisetas 0.25 kg, chaquetas 0.5 kg, pantalones 0.4 kg, gorros 0.25 kg, calzado 0.3 kg, guantes 0.1 kg, MobiGlas 0.5 kg)
- Items FPS varios (111): peso de granadas, multitools, gadgets, flares, etc.
- Mochilas (102): peso 6 kg
- Accesorios de arma (48): stats de miras, cañones, suppressors (+/- cadencia, daño, dispersión, retroceso...)
- Cargadores extra (47): peso añadido (ParaMed Refill 0.32 kg, P8-AR civilian, etc.)
- Accesorios multitool (5): peso 0.1 kg (cutter, mining, salvage, healing, tractor beam)

**Mejoras en stats existentes:**
- Caída de daño detallada: `[Red. daño] 100% 30m | 50% 45m | 0% 80m`
- Peso desglosado en armas: `Cargado: 6.5 kg | Descargado: 5.2 kg`
- Stats de armadura reposicionados: ahora van después de los metadatos, antes de la descripción
- 19 armaduras con descripción compartida: tabla de pesos por pieza (`*Descripción compartida entre piezas\nCasco: 5 | Pechera: 5 | Brazos: 4 | Piernas: 6 kg`)
- 84 armaduras extra parcheadas (flightsuits, cascos undersuit, suits completos)

**Correcciones:**
- Fix: 6 multitools con texto blueprint sin traducir (XMAnFacturer → Fabricante, XXMAZAZINE → Batería)
- Fix: peso de accesorios multitool después de "Clase:", no antes de "Fabricante:"
- Fix: accesorios multitool ya no heredan peso 2.32 kg de la multitool base
- Fix: cargadores limpiados — stats de arma heredados eliminados de 39 descripciones
- Fix: matching mejorado de magazines (fuzzy suffix swap, mapeo via nombres del juego)
- Fix: matching mejorado de attachments (FieldLite, FarSight skins via word match)
- Fix: armaduras con `Item_Desc` (I mayúscula) ahora se procesan
- Limpieza automática de marcadores X-prefix de MrKraken

**Estadísticas:**
- Líneas en global.ini: 87,656
- Total items con stats: 1,996 (294 armas + 774 armaduras + 47 cargadores + 102 mochilas + 615 ropa + 111 items FPS + 48 accesorios arma + 5 accesorios multitool)

## v1.3.0 — 2026-03-31

**Stats reales de armas FPS, cargadores y armaduras inyectados en las descripciones del juego.**

**Fuentes de datos:**
- Tests in-game: spreadsheet comunitario con DPS/Alpha/FR medidos (sin y con crafteo)
- Data.p4k: nombres en inglés extraídos del juego para mapeo de claves

**Armas FPS (329 descripciones):**
- DPS, Alpha, Velocidad, Rango, Dmg/Cargador, Caída de daño, Peso
- Modos de fuego etiquetados: [Auto] [Semi] [Burst] [Beam] [Full] [Hot] [Slug] [Doble]
- Armas con heat ramp: Fresnel, Pulse, Prism (modo frío + caliente)
- Armas con carga: Scourge, Zenith, Karna, Custodian, Devastator, Salvo, Arrowhead
- Armas con modos seleccionables: P4-AR, R97, Scalpel, Arclight, Gallant, P8-SC
- Daño combinado: Killshot (Físico + Energía)
- Valores K para números grandes (2.1K, 95K, 285K)

**Cargadores (42 descripciones):**
- Peso añadido: "Capacidad: 45 | 0.6 kg"

**Armaduras (774 descripciones):**
- Peso, Reducción Stun y Reducción Impacto por pieza
- Formato: "7 kg | Stun: 60% | Impacto: 35%"

**Correcciones:**
- 10 nombres de armadura corregidos (pieza equivocada en traducción)
  - Calico Tactical/Desert: core decía "Piernas" → "Pechera"
  - Aril x5 variantes: legs decía "Brazos" → "Piernas"
  - ADP-mk4 Justified: helmet/legs decía "Pechera" → "Casco"/"Piernas"
  - Horizon Crusader: helmet decía "Pechera" → "Casco"
- Clase energía simplificada: "energía (Laser)" → "Laser"
- Datos beam parcheados (Quartz 225 DPS, Ripper 165, Parallax 210-260)

**Estadísticas:**
- Líneas en global.ini: 87.656
- Armas FPS parcheadas: 328
- Cargadores parcheados: 42
- Armaduras parcheadas: 774
- Nombres corregidos: 10

## v1.2.3 — 2026-03-30

**Cambios:**
- Nuevo formato de componentes: `[Mil-2A]` en vez de `Mil2A` (mas legible, con separador)

## v1.2.2 — 2026-03-30

**Cambios:**
- Movido tag [BP] al principio del titulo (antes estaba al final)
- Reduce solapamiento con el precio en misiones con titulo largo
- Fix: ruta de localizacion corregida a spanish_(spain) en ZIP y README

**Nota:** el solapamiento del precio en algunas misiones (ej: Shubin Mining Rights 175000) es un bug de CIG que muestra el precio sin abreviar. No es corregible desde global.ini.

## v1.2.1 — 2026-03-30

**Cambios:**
- Añadido prefijo de tracking type (IR/EM/CS) a 109 misiles y torpedos (nombre completo + MFD)
- Añadido prefijo de tamaño (B3/B5/B10) a 6 bombas (nombre completo + MFD)
- Eliminados trailing spaces en 604 claves (limpieza de datos de CIG)
- Renombrada carpeta de version: hotfix → LIVE (mismo build 11545720)

**Estadisticas:**
- Lineas en global.ini: 87.656
- Misiles/bombas con tracking/tamaño: 115
- Trailing spaces eliminados: 604

## v1.2.0 — 2026-03-30

**Fuentes utilizadas:**
- Thord82: 4.7.0-hotfix (2026-03-28)
- MrKraken/StarStrings: v4 (2026-03-28)
- ExoAE/ScCompLangPack: v0.10.4 (2026-03-28) — NUEVA
- BeltaKoda/ScCompLangPackRemix: 4.7.0-LIVE (2026-03-26) — NUEVA
- Data.p4k: 4.7.0-hotfix build 11545720

**Cambios:**
- Unificado a un solo output: global.ini (antes habia global.ini + global_plus.ini)
- Un solo ZIP de distribucion (eliminado BluePrints_Plus.zip)
- Añadidas 2 nuevas fuentes: ExoAE y BeltaKoda (componentes de naves)
- Añadido prefijo clase/grado a 368 componentes de naves (formato Mil2A, Civ1C, etc.)
- Añadida marca [BP] en 216 titulos de misiones con blueprints
- Añadida marca [!] en 8 sustancias ilegales (WiDoW, SLAM, Maze, etc.)
- Acortado HUD de mineria: Inestabilidad → Inest:, Resistencia → Res:
- Acortado Hephaestanite → Heph en commodities
- Unificados 18 minerales raw a (Bruto) en vez de mezcla (Raw)/(Crudo)
- Mejorados 5 titulos de hauling con ruta origen>destino y formato compacto
- Descargado contracts.ini delta de MrKraken como fuente de referencia

**Estadisticas:**
- Lineas en global.ini: 87.656
- Blueprints traducidos: 232
- Componentes con clase/grado: 368
- Pools cubiertos: 45/45

## v1.1.3 — 2026-03-28

**Cambios:**
- Eliminados 4 GUIDs nulos (00000000-...) que aparecían como blueprint en misiones InterSec Patrol y Hockrow P2M3
- Eliminada clave LOC_UNINITIALIZED (no es una misión real)
- Añadidos 3 pools de blueprints que faltaban:
  - Hockrow FacilityDelve P3 Repeat: Zenith Darkwave, Fresnel Molten, Geist ASD Edition (7 bps)
  - Headhunters EliminateSpecific PAF: P8-AR Rifle, Palatino + Moonfall (10 bps)
  - Rayari Irradiated Pearls + Storm (x5 claves): Prism Laser Shotgun, Stirling, Siebe (7 bps)

**Estadísticas:**
- Líneas en global.ini: 87.593
- Líneas en global_plus.ini: 87.656
- Blueprints traducidos: 232
- Pools cubiertos: 45/45 (antes 42/45)

## v1.1.2 — 2026-03-28

**Cambios:**
- Corregido crash del juego con global_plus.ini: line endings corruptos (\r\r\n → \r\n)
- Corregida codificación de global_diff_p4k_es.ini (LF sin BOM → CRLF con BOM)
- Estandarizada estructura de ZIPs: carpeta LIVE/ + user.cfg incluidos en ambos

**Estadísticas:**
- Líneas en global.ini: 87.593
- Líneas en global_plus.ini: 87.657
- Blueprints traducidos: 225
- Claves p4k traducidas: 877

## v1.1.1 — 2026-03-28

**Cambios:**
- Renombrado del repositorio a StarCitizen_ES_BluePrints_Plus
- Añadido README con descripción del proyecto y enlaces a fuentes

## v1.1.0 — 2026-03-28

**Fuentes utilizadas:**
- Thord82: global.ini (2026-03-26)
- MrKraken/StarStrings: global.ini (2026-03-27)
- Data.p4k: SC Alpha 4.7.0-hotfix (build 11545720, 2026-03-28)

**Cambios:**
- Nueva estructura versionada: `versions/{version}/sources|diff|output`
- Nueva variante `global_plus.ini`: incluye traducciones del p4k para claves que faltaban
- 65 claves traducidas desde el p4k (diálogos de carreras, tutorial, UI torretas, descripciones, opciones)
- 63 claves nuevas añadidas que no existían en el global.ini original
- ZIPs con estructura LIVE/ + user.cfg listos para instalar

**Estadísticas:**
- global.ini: 87,593 claves (Thord82 + Blueprints)
- global_plus.ini: 87,656 claves (+ p4k traducido)
- Blueprints traducidos: 226
- Claves p4k traducidas: 65
- Claves p4k nuevas añadidas: 63

## v1.0.0 — 2026-03-28

**Fuentes utilizadas:**
- Thord82: global.ini (2026-03-26)
- MrKraken/StarStrings: global.ini (2026-03-27)

**Cambios:**
- Primera versión: traducción al español de Star Citizen combinando la traducción de Thord82 con info de blueprints de MrKraken
- 226 bloques de blueprints traducidos al español siguiendo el estilo de Thord82
- 8 misiones nuevas (no existían en Thord82) traducidas e incorporadas
- Corrección de estilo: "Camuflaje de Musgo" en lugar de "Camo Musgo"

**Estadísticas:**
- Líneas en global.ini: 87,593
- Blueprints traducidos: 226
- Claves nuevas añadidas: 8
