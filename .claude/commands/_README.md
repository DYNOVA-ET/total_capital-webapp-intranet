# Skills / Slash Commands

Los archivos `.md` en esta carpeta se convierten automáticamente en slash commands disponibles en Claude Code.

## Cómo crear un skill

Crea un archivo `nombre-del-skill.md` en esta carpeta con el prompt que Claude debe ejecutar.

```
.claude/commands/
├── nuevo-modulo.md      → /nuevo-modulo
├── revisar-codigo.md    → /revisar-codigo
└── deploy-check.md      → /deploy-check
```

## Uso de argumentos

Usa `$ARGUMENTS` en el contenido del archivo para recibir lo que el usuario escriba tras el comando.

Ejemplo en `nuevo-modulo.md`:
```
Crea un nuevo módulo de departamento llamado "$ARGUMENTS" siguiendo la estructura
definida en .claude/project.md y las reglas de .claude/rules.md
```

Uso: `/nuevo-modulo RRHH`

## Skills disponibles en este proyecto

| Comando | Archivo | Descripción |
|---|---|---|
| `/ui-streamlit` | `ui-streamlit.md` | UI designer con animaciones GSAP-style, hover, cards, métricas animadas — respeta el sistema de diseño Total Capital |
