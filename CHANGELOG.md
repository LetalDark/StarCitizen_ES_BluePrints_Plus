# Changelog

## v1.11.2 — 2026-05-02

**Builds:** 4.7.2-LIVE_11715810 + 4.8.0-PTU_11768487 (sin cambios de upstream).

Fix de dos etiquetas de la barra superior del panel de Ingeniería de las
naves que se solapaban con el campo vecino. Se aplica a ambos canales
(LIVE y PTU).

**Cambios — comunes a LIVE 4.7.2 y PTU 4.8.0:**
- **Barra superior de Ingeniería.** Los labels de la fila de recursos no
  cabían en su columna y desbordaban contra "Soporte Vital":
  - `Sistema de refrigeración` → `Refrigeración` (pisaba la etiqueta vecina).
  - `Combustible de hidrógeno` → `Hidrógeno` (se cortaba al final de la fila).

## v1.11.1 — 2026-05-02

**Builds:** 4.7.2-LIVE_11715810 + 4.8.0-PTU_11768487 (sin cambios de upstream).

Fix de varios textos del mobiGlas que desbordaban su contenedor en la
interfaz en español. Se aplica a ambos canales (LIVE y PTU).

**Cambios — comunes a LIVE 4.7.2 y PTU 4.8.0:**
- **Panel del Administrador de Contratos.** Los labels del panel de
  detalles eran demasiado largos para el ancho de columna que CIG diseñó
  para los textos en inglés, y empujaban los valores a la siguiente
  línea, descuadrando la rejilla:
  - `Recompensa` → `Pago` (cabe en la misma línea que el importe).
  - `Disponibilidad Del Contrato` → `Disponibilidad` (cabe en la misma
    línea que el cronómetro; elimina la mayúscula incorrecta de "Del").
  - `Plazo Del Contrato` → `Plazo` (consistencia con el resto del panel).
- **Barra inferior del mobiGlas.** Botones que se salían del contenedor:
  - `Comunicaciones` → `Comunicación` (botón pensado para "Comms").
  - `Bizum` → `Cartera`. La app de gestión de aUEC pasa a llamarse
    Cartera, un término genérico de monedero digital que mantiene el
    significado original ("Wallet") sin usar una marca comercial real.

## v1.11.0 — 2026-05-02

**Builds:** 4.7.2-LIVE_11715810 (sin cambios) + 4.8.0-PTU_11768487 (nuevo).

Actualización del canal PTU al último build 4.8.0 (11768487). El canal
LIVE 4.7.2 no recibe cambios — su `global.ini` es idéntico a v1.10.1.

**Cambios — canal PTU 4.8.0:**
- **30 claves nuevas traducidas:**
  - 26 líneas de voz de la nueva misión Squadron Battle del *Tranquility*
    (Captain Aniss Martel de la facción **People's Alliance**, enfrentamiento
    con la facción **Shattered Blade** y posterior ataque del destructor
    Vanduul **Mauler** en sistema **Nyx** — incluye rescate del piloto Gabe).
  - Reputación de la nueva facción **People's Alliance**.
  - Objetivo corto del refuel de naves (`ShipRefuel_obj_short`).
  - Etiqueta HUD `Resistencia anti-G prevista`.
- **4 typos del juego corregidos** que CIG arregló en este build:
  `Allrighty`→`Alrighty`, `hotstiles`→`hostiles`, `Suport`→`Support`, y
  ajuste del prefijo del objetivo `Intersec_TSG_Assist_Solo_obj_short_01`.
- **3 errores heredados corregidos** en español:
  - Nombre de la nave `Tranqulity` → `Tranquility` en líneas de fallo
    de misión de Captain Martel.
  - Tags de director (`<death scream>`, `<scream>`) traducidos a
    `<grito de muerte>` / `<grito>` siguiendo la convención usada
    históricamente en el archivo (los corchetes son de CIG, no se tocan).
- **Fix de UI: cabecera del Administrador de Flota.** En 4.8.0 CIG añadió
  un nuevo checkbox "Mostrar naves locales" pegado al título de la
  ventana, y los textos en español no cabían (se solapaban). Hemos
  abreviado el título a "Admin. de Flota" y el checkbox a "Naves locales"
  para que ambos quepan correctamente en la cabecera.

