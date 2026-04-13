# Contexto del proyecto

## Stack tecnológico

| Capa | Tecnología |
|---|---|
| Frontend / App | Streamlit ≥ 1.28 |
| Lenguaje | Python 3.14 |
| Base de datos | Supabase (PostgreSQL 17) |
| Autenticación | Supabase Auth (GoTrue) |
| Persistencia de sesión | Cookies via `extra-streamlit-components` |
| Excel / datos | pandas ≥ 2.0, openpyxl ≥ 3.1 |
| SharePoint | Office365-REST-Python-Client ≥ 2.5 |
| Email | smtplib (MIME) |

---

## Estructura de directorios

```
total_capital_intra/
├── app.py                        # Punto de entrada principal
├── requirements.txt
├── assets/
│   └── logo.png
├── config/
│   ├── theme.py                  # CSS global y de login, colores de marca
│   ├── supabase_auth.py          # Wrappers HTTP para Supabase Auth + PostgREST
│   ├── auth_cookie.py            # Persistencia de sesión en cookies (30 días)
│   ├── email_sender.py           # Envío de correo SMTP con adjuntos
│   └── auth.py                   # Sistema legacy YAML (NO usar en código nuevo)
├── modules/
│   ├── admin/
│   │   ├── admin_ui.py           # UI procesador de estados de cuenta CSV → Excel
│   │   ├── admin_logic.py        # Lógica de parseo de CSV bancarios
│   │   └── users_ui.py           # Gestión de usuarios (solo admin)
│   └── shared/
│       └── sharepoint.py         # Cliente SharePoint
├── scripts/
│   └── generate_password_hash.py
├── supabase/
│   └── config.toml
└── .streamlit/
    ├── secrets.toml              # Gitignoreado
    └── secrets.toml.example
```

---

## Arquitectura

`app.py` es una **single-page app** con enrutamiento manual por `st.session_state`. No usar `pages/` de Streamlit.

Claves de navegación:
- `st.session_state["nav_main"]` → `"profile"` | `"module"` | `"users"`
- `st.session_state["nav_department"]` → `"Administración"` | `"RRHH"` | `"Ventas"` | `"Legal"`

Flujo de inicio:
1. Restaurar sesión desde cookie → si falla → mostrar login
2. Login exitoso → cargar usuario (rol, departamentos) desde Supabase
3. Renderizar sidebar dinámico según rol y departamentos asignados
4. Renderizar contenido según navegación activa

---

## Autenticación y sesión

### Supabase Auth (activo)
- Login: email (local + dominio por selectbox) + contraseña
- Endpoint: `POST /auth/v1/token?grant_type=password`
- Tokens en `st.session_state`: `supabase_access_token`, `supabase_user_id`, `supabase_email`
- Cookie `tc_intra_sb_rt_v1`: refresh token, 30 días
- Al F5: `restore_supabase_session_from_cookie()` canjea el refresh token por nuevo access token

### Dominios soportados
```
banverde.com | fidalia.mx | totalcapital.mx | totaltax.mx | totalbridge.com.mx | dynovaet.com
```

### Sistema legacy (NO usar)
`config/auth.py` + `config/credentials.yaml` — YAML + bcrypt. No usar en código nuevo.

---

## Base de datos Supabase

### Tablas principales

| Tabla | Columnas clave |
|---|---|
| `public.users` | `id` (UUID), `full_name`, `email`, `role_id`, `active` |
| `public.roles` | `id`, `name` (`"admin"` \| `"user"`) |
| `public.departments` | `id`, `name` |
| `public.user_departments` | `user_id`, `department_id` (M:N) |

### RLS (Row Level Security)
- Usuarios normales: consultas con `access_token` como Bearer
- Operaciones admin: usar `service_role_key` (NUNCA `anon_key` para CRUD de usuarios)

### Patrón de consulta — tupla `(ok, data_or_error)`
```python
ok, result = supabase_rest_select("users", params, access_token)
if not ok:
    st.error(result)
```

---

## Módulos de departamentos

### Administración (`modules/admin/`) — Implementado
- Procesador CSV bancarios → Excel multi-hoja (banco: "Banco VE POR MAS")
- Tags: IDs de cuenta → códigos de departamento (DGE USD, BSI MXN, DGP, SVC…)
- Gestión de usuarios (CRUD completo, solo admin): `users_ui.py`

### RRHH | Ventas | Legal — Placeholders

### Para agregar un módulo nuevo
1. Crear `modules/<dept>/__init__.py` y `modules/<dept>/<dept>_ui.py` con función `render()`
2. Registrar en `app.py` bajo el bloque `elif dept_name == "..."`
3. Insertar departamento en `public.departments` y asignar a usuarios en `public.user_departments`

---

## Configuración

### `.streamlit/secrets.toml`
```toml
[supabase]
url = "https://<project-id>.supabase.co"
anon_key = "eyJ..."
service_role_key = "eyJ..."

[sharepoint]
site_url = "https://..."
username = "user@dominio.com"
password = "..."
```

### Variables de entorno
```
SMTP_HOST= | SMTP_PORT=587 | SMTP_USER= | SMTP_PASSWORD= | EMAIL_FROM= | SMTP_USE_TLS=true
SHAREPOINT_SITE_URL= | SHAREPOINT_USERNAME= | SHAREPOINT_PASSWORD=
```

---

## Estilo y tema

- **Fuentes**: Montserrat (títulos), Poppins (cuerpo) — Google Fonts
- **Colores**: Primario `#003a40` · Secundario `#7ed957` · Terciario `#4e5d77`
- CSS centralizado en `config/theme.py` (`CUSTOM_CSS` y `LOGIN_PAGE_CSS`)
- Iconos SVG embebidos como base64 en Markdown del sidebar
- No usar estilos inline en componentes — todo va en `theme.py`

---

## Correr la aplicación

```bash
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Completar secrets.toml con credenciales reales
streamlit run app.py
```
