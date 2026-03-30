# Star Citizen - Traduccion ES + BluePrints

Traduccion al español de Star Citizen que combina multiples fuentes para ofrecer la experiencia mas completa posible en español.

## Que hace este proyecto

Star Citizen no tiene traduccion oficial completa al español. Existen proyectos comunitarios que traducen los textos del juego, pero ninguno incluye toda la informacion disponible. Este proyecto:

1. **Parte de la traduccion de Thord82**, la traduccion comunitaria al español mas completa
2. **Añade datos de blueprints** de las misiones que dan planos, con la lista de posibles recompensas traducida al español
3. **Añade clase/grado a los componentes** de naves (coolers, power plants, quantum drives, shields, radars) con prefijo compacto (ej: `Mil2A Bracer` = Militar, Tamaño 2, Grado A)
4. **Marca misiones con blueprints** con `[BP]` en el titulo para identificarlas rapidamente
5. **Marca sustancias ilegales** con `[!]` para avisar antes de transportarlas
6. **Mejora titulos de hauling** añadiendo la ruta (origen>destino) al titulo del contrato
7. **Acorta nombres largos** en el HUD de mineria para evitar solapamiento (Hephaestanite → Heph, Inestabilidad → Inest:)
8. **Completa claves que faltan** extrayendo los textos oficiales directamente del Data.p4k del juego
9. **Corrige errores** de las fuentes originales (GUIDs nulos, pools faltantes, duplicados)

## Fuentes

| Fuente | Descripcion | Enlace |
|---|---|---|
| **Thord82** | Traduccion comunitaria al español. Base principal del proyecto | [github.com/Thord82/Star_citizen_ES](https://github.com/Thord82/Star_citizen_ES/) |
| **MrKraken / StarStrings** | Blueprints de misiones, clase/grado de componentes, mejoras de hauling y QoL | [github.com/MrKraken/StarStrings](https://github.com/MrKraken/StarStrings) |
| **ExoAE / ScCompLangPack** | Clase/grado de componentes, blueprints, avisos de sustancias ilegales | [github.com/ExoAE/ScCompLangPack](https://github.com/ExoAE/ScCompLangPack/) |
| **BeltaKoda / ScCompLangPackRemix** | Prefijos compactos de componentes (referencia) | [github.com/BeltaKoda/ScCompLangPackRemix](https://github.com/BeltaKoda/ScCompLangPackRemix) |
| **Data.p4k** | Textos oficiales EN/ES extraidos del propio juego con `extract_p4k.py` | Instalacion local de Star Citizen |

## Que incluye el global.ini final

| Capa | Descripcion | Claves |
|---|---|---|
| Thord82 | Traduccion base al español | ~87.585 |
| Blueprints | Planos posibles en misiones (traducidos al ES) + correcciones | ~232 |
| Componentes | Prefijo clase/grado en 368 componentes de naves | 368 |
| [BP] titulos | Marca `[BP]` en misiones que dan blueprints | 216 |
| Sustancias ilegales | Marca `[!]` en 8 drogas/sustancias | 8 |
| HUD mining | Abreviaturas para evitar solapamiento | 2 |
| Heph + minerales | Hephaestanite acortado + unificacion a (Bruto) | 20 |
| Hauling titles | Rutas en titulos de transporte de carga | 5 |
| P4K traducciones | Claves que faltan en Thord82, traducidas | ~874 |

## Instalacion

1. Descarga el ZIP de la ultima release
2. Extrae el contenido en la carpeta de Star Citizen (ej: `C:\Program Files\Roberts Space Industries\StarCitizen\`)
3. La estructura queda asi:
```
StarCitizen/
└── LIVE/
    ├── data/Localization/english/global.ini
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

Ejemplo: `Mil2A Bracer` = Bracer, clase Militar, tamaño 2, grado A.

## Herramienta incluida: extract_p4k.py

Script Python que extrae el `global.ini` de cualquier idioma directamente del `Data.p4k` de tu instalacion de Star Citizen.

```bash
pip install zstandard
python extract_p4k.py --list                        # Ver idiomas disponibles
python extract_p4k.py                               # Extraer ingles
python extract_p4k.py --lang spanish_(spain)         # Extraer español oficial de CIG
```

## Version actual

- **Star Citizen Alpha 4.7.0-hotfix** (build 11545720)
- Ver [CHANGELOG.md](CHANGELOG.md) para el historial completo