**Cambios — canal LIVE 4.7.2:**
- Sin cambios (`global.ini` idéntico a v1.10.1).

## v1.10.1 — 2026-04-30

**Builds:** 4.7.2-LIVE_11715810 + 4.8.0-PTU_11753569 (sin cambios de upstream).

Hotfix puntual del PTU 4.8: las 6 variantes de la misión de
HeadHunters "Defender ubicación frente a aspirantes/rivales/mercenarios"
mostraban en la oferta de contrato la lista de planos pegada al
título, saliéndose del recuadro. La descripción seguía bien; el título
queda ahora limpio y la lista solo aparece en la descripción.

**Cambios — canal PTU 4.8.0:**
- Fix títulos de las 6 variantes de misión "Defender ~ubicación~" (E/H/M/S/VE/VH)
  de HeadHunters: el bloque "Posibles Planos" ya no aparece en el título.

**Cambios — canal LIVE 4.7.2:**
- Sin cambios (`global.ini` idéntico a v1.10.0).

## v1.10.0 — 2026-04-30

**Builds:** 4.7.2-LIVE_11715810 + 4.8.0-PTU_11753569

Primer release dual-canal del proyecto. Coexisten un LIVE estable
(4.7.2 build 11715810) y un PTU de pruebas (4.8.0 build 11753569) con
contenido nuevo masivo de la actualización 4.8. El ZIP de distribución
contiene ambos `global.ini` en subcarpetas separadas (`LIVE/` y `PTU/`)
para que cada usuario instale el que corresponde a su rama del RSI
Launcher.

**Cambios principales — canal LIVE 4.7.2:**
- `global.ini` prácticamente idéntico a v1.9.11 (mismo contenido,
  reorganización interna de carpetas).
- Mejora de hauling: los títulos de transporte de carga Covalex ahora
  preservan la marca `[BP]` cuando el contrato da planos como recompensa
  (antes la perdían silenciosamente al reescribir el título con la ruta).

**Cambios principales — canal PTU 4.8.0:**
- **+1 009 claves nuevas** del enorme parche 4.8 traducidas con un
  glosario consolidado (Antiaéreo, Tanque pesado/ligero, Caza pesado,
  Pathfinder → Explorador, Subtraje, Casco de vuelo, Repostaje, Boquilla
  de combustible, Cañonera, etc.).
- **Sistema de repostaje completo** traducido: 33 claves de UI (Boquilla
  de combustible, Módulo de combustible, Cancelar repostaje, Distribución
  de combustible, etc.).
- **Diálogos NPC en misiones** (309 líneas habladas): conversaciones
  cortas estilo radio bajo presión durante misiones Intersec, Foxwell,
  TheCollector (con tono pidgin-Banu de Wikelo preservado), UWC, TSG.
- **Misiones nuevas con título y descripción**: Intersec_TSG_*,
  Foxwell_DefendDestructibleEntites_*, FTLCourier_*, HeadHunters_*,
  TheCollector_*, Adagio_Industrial_Salvage_*, Eckhart_*.
- **Re-categorización masiva de naves** (126 descripciones): el Focus
  de combate y especialización ha sido rehecho para precisar el rol
  (Cyclone AA → Antiaéreo, Storm → Tanque ligero, Nova → Tanque pesado,
  Vanguard Sentinel → Heavy Fighter, Perseus → Cañonera pesada, etc.).
- **Destructor Vanduul Mauler** (nueva nave capital enemiga) con sus
  componentes Gen2 y armas IGNITER/STRIKER/RAGE/ANNIHILATOR/ERADICATOR.
- **Crafting UI** (20 slots): Iris de apertura, Barras colectoras,
  Disipador térmico, Procesador de señal, etc.
- **Stats GPP nuevos** (15): Integridad, Eficiencia, Radio, Salud máxima,
  Pips de energía, Consumo de combustible cuántico, etc.
