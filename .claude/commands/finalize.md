# Skill: Finalize

Flujo completo de cierre de build: changelog, documentación, optimización de agentes, ZIP de distribución, commit y push. Ejecutar cada fase en orden — no empezar la siguiente hasta terminar la anterior.

## Fase 1: Changelog

1. Identificar última versión:

```bash
head -20 CHANGELOG.md
```

Si no existe, crear con versión `v1.0.0`.

2. Revisar commits desde esa versión:

```bash
git log --oneline -30
```

3. Redactar entrada con esta estructura:

```markdown
## vX.Y.Z — YYYY-MM-DD

**Fuentes utilizadas:**
- Thord82: [versión/fecha del .ini usado]
- MrKraken/StarStrings: [versión/fecha del .ini usado]

**Cambios:**
- [descripción funcional orientada al usuario]

**Estadísticas:**
- Líneas en global.ini: X
- Blueprints traducidos: X
- Claves nuevas añadidas: X
```

Versionado: Minor (1.X.0) = nueva versión de fuentes procesada, Patch (1.0.X) = correcciones de traducción. Proponer al usuario para validación antes de escribir.

## Fase 2: Actualizar guía de estilo

Revisar si el estilo de Thord82 cambió en esta versión:

1. Buscar nuevos sets de armadura, armas o patrones de traducción en `global_thord82_.ini`
2. Comparar contra `.claude/guides/thord82-style.md`
3. Si hay cambios (nuevos items, nuevos patrones), actualizar la guía
4. Si no cambió nada, no tocar

## Fase 3: Optimización de agentes

Para cada agente en `.claude/agents/`:

### 3a. Higiene de contenido
- **PROHIBIDO** en agentes: listados de archivos, explicaciones de código, snippets
- Si un agente tiene documentación técnica → moverla a la guía correspondiente
- Los agentes solo contienen: rol, referencias a guías, reglas operativas, protocolo

### 3b. Boilerplate compacto
Todos los agentes (excepto tech-lead.md) deben terminar con este bloque exacto:

```markdown
## Protocolo estándar

- **Permisos**: si falta acceso, reportar al Tech Lead: "Necesito [herramienta] para [tarea]"
- **Solo directrices aquí**: documentación técnica va en guías, no en este archivo
- **Autoactualización**: al terminar, si cambió el dominio actualizar este archivo; si cambió un sistema actualizar guías
```

### 3c. Verificar tamaños

| Archivo | Objetivo |
|---|---|
| CLAUDE.md | < 160 líneas |
| tech-lead.md | < 60 líneas |
| Agentes especialistas | < 80 líneas |

Reportar si alguno excede el límite.

## Fase 4: Generar ZIP de distribución

```bash
# Limpiar temporal
rm -rf /tmp/blueprints_zip

# Crear estructura LIVE
mkdir -p /tmp/blueprints_zip/LIVE/data/Localization/spanish_\(spain\)
cp global.ini /tmp/blueprints_zip/LIVE/data/Localization/spanish_\(spain\)/global.ini
```

Extraer `user.cfg` del ZIP de Thord82 si existe:

```bash
unzip -o "Star_citizen_ES _Thord82.zip" "LIVE/user.cfg" -d /tmp/thord82_extract 2>/dev/null
cp /tmp/thord82_extract/LIVE/user.cfg /tmp/blueprints_zip/LIVE/user.cfg 2>/dev/null
```

Si no hay ZIP de Thord82, crear user.cfg con contenido estándar:

```
g_language = spanish_(spain)
g_languageAudio=english
```

Generar ZIP:

```bash
powershell.exe -Command "Compress-Archive -Path '/tmp/blueprints_zip/LIVE' -DestinationPath 'Star_citizen_ES_BluePrints.zip' -Force"
```

Verificar contenido del ZIP generado.

## Fase 5: Commit y Push

```bash
git add CHANGELOG.md CLAUDE.md .claude/ global.ini global_diff.ini global_diff_es.ini global_thord82_.ini global_blueprints.ini .gitignore
git commit -m "vX.Y.Z: descripción breve

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
git push
```

**No incluir en el commit**: archivos .zip (están en .gitignore).

## Notas

- Ejecutar fases en orden estricto — no saltar ninguna
- El usuario valida el changelog antes de continuar
- Si alguna fase falla, reportar y esperar instrucciones — no continuar automáticamente
- Los .zip no se suben a git — son solo para distribución local
