# Reglas de desarrollo

## Principios SOLID

### S — Single Responsibility
Cada módulo, clase o función tiene una sola razón para cambiar.
- `admin_ui.py` solo maneja presentación; `admin_logic.py` solo maneja lógica de negocio
- Las funciones de `supabase_auth.py` solo hacen una operación de BD cada una
- No mezclar lógica de negocio con llamadas a `st.*` en el mismo lugar

### O — Open/Closed
El código está abierto para extensión, cerrado para modificación.
- Los módulos de departamento se agregan sin tocar los existentes
- El enrutamiento en `app.py` usa `elif dept_name` extensible, no condiciones hardcoded en lógica interna
- Los parsers de bancos en `admin_logic.py` deben poder agregarse sin reescribir los existentes

### L — Liskov Substitution
Las implementaciones de una interfaz deben ser intercambiables.
- Cualquier módulo de departamento con función `render()` es intercambiable en el router
- Los clientes de BD (supabase_auth) deben poder sustituirse sin cambiar los módulos que los usan

### I — Interface Segregation
No forzar dependencias en funcionalidad que no se usa.
- Los módulos solo importan lo que necesitan de `config/`
- No importar `users_ui` en módulos de usuario regular
- Cada módulo de departamento es autónomo en sus imports

### D — Dependency Inversion
Depender de abstracciones, no de implementaciones concretas.
- Los módulos de departamento reciben el `access_token` como parámetro o lo leen de `session_state`, no dependen de detalles de autenticación
- La lógica de negocio no importa directamente `st.secrets` — eso lo hace la capa `config/`

---

## Reglas generales de código

### Funciones y módulos
- **Una función = una tarea**. Si una función hace más de una cosa, dividirla.
- Máximo ~50 líneas por función. Si se excede, extraer subfunciones con nombre descriptivo.
- Nombrar funciones con verbos: `parse_csv_row()`, `render_user_card()`, `fetch_user_departments()`
- Nombrar variables con sustantivos descriptivos. Sin abreviaciones ambiguas (`usr`, `tmp`, `d`).

### Separación de capas
```
UI (st.*)  ←→  Lógica de negocio  ←→  Acceso a datos (supabase_auth)
```
- Las funciones `render_*` y `_ui.py` solo llaman a lógica, no procesan datos crudos
- Las funciones `_logic.py` no tocan `st.*` — retornan datos, no los muestran
- `config/supabase_auth.py` no sabe nada de la UI ni de la lógica de negocio

### Manejo de errores
- Usar siempre el patrón de tupla: `(ok: bool, data | error_msg: str)`
- Nunca silenciar errores con `except: pass`
- Mostrar errores con `st.error()` solo en la capa UI, no en lógica ni en acceso a datos
- Los errores deben ser legibles para el usuario en español

```python
# Correcto
ok, result = supabase_rest_select("users", params, token)
if not ok:
    st.error(f"No se pudo cargar usuarios: {result}")
    return

# Incorrecto
try:
    data = supabase_rest_select(...)
except:
    pass
```

### Estado de la sesión (`st.session_state`)
- Todas las claves prefijadas con `tc_`: `tc_nav_main`, `tc_cookie_manager`, etc.
- Inicializar claves con `.get()` o `setdefault()`, nunca asumir que existen
- No guardar en session_state datos que pueden recalcularse fácilmente

### Seguridad
- **Nunca** usar `service_role_key` en operaciones que pueden hacer usuarios normales
- **Nunca** exponer `service_role_key` en logs, mensajes de error o en el frontend
- Validar que el usuario esté autenticado antes de cualquier operación de BD
- Las operaciones de admin deben verificar `role_name == "admin"` antes de ejecutarse
- No construir queries con f-strings con input del usuario — usar parámetros de PostgREST

### CSS y estilo
- Todo el CSS va en `config/theme.py`. No usar `st.markdown("<style>...</style>")` fuera de ahí.
- No usar `st.write()` para HTML — usar `st.markdown(..., unsafe_allow_html=True)` solo cuando es necesario
- Respetar la paleta de colores: primario `#003a40`, secundario `#7ed957`, terciario `#4e5d77`

---

## Convenciones de este proyecto

| Elemento | Convención |
|---|---|
| Idioma de UI | Español (México) |
| Idioma de código | Inglés (nombres de variables, funciones) |
| Idioma de comentarios | Español |
| Archivos de módulo UI | `<dept>_ui.py` con función `render()` |
| Archivos de lógica | `<dept>_logic.py` |
| Session state keys | Prefijo `tc_` |
| Modales/dialogs | Decorador `@st.dialog()` |
| Formato de retorno BD | Tupla `(ok: bool, data_or_error)` |

---

## Lo que NO hacer

- No usar el sistema legacy (`config/auth.py`, `credentials.yaml`) en código nuevo
- No usar `pages/` de Streamlit — la app es single-page con routing manual
- No poner lógica de negocio en `app.py` — solo routing y composición
- No hacer imports circulares entre módulos
- No commitear `secrets.toml` ni `.env` con credenciales reales
- No usar `st.experimental_*` — usar las APIs estables equivalentes
- No crear abstracciones para un solo caso de uso — YAGNI (You Aren't Gonna Need It)
- No agregar manejo de errores para escenarios imposibles en el flujo actual

---

## Checklist antes de cada cambio

- [ ] La función tiene una sola responsabilidad
- [ ] La lógica de negocio está separada de la UI
- [ ] Los errores se manejan con la tupla `(ok, data_or_error)` y se muestran en la capa UI
- [ ] No se exponen secrets ni tokens en logs o mensajes
- [ ] El código nuevo está en español (comentarios) e inglés (variables/funciones)
- [ ] Se respetan los prefijos de session state (`tc_`)
- [ ] No se rompe el enrutamiento de `app.py`