- **Minerales mineabletype** (35 primarios + variantes): Agricium,
  Aluminium, Aslarite, etc. (nombres propios sin traducir).
- **Items commodities** (23): contramedidas (señuelos/bengalas),
  munición, ranking ShatteredBlade, etc.
- **Foundation Festival** + variantes Purgatory Camo de equipo cosmético
  (Aopoa, Anvil, MISC, RSI, Tumbril).

**"Posibles Planos" auto-generados (nuevo):**
- Las descripciones de misiones que dan planos ahora incluyen un bloque
  "Posibles Planos" con la lista de items que la misión puede recompensar,
  en español. Antes esta lista solo aparecía en las misiones que existían
  en versiones históricas; ahora se genera automáticamente para
  cualquier misión con planos en los datos del juego.
- Resultado en PTU 4.8: **291** misiones con `[BP]` en título (+57
  nuevas etiquetadas), **385** descripciones con "Posibles Planos"
  (+59 vs v1.9.11). Cobertura efectiva del 99 %; las 5 misiones
  restantes son casos en los que el propio juego no tiene aún el
  nombre localizado del item recompensa
  (`salvage_modifier_scraper_*`, etc.).
- 194 nuevos blueprints añadidos a los pools de misión por la
  actualización 4.8: 161 (83 %) ya tienen su nombre español;
  33 (17 %) están a la espera del nombre localizado oficial.

**Estadísticas:**
- Líneas en `global.ini` LIVE 4.7.2: 87 626 (sin cambio neto vs v1.9.11).
- Líneas en `global.ini` PTU 4.8.0: 88 586 (+960 netas).
- Claves nuevas en PTU vs LIVE: 1 009.
- Cobertura de blueprints en misiones: 99 % (PTU) / 100 % (LIVE).

## v1.9.11 — 2026-04-26

**Build:** 4.7.2-HOTFIX_11715810

Patch sobre v1.9.10 para arreglar un bug visual del HUD en misiones de patrulla `[BP] Patrullar...`. Durante el primer objetivo el juego mostraba "Esperar el despliegue: %ls" con el `%ls` literal en pantalla (un placeholder técnico que el motor del juego debería sustituir pero no lo hace en español). En inglés el motor lo sustituye por una cadena vacía y el bug pasa desapercibido. La traducción ahora omite el placeholder y queda solo "Esperar el despliegue", limpio. El cronómetro de la misión sigue apareciendo aparte en su widget.

**Cambios:**
- `SP_Wait_Obj`: "Esperar el despliegue: %ls" → "Esperar el despliegue".

**Estadísticas:**
- Líneas en global.ini: 87 626 (sin cambio)
- Cobertura de blueprints en misiones: 100 %

## v1.9.10 — 2026-04-25

**Build:** 4.7.2-HOTFIX_11715810

Release de compatibilidad con el nuevo hotfix 4.7.2-HOTFIX_11715810. CIG ha publicado un hotfix puramente técnico (servidor, netcode, motor): no ha tocado ningún texto en los archivos de localización del juego ni los datos de gameplay (los archivos internos son byte-idénticos al build 11674325).

El `global.ini` distribuido en este release es prácticamente idéntico al de v1.9.8 (mismo MD5). Frente a v1.9.9, se uniforma el formato de stats de dos armas (`item_DescGATS_BallisticGatling_S1` y `item_DescTOAG_LaserGatling_S2`) al formato `[Auto]` consistente con el resto del catálogo de armas de nave.

**Estadísticas:**
- Líneas en global.ini: 87 626 (igual que v1.9.6/7/8/9)
- Cobertura de blueprints en misiones: 100 %

## v1.9.9 — 2026-04-22

**Build:** 4.7.2-LIVE_11674325

Release de compatibilidad con la promoción del build 11674325 de 4.7.1-HOTFIX a 4.7.2-LIVE. El anuncio oficial del 4.7.2 (Nyx Mission Pack 2: nuevas misiones de Courier, Recover Cargo, Ship Wave Attack, Bounty Kill Ship, Bombing Run y Paid Salvage) se activa server-side sobre el mismo build: los archivos de localización y los datos de gameplay del juego no han cambiado. Las misiones nuevas reutilizan plantillas que ya estaban cubiertas y etiquetadas con `[BP]` (CFP, Foxwell, Headhunters, Intersec, Shubin, RDC, BHG…), así que la cobertura de blueprints es del 100 % desde el primer momento.

