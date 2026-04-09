# Changelog

## v1.7.1 — 2026-04-09

**Build:** 4.7.1-LIVE_11592622 (sin cambio de version del juego)

Correcciones de integridad: variables de mision rotas, tutoriales de controles truncados, descripciones legales desactualizadas y el peso mal calculado del cohete del Boomtube.

**Variables de mision corregidas (>150 correcciones):**
- Varias descripciones de misiones tenian variables internas con nombres mal escritos o traducidos (`Profundidad` en lugar de `Depth`, `Ruta` en lugar de `Route`, `Nombre` en lugar de `Name`, etc.) que impedian al juego sustituirlas correctamente. Ahora el juego muestra el valor real (el nombre del objetivo, el destino, la ubicacion) en vez del texto crudo.
- Nombres con caracteres especiales (tildes, ñ) ya se muestran correctamente en chat, invitaciones de grupo y notificaciones de comms.
- Case mismatches en variables (`|address` vs `|Address`) arreglados en 36 misiones.

**Tutoriales y textos truncados completados:**
- 19 textos de tutoriales de controles (movimiento, disparo, contramedidas, strafing, freelook, rolling, etc.) que aparecian cortados a mitad del combo de teclas. Ahora se leen completos con todas las teclas asignadas.
- 8 simbolos quimicos de minerales (NH₃ amoniaco, CO₂, CH₄ metano, O₂ oxigeno, etc.) que aparecian truncados en la UI.
- 7 descripciones legales (JurisdictionJournals de ArcCorp, Crusader, Hurston, Klescher, microTech, Alianza del Pueblo, UEE) reescritas con toda la tabla legal dinamica (delitos graves, delitos menores, bienes prohibidos, sustancias controladas de clase A/B/C) que CIG habia añadido y que hasta ahora aparecia solo en ingles.
- 5 titulos de contratos Covalex HaulCargo corregidos (ahora muestran "Transporte de Carga" legible en vez de un placeholder roto).
- 10 descripciones del HUD de mineria con parametros que no se sustituian.
- 3 descripciones de misiones Eliminate/Delivery retraducidas al texto oficial.

**Fix en el cohete del Boomtube:**
- La municion del lanzacohetes Boomtube mostraba incorrectamente los stats del arma completa (DPS, Alpha, peso del lanzador) en lugar del peso real del cohete individual. Ahora muestra `Capacidad: 1 | 0.32 kg` correctamente.

**Correcciones de contenido:**
- Eliminadas algunas frases que estaban en la traduccion anterior pero no existen en el juego original (CleanAir, Headhunters), alineando el texto con lo que CIG escribio.

**Estadisticas:**
- Lineas en global.ini: 87,718 (sin cambio respecto a v1.7.0)
- Correcciones manuales totales: 39 → 98

## v1.7.0 — 2026-04-09

**Build:** 4.7.1-LIVE_11592622

Actualizacion al parche 4.7.1 con nuevos contenidos, limpieza de descripciones y mejoras de verificacion.

**Cambios:**
- 35 claves nuevas traducidas del parche 4.7.1:
  - Greycat UTV (vehiculo nuevo) y sus 5 pinturas (Resistor Camo, Bonanza, Wilderness Camo, Reckoner, Keystone)
  - 5 pinturas nuevas para el MISC Hull B (Empyrean, Dusk, Horizon, Keystone, First Light)
  - Rack de misiles integrado del Hull B (S6, 8xS3)
  - 3 pinturas mas: Buccaneer Redline, Hermes Keystone, RAFT Keystone
  - 3 interactores de la torreta tractora (entrar / izquierda / derecha)
  - Nuevo tier "Extrapequeño" para misiones Covalex Recover Cargo
