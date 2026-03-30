# Changelog

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
- Pools cubiertos: 45/45 del DCB

## v1.1.3 — 2026-03-28

**Cambios:**
- Eliminados 4 GUIDs nulos (00000000-...) que aparecían como blueprint en misiones InterSec Patrol y Hockrow P2M3
- Eliminada clave LOC_UNINITIALIZED (no es una misión real)
- Añadidos 3 pools de blueprints que faltaban (verificados contra Game2.dcb):
  - Hockrow FacilityDelve P3 Repeat: Zenith Darkwave, Fresnel Molten, Geist ASD Edition (7 bps)
  - Headhunters EliminateSpecific PAF: P8-AR Rifle, Palatino + Moonfall (10 bps)
  - Rayari Irradiated Pearls + Storm (x5 claves): Prism Laser Shotgun, Stirling, Siebe (7 bps)
- Nueva herramienta parse_dcb.py para datamining del Game2.dcb (DataCore Binary)
- Nueva herramienta explore_p4k.py para explorar contenido del Data.p4k

**Estadísticas:**
- Líneas en global.ini: 87.593
- Líneas en global_plus.ini: 87.656
- Blueprints traducidos: 232
- Pools cubiertos: 45/45 del DCB (antes 42/45)

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
- Nueva herramienta `extract_p4k.py` para extraer global.ini directamente del Data.p4k del juego
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