El `global.ini` es prácticamente idéntico al de v1.9.8, con un microdelta: dos armas de nave (el gatling láser Torral Aggregate S2 y el gatling balístico Gallenson Tactical S1) pasan al formato de stats multilínea nuevo que ya usaban el resto de armas.

**Estadísticas:**
- Líneas en global.ini: 87 626 (igual que v1.9.8)
- Cobertura de blueprints en misiones: 100 %

## v1.9.8 — 2026-04-19

**Build:** 4.7.1-HOTFIX_11674325

Release de compatibilidad con el nuevo hotfix 4.7.1-HOTFIX_11674325. CIG ha publicado otro hotfix puramente técnico (servidor, netcode, motor): no ha tocado ningún texto en los archivos de localización del juego ni los datos de gameplay.

El `global.ini` distribuido en este release es **byte-idéntico** al de v1.9.7, pero se publica con el build nuevo en el ZIP para que no haya dudas sobre compatibilidad. Si ya tenías v1.9.7 instalado, sigue siendo válido sobre 11674325 y no hace falta actualizar.

**Estadísticas:**
- Líneas en global.ini: 87 626 (igual que v1.9.7)

## v1.9.7 — 2026-04-15

**Build:** 4.7.1-HOTFIX_11638371

Release de compatibilidad con el nuevo hotfix 4.7.1-HOTFIX_11638371. CIG ha publicado un hotfix puramente técnico (servidor, netcode, motor): no ha tocado ningún texto en los archivos de localización del juego ni los datos de gameplay.

El `global.ini` distribuido en este release es **byte-idéntico** al de v1.9.6, pero se publica con el build nuevo en el ZIP para que no haya dudas sobre compatibilidad. Si ya tenías v1.9.6 instalado, sigue siendo válido sobre 11638371 y no hace falta actualizar.

**Estadísticas:**
- Líneas en global.ini: 87 626 (igual que v1.9.6)

## v1.9.6 — 2026-04-14

**Build:** 4.7.1-HOTFIX_11617053

Extensión del refactor v1.9.5 a mochilas, subtrajes y trajes de exploración, más un fix importante de un bug que había dejado ~24 cascos con el nombre roto en la versión anterior.

**Fix cascos rotos v1.9.5:**
- En v1.9.5, el refactor de nombres dejó ~24 cascos con el prefijo truncado cuando el nombre original contenía una preposición (ej. `Casco de Exploración Zeus` quedó como `de Exploración Zeus (Casco)`). Todos corregidos: `Zeus (Casco exploración)`, `Stirling Sediment Edition (Casco exploración)`, `Advocacy Interceptor (Casco)`, etc.

**Trajes de exploración — pieza única (~85 claves):**
Los trajes Novikov, Pembroke, Zeus y Stirling son una pieza única integrada in-game (brazos+piernas+pecho+subtraje) y ahora llevan marcador propio para diferenciarlos del resto de armadura:
- Traje completo → `Novikov (Traje exploración)`, `Stirling Sediment Edition (Traje exploración)`
- Casco (item separado) → `Zeus Starscape (Casco exploración)`
- Mochila (item separada) → `Pembroke RSI Sunburst Edition (Mochila exploración)`

**Cascos de carreras (6 claves):**
Los cascos de piloto temáticos de naves/ligas de carreras usan `(Casco carreras)`:
- `Mirai (Casco carreras)` · `Origin (Casco carreras)` · `Murray Cup (Casco carreras)` · `Star Kitten (Casco carreras)` · `Fortuna (Casco carreras)` · `Origin 350r (Casco carreras)`

**Mochilas — ~130 claves al formato unificado:**
Todas las mochilas pasan del prefijo heredado `Mochila X` al formato `<Set> <Variante> (Mochila)`, coherente con el refactor de armaduras de v1.9.5.
```
CSP-68L Forest Camo (Mochila)
Aril Black Cherry (Mochila)
Geist Whiteout (Mochila)
```