- Journal "Mining Compendium" reescrito con ubicaciones mucho mas detalladas por Lagrange points (ARC-L1..L5, CRU-L1..L5, HUR-L1..L5, MIC-L1..L5), cinturones (Glaciem Ring, cinturon Keeger, anillo de Yela, Akiro Cluster) y estaciones (QV Breaker en Nyx). Minerales comunes traducidos al español (Cobre, Oro, Hierro, Aluminio, Cuarzo, Estaño, Titanio, Tungsteno, Hielo, Silicio).
- 50 descripciones limpiadas de etiquetas en ingles que persistian desde versiones anteriores (Manufacturer:, Item Type:, Damage Reduction:, Tracking Signal:, etc.) en misiles, mochilas, armaduras y pistolas Klaus & Werner.
- Etiqueta `[BP]` añadida a misiones generales del Bounty Hunters Guild que no la tenian.

**Correcciones importantes:**
- Recuperacion de 70 claves perdidas entre versiones del juego. CIG renombro el casing de varias claves de dialogos y notificaciones (ejemplo: `Dlg_SC_mc_lose_Position*` → `Dlg_SC_mc_lose_position*`), y el merge anterior las descartaba silenciosamente dejando solo la version antigua obsoleta.
- Correcciones manuales aplicadas en el orden correcto para evitar prefijos duplicados tipo `[SIG|1|B] [SIG|1|B] Hunter`.

**Estadísticas:**
- Líneas en global.ini: 87,718 (antes 87,683)
- Claves nuevas añadidas vs 4.7.0: 35
- Descripciones limpiadas EN→ES: 50
- Claves recuperadas: 70
- [BP] en titulos: 243

## v1.6.3 — 2026-04-06

**Build:** 4.7.0-LIVE_11576750

**Cambios:**
- Normalizar nombres de producto: mantener nombre EN en modulos mineria y radares
  - "Modulo de sobretension" → "Modulo Surge", "Modulo para Lifeline" → "Modulo Lifeline"
  - "Cazador" → "Hunter", "Profeta" → "Prophet" (radares Balter)
- Labels del MFD traducidos al español (consistencia completa):
  - HEAT→TEMP, SHIELDS→ESCUDOS, WEAPONS→ARMAS, COMMS→COMNS
  - SECURITY→SEGURD., TRGT. STATUS→ESTADO OBJ., TARGET SELECTOR→SEL. OBJ.
  - ENERGÍA→ENERG (acortado para caber en MFD)
- Fix tabla del README que se renderizaba mal en GitHub

**Estadísticas:**
- Líneas en global.ini: 87,683

## v1.6.2 — 2026-04-05

**Build:** 4.7.0-LIVE_11576750

**Cambios:**
- Abreviados nombres de minerales en HUD de mineria para evitar solapamiento (max 15 chars)
  - Minerales ore: "(Mineral)" → "(Mnl)"
  - Minerales raw: "(Bruto)" → "(Bto)"
  - Nombres largos acortados: Tungsteno → Tungsten, Feynmaline → Feynmalin, Hephaestanite sin sufijo
- Recuperadas 10 traducciones que se habian perdido entre versiones (carreras, tutorial, misiones, eventos)

**Estadísticas:**
- Líneas en global.ini: 87,683

## v1.6.1 — 2026-04-04

**Build:** 4.7.0-LIVE_11576750

**Cambios:**
- Traducidas 11 descripciones que estaban completamente en ingles (misiones, armaduras, tutorial)
- Nuevo check de verificacion para detectar descripciones sin traducir

**Estadísticas:**
- Líneas en global.ini: 87,613

## v1.6.0 — 2026-04-04

**Build:** 4.7.0-LIVE_11576750

**Cambios:**
- Nueva version LIVE: la build 11576750 pasa de HOTFIX a LIVE oficial
- Rebuild completo con todas las capas y verificaciones

**Estadísticas:**
- Líneas en global.ini: 87,613

## v1.5.6 — 2026-04-04

**Build:** 4.7.0-HOTFIX_11576750

**Cambios:**
- Fix: la marca `[BP]` en misiones con blueprints ahora aparece siempre al principio del titulo
- Corregidos 195 titulos de misiones que tenian `[BP]` al final o texto en ingles concatenado

**Estadísticas:**
- Líneas en global.ini: 87,683

## v1.5.5 — 2026-04-04

**Build:** 4.7.0-HOTFIX_11576750