**Subtrajes — ~198 claves al formato unificado:**
Palabra nueva **Subtraje** como calco español de "undersuit" (sub+traje). Más específica que "traje" genérico, transparente para quien consulta guías en inglés, y evita colisión con "traje" en otros contextos del juego.
```
TCS-4 Woodland (Subtraje)
Guardian (Subtraje)
Advocacy Interceptor (Subtraje)
```

**Cambios menores:**
- Variantes "Modificado/a/s" con concordancia de género: `(Mochila Modificada)`, `(Subtraje Modificado)`, `(Traje exploración Modificado)`.
- ~5 correcciones puntuales de cascos/subtrajes con nombres preposicionales (Field Recon, Microid Battle, etc.).

**Estadísticas:**
- ~430 entradas tocadas en total
- Líneas en global.ini: 87626 (sin cambio)

## v1.9.5 — 2026-04-13

**Build:** 4.7.1-HOTFIX_11617053

Refactor completo de nombres de piezas de armadura. Unifica el estilo de todas las piezas al formato `<Set> <Variante> (Parte)`, mirror del inglés oficial del juego. Antes convivían tres formatos distintos heredados del histórico de traducción; a partir de ahora los nombres son consistentes entre sí, más cortos y alineados con cómo CIG los nombra internamente.

**Cambios:**
- Piezas de armadura renombradas al formato unificado: ej. `Citadel Dark Red (Pecho)`, `Aves Starchaser (Piernas)`, `ADP-mk4 Big Boss (Casco)`, `DCP Camuflaje Cazador (Brazos)`. Las 4 partes (pecho/brazos/piernas/casco) usan el mismo esquema.
- Variantes modificadas con concordancia de género: `(Pecho Modificado)`, `(Brazos Modificados)`, `(Piernas Modificadas)`, `(Casco Modificado)`.
- Trajes tipo pantalón (Antium, Palatino) usan `(Pantalones)` como marcador para reflejar que son prendas de tela, no armadura rígida. Ej: `Antium Storm (Pantalones)`, `Palatino Shadow Gild (Pantalones)`.
- Cascos antes sin traducir ahora con marcador unificado: `Argus (Casco)`, `Cyclops (Casco)`, `G-6 (Casco)`, `G-8 (Casco)`, `The Hill Horror (Casco)`, `Snarling Vanduul (Casco)`, `Parasite Replica (Casco)`, `TrueDef-Pro (Pecho)`, `ORC-mkV Crusader Edition (Pecho)`.
- Corregido typo histórico en Defiance Desert (palabras pegadas sin espacio) → ahora `Defiance Desert (Brazos)` y `Defiance Desert (Casco)`.
- La tabla de pesos compartida en descripciones de armadura también usa "Pecho" en vez de "Pechera" para coherencia con los nombres.
- ~1200 entradas tocadas en total.

**Estadísticas:**
- Líneas en global.ini: 87626 (sin cambio)

## v1.9.4 — 2026-04-13

**Build:** 4.7.1-HOTFIX_11617053

Bump de compatibilidad. El nuevo HOTFIX 11617053 publicado por Star Citizen no toca ninguna cadena de texto del juego, asi que el archivo `global.ini` distribuido es exactamente el mismo que el de v1.9.3. Esta version existe unicamente para que sepas que el parche sigue siendo valido sobre la build vigente y no tengas que adivinarlo.

**Cambios:**
- Sin cambios en `global.ini` respecto a v1.9.3.
- ZIP renombrado a v1.9.4 con estructura LIVE + HOTFIX (mismo `global.ini` en ambas carpetas), para que la instalacion sea trivial sobre cualquiera de los dos canales.

**Estadisticas:**
- Lineas en global.ini: 87626 (sin cambios)

## v1.9.3 — 2026-04-13

**Build:** 4.7.1-LIVE_11592622 (sin cambio de version del juego)

Limpieza interna del archivo de traduccion: eliminadas 92 entradas heredadas de versiones antiguas que el juego ya no usa (codigo muerto). El parche queda mas pequeño y alineado al 100% con las claves activas del juego.

**Cambios:**
- Eliminadas 92 entradas obsoletas que correspondian a renombres antiguos del juego: dialogos de comentarista de carreras, descripciones de misiones de mineria de Shubin, mision Hockrow Facility Delve, mision blackbox recovery, opciones del head-tracking Tobii, tutoriales retirados, y variantes antiguas de items y torretas.
- Las traducciones de esas entradas se conservan automaticamente bajo los nombres nuevos que usa el juego, asi que no se pierde ninguna traduccion visible — solo se elimina el duplicado interno.

**Estadisticas:**
- Lineas en global.ini: 87626 (antes 87718, -92)

## v1.9.2 — 2026-04-12

**Build:** 4.7.1-LIVE_11592622 (sin cambio de version del juego)

Correccion de tres traducciones que sonaban forzadas por seguir demasiado al pie de la letra el orden de las palabras del ingles original.

**Cambios:**
- Aviso de sensor: `Radar contacto` -> `Contacto de radar` (mas natural en español).
- HUD de combate: `Ciclismo objetivo` -> `Cambiar objetivo`. *"Ciclismo"* sonaba al deporte de la bici en lugar de a la accion de pasar de un objetivo a otro.

**Estadisticas:**
- Lineas en global.ini: 87718 (sin cambio)

## v1.9.1 — 2026-04-12

**Build:** 4.7.1-LIVE_11592622 (sin cambio de version del juego)

Recuperacion de traducciones que se perdian entre versiones y traduccion de varios titulos y mensajes que seguian en ingles.

**Traducciones recuperadas (47):**
- Lineas del comentarista de carreras (`Lose Position` y `Moving Up Position`) que volvian a aparecer en ingles tras cada actualizacion del juego.
- Avisos de sensores en HUD: `Bogey` -> `Espectro`, `Contact` -> `Contacto`, `Radar contact` -> `Radar contacto` (variantes ANVL, ORIG, RSI).
- `Cambiar Posicion de la torreta` (UI de tripulacion).
- Resumen rapido de la mision Siege of Orison y aviso de cierre del evento del LPA.
- Frases cortas de NPC en combate y sociales.
- Tutorial de combate (consejo profesional sobre contramedidas).
- Briefing del contrato `hurston_UGF_defend` (Hurston Dynamics Outsourcing).

**Nuevas traducciones de textos heredados (10):**
- Mensaje de objetivo de reabastecimiento: *"Reabastecimiento al X% completado. Por favor, manten la posicion actual."*
- Titulo de mision: *"Lucha por un Pyro Libre"*
- Sobres del Año Lunar (Caballo, Mono, Carnero, Gallo).
- 4 titulos de mision de HeadHunters - Recuperar Carga: *"Recuperando lo nuestro"*, *"Terminar el trabajo"*, *"Vale la pena"*, *"Obteniendo lo que merecemos"*.

**Estadisticas:**
- Lineas en global.ini: 87718

## v1.9.0 — 2026-04-12

**Build:** 4.7.1-LIVE_11592622 (sin cambio de version del juego)

Mejora del estilo de misiles, torpedos y bombas para que todos sigan el mismo formato visible en pantalla, mas correcciones puntuales de traducciones y nombres.

**Misiles, torpedos y bombas con estilo uniforme:**
- Todos los misiles y torpedos ahora muestran el tracking type (`IR`/`EM`/`CS`) como prefijo al inicio del nombre, eliminando duplicaciones donde el sufijo del modelo (`-CS`/`-EM`/`-IR`) ya lo indicaba.
- Ground missiles y torpedos grandes (Spearhead, Agitator, Argos, Vanquisher, Calamity, Apex, Executor, Torpedo Short) que antes salian sin tracking visible, ahora lo llevan al inicio.
- Las bombas conservan el formato `B#` (B3, B5, B10) segun su tamaño.
- Pequeño bug fix: el Thunderbolt S03 marcado erroneamente como `CS` ahora muestra el `EM` correcto.