**Cambios:**
- Fix: MagnaBloom (Power Plant) ahora muestra stats correctamente (334 componentes con stats)
- Mejorada la cobertura de stats en skins de armas FPS
- Actualizada la tabla de estadisticas del README con numeros verificados

**Estadísticas:**
- Líneas en global.ini: 87,683

## v1.5.4 — 2026-04-04

**Build:** 4.7.0-HOTFIX_11576750

**Cambios:**
- Corregidos 10 nombres de armadura que mostraban la pieza equivocada
  - Calico Tactical/Desert: core mostraba "Piernas" en vez de "Pechera"
  - Aril (5 variantes): piernas mostraban "Brazos" en vez de "Piernas"
  - ADP-mk4 Justified: casco y piernas mostraban "Pechera"
  - Horizon Crusader: casco mostraba "Pechera" en vez de "Casco"

**Estadísticas:**
- Líneas en global.ini: 87,683

## v1.5.3 — 2026-04-04

**Build:** 4.7.0-HOTFIX_11576750

**Cambios:**
- Fix regresión: restaurados todos los datos de componentes de nave
  - Prefijos [CLS|tam|grado] en 383 componentes (Power Plants, Shields, Coolers, QDrives, Radars, Jump Drives)
  - Eliminadas líneas redundantes de Tamaño/Grado/Clase de las descripciones
  - Tracking de misiles IR/EM/CS y tamaño de bombas B# restaurados
  - Avisos [!] en sustancias ilegales restaurados
  - Abreviaturas HUD minería, minerales (Bruto), títulos hauling restaurados
- Abreviados nombres de minerales en el HUD de minería: "(Mineral)" → "(Mnl)" (15 minerales)
- Tungsteno → Tungsten para reducir longitud en scanner

**Estadísticas:**
- Líneas en global.ini: 87,613

## v1.5.2 — 2026-04-04

**Build:** 4.7.0-HOTFIX_11576750

**Cambios:**
- Actualizado al nuevo hotfix 11576750
- Corregido merge: las descripciones de misiones con blueprints ahora conservan la traducción al español completa
- Los títulos de misiones con [BP] ahora muestran el título traducido en español
- 7 traducciones adicionales corregidas (vehículos, ropa, localizaciones)
- Regresiones de traducción eliminadas respecto a versiones anteriores

**Estadísticas:**
- Líneas en global.ini: 87,613

## v1.5.1 — 2026-04-03

**Build:** 4.7.0-HOTFIX_11568150

**Cambios:**
- Corregidos stats de 9 armas de nave que mostraban valores erróneos
  - Revenant, GVSR Repeater, Tarantula GT-870 Mk3, M9A Cannon, entre otras
- YellowJacket GT-210 actualizada con stats correctos (DPS 201.6)
- Verificado contra spviewer y erkul

**Estadísticas:**
- Líneas en global.ini: 87,670

## v1.5.0 — 2026-04-02

**Build:** 4.7.0-HOTFIX_11568150

**Fuentes utilizadas:**
- Thord82: 4.7.0-LIVE (sin cambios)
- MrKraken/StarStrings: 2026-04-01 (build update + mining/missiles)
- ExoAE/ScCompLangPack: v0.10.4 + commits post-release
- BeltaKoda/ScCompLangPackRemix: 4.7.0-LIVE-HOTFIX (2026-03-31)
- Data.p4k: HOTFIX build 11568150 (sin cambios vs LIVE)

**Cambios:**
- Soporte hotfix build 11568150 — ZIP incluye carpetas LIVE/ y HOTFIX/
- 20 misiones con nuevos bloques de blueprints traducidos
- 17 títulos de misiones con etiqueta [BP] añadida
- 22 blueprints actualizados (listas de items cambiaron)
- 14 claves nuevas (blackbox_recover, cfp_defendship Nyx, etc.)
- Corrección radar Pelerous Stealth: grado C → A (fuente: ExoAE)

**Estadísticas:**
- Líneas en global.ini: 87,670
- Blueprints traducidos: 224 descripciones + 216 títulos
- Claves nuevas añadidas: 14

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