**Correcciones puntuales de nombres y traducciones:**
- Componentes MISC con palabras comunes traducidas correctamente: Reliant Mako Wing Mount, Reliant/Prospector CML Flare, FuelPod, Starfarer Captain's Seat, SelfDestruct, FuelRefinery.
- 6 titulos de misiones que tenian texto español+ingles concatenado sin separador (cfp_defendship, cfp_eliminateall_fromCFP_XT, RAIN_collectresources, vaughn_assassination) ahora muestran solo la version en español.
- 14 nombres de pinturas y vehiculos con texto literalmente duplicado (`Greycat UTVGreycat UTV`, `Pintura Hull B KeystonePintura Hull B Keystone`, etc.) limpiados.
- `PIT_Inventory_Helmet`: la opcion del menu inventario para intercambiar casco mostraba "Casco de palanca" (mala traduccion del verbo "swap"). Corregido a "Intercambiar Casco".
- `F8C Stealth`: revertido el nombre traducido "Apuñalador Sigiloso" al nombre propio original "Sneaky Stabber".

**Componentes con grado preservado:**
- Algunos componentes de naves industriales (AEGS Reclaimer cooler/shield, ORIG 890J shield) recuperan su clase y grado correctos que habian perdido en versiones intermedias.
- 5 manufacturers de componentes de nave que estaban sin clasificar ahora reciben su prefijo (54 radares afectados).

**Componentes que el motor del juego no encontraba:**
- 4 mensajes de error de eventos antiguos (DynamicEvent_FleetWeek2022_FailReason_*) que tenian un espacio de mas en su clave y el juego no los matcheaba ahora se cargan correctamente.

**45 descripciones de mision con "Posibles Planos" propagadas:**
- Misiones con multiples variantes de descripcion (boss, side, intro, etc.) ahora todas muestran la lista de blueprints, no solo la principal.

**Estadisticas:**
- Lineas en global.ini: 87.718 (sin cambio en cardinalidad vs v1.8.3)
- Misiles con tracking type visible: 108 → 136 (+28 ground missiles y torpedos grandes)
- Componentes con clase y grado completos: 379 → 382

## v1.8.3 — 2026-04-12

**Build:** 4.7.1-LIVE_11592622 (sin cambio de version del juego)

Fix de un nombre roto en la armadura ORC-mkV y restauracion de listas de "Posibles Planos" perdidas en muchas variantes de descripcion de mision.

**Fix nombre roto en armadura ORC-mkV:**
- Las piernas modificadas de la ORC-mkV mostraban una cadena de basura pegada al nombre (`ORC-mkVbbbbbbbbbbbbbbbbbbbbbbbb (Piernas Modificadas)`). Corregido a `ORC-mkV (Piernas Modificadas)`.

**Restauradas 45 listas de "Posibles Planos" en descripciones de mision:**
- Muchas misiones con el marcador `[BP]` en el titulo mostraban la descripcion **sin la lista de planos** en el panel de oferta.
- Causa: el juego puede mostrar varias variantes de descripcion para la misma mision (segun fase, contexto o submision), y la lista de planos solo estaba en una de ellas. Las demas variantes quedaban "huerfanas".
- Ahora la lista de planos se propaga automaticamente a todas las variantes hermanas de cada mision, asi siempre se ve sin importar la version del texto que muestre el juego.
- Misiones afectadas: variantes de asesinatos selectivos en UGFs, defensas de naves CFP en Nyx, caza de fauna en Highpoint, ataques de Headhunters, defensas Foxwell, sondas legales y mas.

**Estadisticas:**
- Lineas en global.ini: 87 718
- Descripciones con "Posibles Planos": 249 → 294 (+45)

## v1.8.1 — 2026-04-10

**Build:** 4.7.1-LIVE_11592622 (sin cambio de version del juego)

Pesos correctos en consumibles del SRT, fix del boton de encendido en cabinas tipo Apolo Medivac, y recuperacion de 34 misiones que perdian el marcador `[BP]` en el titulo + 25 listas de "Posibles Planos" perdidas desde versiones antiguas.

**Pesos correctos en contenedores RMC del Cambio SRT:**
- `Contenedor SRT Cambio` (grande): añadido `1.3 kg` (antes no aparecia)
- `Contenedor SRT Cambio-Lite` (multi-herramienta): corregido `0.1 kg` → `0.82 kg`

**Boton de encendido en cabinas tipo Apolo Medivac:**
- El label del boton de encendido (cuando esta apagada) decia "Listo para despegue", pero su par opuesto (cuando esta encendida) dice "Desactivar energia". El nuevo label unifica ambos estados como "Activar energia" / "Desactivar energia"

**Recuperadas 34 misiones con marcador `[BP]`:**
- Mejorada la deteccion de misiones que recompensan blueprints. Antes el sistema fallaba cuando una capa intermedia no marcaba la mision aunque el juego siguiera dandole blueprints. Ahora se detectan directamente desde los datos del juego
- Total de titulos con `[BP]`: 200 → 234 (+34 misiones recuperadas, principalmente variantes de sabotaje, defensa de bases, headhunters y bounties FPS)

**Restauradas 25 listas de "Posibles Planos" perdidas:**
- Auditoria detecto que 25 misiones aparecian con el marcador `[BP]` en el HUD pero su descripcion no listaba los planos posibles. La regresion se arrastraba desde una version antigua donde el archivo de blueprints se regenero perdiendo entradas
- Despues del fix: 229 misiones con `[BP]` muestran ademas la lista de posibles planos en su descripcion (antes 200)

**Estadisticas:**
- Lineas en global.ini: 87.718 (sin cambio)
- Blueprints traducidos: 502 (antes 477)
- Misiones con `[BP]`: 234 (antes 200)

## v1.8.0 — 2026-04-09

**Build:** 4.7.1-LIVE_11592622 (sin cambio de version del juego)

Reestructura del compendio de mineria del diario, unificacion del formato de minerales en el HUD y limpieza de un placeholder con un marcador fantasma.

**Compendio de mineria reorganizado por rareza:**
- El "Compendio general de mineria" del diario del juego ahora esta organizado en 6 secciones por rareza (Legendario, Epico, Raro, Poco comun, Comun, Minables a mano), con los minerales en orden alfabetico dentro de cada seccion.
- Antes era un listado plano alfabetico; ahora es mucho mas facil localizar los minerales raros y saber a primera vista en que categoria estan.
- Encabezados en español y marcador "(Raro)" redundante eliminado de Quantainium (ya esta bajo "Legendario").

**Minerales en el HUD de nave:**
- Los 4 minerales que antes aparecian con formatos inconsistentes o en ingles ahora siguen la convencion `(Bto)` raw / `(Mnl)` mena:
  - `Raw Ice` (en ingles) → `Hielo (Bto)`
  - `Quantainium C.` → `Quant (Bto)` (formato `C.` eliminado)
  - `Hephaestanite` (sin marca) → `Heph (Bto)`
  - `Feynmalin (Bto)` (nombre truncado) → `Feynma (Bto)`
- 3 nombres de mena que se salian del ancho del HUD acortados de forma natural:
  - `Savrilium (Mnl)` → `Savril (Mnl)`
  - `Saldynium (Mnl)` → `Saldyn (Mnl)`
  - `Lindinium (Mnl)` → `Lindin (Mnl)`
- Añadido acortamiento `Glacosite (Bto)` → `Glacos (Bto)`
- El commodity refinado de Hephaestanite revertido al nombre completo (ya no hace falta abreviar porque el raw es el que lleva la marca).

**Fix en el placeholder de localizacion:**
- La clave de error de localizacion `LOC_UNINITIALIZED` arrastraba un marcador `<EM4>[BP]</EM4>` fantasma. Este placeholder se muestra cuando el motor del juego no puede resolver un texto y no tiene nada que ver con misiones de blueprints, asi que el marcador estaba fuera de lugar. Ahora se muestra limpio.

**Estadisticas:**
- Lineas en global.ini: 87,718 (sin cambio respecto a v1.7.1)
- Correcciones manuales totales: 100

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
