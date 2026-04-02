"""Punto de entrada principal - Intranet Total Capital."""

import base64
from pathlib import Path

import streamlit as st

from config.theme import CUSTOM_CSS, LOGIN_PAGE_CSS
from config.supabase_auth import supabase_rest_select, supabase_sign_in, supabase_sign_up
from modules.admin import admin_ui
from modules.admin.users_ui import render as render_users_ui

# Iconos SVG (línea fina) para la barra lateral
_ICO = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" '
    'viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">{inner}</svg>'
)
ICO_USER = _ICO.format(
    inner='<path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z"/>'
)
ICO_USERS_ADMIN = _ICO.format(
    inner='<path stroke-linecap="round" stroke-linejoin="round" d="M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.433-2.554M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zm8.25 2.25a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z"/>'
)
ICO_LOGOUT = _ICO.format(
    inner='<path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v10.5A2.25 2.25 0 007.5 18h6a2.25 2.25 0 002.25-2.25V15M12 9l-3 3m0 0l3 3m-3-3h12.75"/>'
)
ICO_GRID = _ICO.format(
    inner='<path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6A2.25 2.25 0 016 3.75h2.25A2.25 2.25 0 0110.5 6v2.25a2.25 2.25 0 01-2.25 2.25H6a2.25 2.25 0 01-2.25-2.25V6zM3.75 15.75A2.25 2.25 0 016 13.5h2.25a2.25 2.25 0 012.25 2.25V18a2.25 2.25 0 01-2.25 2.25H6A2.25 2.25 0 013.75 18v-2.25zM13.5 6a2.25 2.25 0 012.25-2.25H18A2.25 2.25 0 0120.25 6v2.25a2.25 2.25 0 01-2.25 2.25H15.75a2.25 2.25 0 01-2.25-2.25V6zM13.5 15.75a2.25 2.25 0 012.25-2.25H18a2.25 2.25 0 012.25 2.25V18A2.25 2.25 0 0118 20.25h-2.25a2.25 2.25 0 01-2.25-2.25v-2.25z"/>'
)
ICO_BRIEFCASE = _ICO.format(
    inner='<path stroke-linecap="round" stroke-linejoin="round" d="M20.25 14.15v4.25c0 1.094-.787 2-1.75 2H5.5c-.963 0-1.75-.906-1.75-2v-4.15m18.5 0a2.25 2.25 0 00-2.25-2.25H5.25a2.25 2.25 0 00-2.25 2.25m18.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 16.308a2.25 2.25 0 01-1.07-1.916v-.243m18.5 0a2.25 2.25 0 00-2.25-2.25H5.25a2.25 2.25 0 00-2.25 2.25"/>'
)
ICO_CHART = _ICO.format(
    inner='<path stroke-linecap="round" stroke-linejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75zM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V8.625zM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V4.125z"/>'
)
ICO_SCALE = _ICO.format(
    inner='<path stroke-linecap="round" stroke-linejoin="round" d="M12 3v17.25m0 0c-1.472 0-2.882.265-4.185.75M12 20.25c1.472 0 2.882.265 4.185.75M18.75 4.97A48.416 48.416 0 0012 4.5c-2.291 0-4.545.16-6.75.47m13.5 0c1.01.143 2.01.317 3 .52m-3-.52l-2.62 10.726c-.122.499-.106 1.028.016 1.51.148.601.444 1.153.848 1.59l.004.005.005.005a2.25 2.25 0 001.856.647H18a2.25 2.25 0 002.25-2.25V6.108c0-1.198-.806-2.291-1.86-2.684M6.75 4.97A48.416 48.416 0 0112 4.5c2.291 0 4.545.16 6.75.47m-6.75-.47l-2.62 10.726c-.122.499-.106 1.028.016 1.51.148.601.444 1.153.848 1.59l.004.005.005.005a2.25 2.25 0 001.856.647H6a2.25 2.25 0 01-2.25-2.25V6.108c0-1.198.806-2.291 1.86-2.684"/>'
)
ICO_BUILDING = _ICO.format(
    inner='<path stroke-linecap="round" stroke-linejoin="round" d="M2.25 21h19.5m-18-18v18m10.5-18v18m6-13.5V21M6.75 6.75h.75m-.75 3h.75m-.75 3h.75m3-6h.75m-.75 3h.75m-.75 3h.75M6.75 21v-3.375c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21M3 3h12m-.75 4.5H21m-3.75 3.75h.008v.008H18v-.008zm0 3h.008v.008H18V18zm-3 3h.008v.008H15V21zm0-3h.008v.008H15V18zm0-3h.008v.008H15V15zm-3 3h.008v.008H12V18zm0-3h.008v.008H12V15zm0-3h.008v.008H12V12zm-3 3h.008v.008H9V18zm0-3h.008v.008H9V15zm0-3h.008v.008H9V12zm-3 3h.008v.008H6V18zm0-3h.008v.008H6V15zm0-3h.008v.008H6V12z"/>'
)


def _icon_for_department(name: str) -> str:
    n = (name or "").lower()
    if "rrhh" in n or "humano" in n or "recursos" in n:
        return ICO_USERS_ADMIN
    if "venta" in n:
        return ICO_CHART
    if "legal" in n:
        return ICO_SCALE
    if "admin" in n:
        return ICO_BRIEFCASE
    if "general" in n:
        return ICO_GRID
    return ICO_BUILDING


def _sidebar_nav_row(icon_html: str, label: str, button_key: str, *, active: bool) -> bool:
    """Una fila de menú: icono + botón. Devuelve True si el botón se pulsó en este run."""
    ic, bc = st.sidebar.columns([0.14, 0.86])
    with ic:
        accent = (
            "border-left:3px solid #003a40;margin-left:-2px;padding-left:6px;border-radius:2px;"
            if active
            else ""
        )
        st.markdown(
            f'<div class="tc-nav-icon-wrap" style="{accent}">{icon_html}</div>',
            unsafe_allow_html=True,
        )
    with bc:
        return st.button(label, key=button_key, use_container_width=True)


def _dept_nav_key(dept: str) -> str:
    safe = "".join(c if c.isalnum() else "_" for c in dept).strip("_")[:36]
    return f"tc_nav_d_{safe or 'x'}"


def _render_profile_page(*, full_name: str, role_name: str, email: str) -> None:
    st.header("Perfil")
    st.markdown(f"**Nombre:** {full_name}")
    st.markdown(f"**Rol:** {role_name}")
    st.markdown(f"**Correo:** {email}")


st.set_page_config(
    page_title="Total Capital Intranet",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inyectar CSS personalizado
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Flujo de registro (Supabase) - NO depende de credentials.yaml
if st.query_params.get("page") == "register":
    st.markdown(LOGIN_PAGE_CSS, unsafe_allow_html=True)
    st.markdown('<div class="login-page">', unsafe_allow_html=True)
    col_left, col_right = st.columns([1, 1])

    logo_path = Path(__file__).parent / "assets" / "logo.png"

    def _render_branding(logo_path: Path) -> None:
        logo_b64 = ""
        if logo_path.exists():
            with open(logo_path, "rb") as f:
                logo_b64 = base64.b64encode(f.read()).decode("utf-8")
        st.markdown(
            '<div class="login-branding-box">'
            + (
                f'<img src="data:image/png;base64,{logo_b64}" alt="Total Capital" class="login-branding-logo"/>'
                if logo_b64
                else ""
            )
            + '<h3 class="login-branding-title">Bienvenido a Total Capital</h3>'
            + '<p class="login-branding-subtitle">Intranet de automatización y herramientas internas.</p>'
            + "</div>",
            unsafe_allow_html=True,
        )

    with col_left:
        st.subheader("Crear cuenta")
        st.markdown(
            '<p class="login-register-prompt">¿Ya tienes cuenta? <a href="?">Inicia sesión</a></p>',
            unsafe_allow_html=True,
        )
        with st.form("form_register", clear_on_submit=True):
            reg_username = st.text_input("Usuario", key="reg_username", placeholder="ej: mi_usuario")
            reg_password = st.text_input(
                "Contraseña", type="password", key="reg_password", placeholder="Elige una contraseña"
            )
            reg_name = st.text_input("Nombre (opcional)", key="reg_name", placeholder="Tu nombre")
            reg_department = st.selectbox(
                "Departamento",
                options=["General", "Administración", "RRHH", "Ventas"],
                key="reg_department",
            )
            submitted = st.form_submit_button("Registrarme")
            if submitted:
                if not reg_username or not reg_password:
                    st.error("Usuario y contraseña son obligatorios.")
                else:
                    username = reg_username.strip().lower()
                    email = username if "@" in username else f"{username}@totalcapital.com"
                    user_metadata = {
                        "username": username,
                        "name": (reg_name or reg_username).strip() or username,
                        "department": reg_department,
                    }
                    ok, msg = supabase_sign_up(email=email, password=reg_password, user_metadata=user_metadata)
                    if ok:
                        st.success(msg)
                        st.info("Luego de confirmar el correo, inicia sesión.")
                        st.query_params.clear()
                        st.rerun()
                    else:
                        st.error(msg)

    with col_right:
        _render_branding(logo_path)
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# Login / sesión con Supabase Auth
def _normalize_email(user_or_email: str) -> str:
    value = (user_or_email or "").strip().lower()
    if not value:
        return ""
    if "@" in value:
        return value
    # Compatibilidad con tu register actual: usuario -> usuario@totalcapital.com
    return f"{value}@totalcapital.com"


access_token = st.session_state.get("supabase_access_token")
user_id = st.session_state.get("supabase_user_id")

logo_path = Path(__file__).parent / "assets" / "logo.png"


def _render_branding(logo_path: Path) -> None:
    logo_b64 = ""
    if logo_path.exists():
        with open(logo_path, "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode("utf-8")
    st.markdown(
        '<div class="login-branding-box">'
        + (
            f'<img src="data:image/png;base64,{logo_b64}" alt="Total Capital" class="login-branding-logo"/>'
            if logo_b64
            else ""
        )
        + '<h3 class="login-branding-title">Bienvenido a Total Capital</h3>'
        + '<p class="login-branding-subtitle">Intranet de automatización y herramientas internas.</p>'
        + "</div>",
        unsafe_allow_html=True,
    )


if not access_token or not user_id:
    st.markdown(LOGIN_PAGE_CSS, unsafe_allow_html=True)
    st.markdown('<div class="login-page">', unsafe_allow_html=True)
    col_left, col_right = st.columns([1, 1])
    with col_left:
        st.subheader("Iniciar sesión")
        with st.form("form_login", clear_on_submit=True):
            login_user = st.text_input(
                "Usuario o email",
                key="login_user",
                placeholder="ej: mi_usuario o correo@dominio.com",
            )
            login_password = st.text_input(
                "Contraseña",
                type="password",
                key="login_password",
                placeholder="Tu contraseña",
            )
            submitted = st.form_submit_button("Ingresar")
            if submitted:
                email = _normalize_email(login_user)
                if not email or not login_password:
                    st.error("Usuario/email y contraseña son obligatorios.")
                else:
                    ok, data_or_msg = supabase_sign_in(email=email, password=login_password)
                    if not ok:
                        st.error(str(data_or_msg))
                    else:
                        data = data_or_msg
                        access_token = data.get("access_token")
                        user_obj = data.get("user") or {}
                        new_user_id = user_obj.get("id")
                        if access_token and new_user_id:
                            st.session_state["supabase_access_token"] = access_token
                            st.session_state["supabase_user_id"] = new_user_id
                            st.session_state["supabase_email"] = user_obj.get("email") or email
                            st.rerun()
                        else:
                            st.error("Sesión inválida: Supabase no devolvió usuario/token.")

        st.markdown("---")
        st.markdown(
            '<p class="login-register-prompt">¿No tienes cuenta? <a href="?page=register">Regístrate</a></p>',
            unsafe_allow_html=True,
        )

    with col_right:
        _render_branding(logo_path)

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# Usuario autenticado
try:
    ok, users_rows = supabase_rest_select(
        table_or_view="users",
        access_token=access_token,
        query_params={"select": "id,full_name,role_id,active", "id": f"eq.{user_id}", "limit": "1"},
    )
    if not ok:
        # Fallback si aún no existe la columna `active` en tu tabla.
        if "active" in str(users_rows):
            ok, users_rows = supabase_rest_select(
                table_or_view="users",
                access_token=access_token,
                query_params={"select": "id,full_name,role_id", "id": f"eq.{user_id}", "limit": "1"},
            )
        if not ok:
            raise RuntimeError(str(users_rows))
    if not users_rows:
        st.error("Tu usuario no existe en `public.users`. Contacta con un admin.")
        st.session_state.pop("supabase_access_token", None)
        st.session_state.pop("supabase_user_id", None)
        st.stop()

    user_row = users_rows[0]
    full_name = user_row.get("full_name") or st.session_state.get("supabase_email") or user_id
    role_id = user_row.get("role_id")
    user_active = bool(user_row.get("active", True))
    if not user_active:
        st.error("Tu cuenta está desactivada. Contacta a un admin.")
        st.session_state.pop("supabase_access_token", None)
        st.session_state.pop("supabase_user_id", None)
        st.stop()

    ok, role_rows = supabase_rest_select(
        table_or_view="roles",
        access_token=access_token,
        query_params={"select": "name", "id": f"eq.{role_id}", "limit": "1"},
    )
    role_name = "user"
    if ok and role_rows:
        role_name = role_rows[0].get("name") or "user"

    # Departamentos disponibles para el usuario
    departamento_options: list[str] = []
    if role_name == "admin":
        ok, dept_rows = supabase_rest_select(
            table_or_view="departments",
            access_token=access_token,
            query_params={"select": "name", "order": "name"},
        )
        if ok:
            departamento_options = [str(r.get("name")) for r in dept_rows if r.get("name")]
    else:
        ok, ud_rows = supabase_rest_select(
            table_or_view="user_departments",
            access_token=access_token,
            query_params={"select": "department_id", "user_id": f"eq.{user_id}"},
        )
        dept_ids = []
        if ok:
            for r in ud_rows:
                if r.get("department_id"):
                    dept_ids.append(str(r["department_id"]))

        if dept_ids:
            ids_param = ",".join(dept_ids)
            ok, dept_rows = supabase_rest_select(
                table_or_view="departments",
                access_token=access_token,
                query_params={"select": "name", "id": f"in.({ids_param})", "order": "name"},
            )
            if ok:
                departamento_options = [str(r.get("name")) for r in dept_rows if r.get("name")]

    if not departamento_options:
        st.warning("No se encontraron departamentos para tu usuario.")
        st.stop()

    # Navegación lateral (session_state se lee después de pintar los botones)
    if "nav_main" not in st.session_state:
        st.session_state["nav_main"] = "tools"
    if "nav_department" not in st.session_state:
        st.session_state["nav_department"] = departamento_options[0]

    if st.session_state["nav_department"] not in departamento_options:
        st.session_state["nav_department"] = departamento_options[0]

    if st.session_state["nav_main"] == "users" and role_name != "admin":
        st.session_state["nav_main"] = "tools"
        st.session_state["nav_department"] = departamento_options[0]

    # ——— Barra lateral (estilo limpio: marca, menú con iconos, logout abajo) ———
    if logo_path.exists():
        st.sidebar.image(str(logo_path), width=108)
    st.sidebar.markdown('<p class="tc-sidebar-brand-title">Total Capital</p>', unsafe_allow_html=True)
    st.sidebar.caption(f"{full_name} · {role_name}")
    st.sidebar.markdown('<p class="tc-sidebar-section-label">Menú</p>', unsafe_allow_html=True)

    nm = st.session_state["nav_main"]
    nd = st.session_state["nav_department"]

    if _sidebar_nav_row(ICO_USER, "Perfil", "tc_nav_profile", active=(nm == "profile")):
        st.session_state["nav_main"] = "profile"

    for dept in departamento_options:
        if _sidebar_nav_row(
            _icon_for_department(dept),
            dept,
            _dept_nav_key(dept),
            active=(nm == "tools" and nd == dept),
        ):
            st.session_state["nav_main"] = "tools"
            st.session_state["nav_department"] = dept

    if role_name == "admin":
        if _sidebar_nav_row(
            ICO_USERS_ADMIN,
            "Usuarios",
            "tc_nav_users",
            active=(nm == "users"),
        ):
            st.session_state["nav_main"] = "users"

    st.sidebar.markdown("---")
    st.sidebar.caption("Intranet de Automatización v1.0")

    if _sidebar_nav_row(ICO_LOGOUT, "Cerrar sesión", "tc_nav_logout", active=False):
        st.session_state.pop("supabase_access_token", None)
        st.session_state.pop("supabase_user_id", None)
        st.session_state.pop("nav_main", None)
        st.session_state.pop("nav_department", None)
        st.rerun()

    nav_main = st.session_state["nav_main"]
    nav_department = st.session_state["nav_department"]
    user_email = st.session_state.get("supabase_email") or ""

    if nav_main == "profile":
        _render_profile_page(full_name=full_name, role_name=role_name, email=user_email)
    elif nav_main == "users":
        render_users_ui(access_token=access_token, current_user_id=user_id)
    else:
        MODULES = {
            "Administración": admin_ui.render,
            "RRHH": lambda: st.info("Módulo RRHH - Próximamente."),
            "Ventas": lambda: st.info("Módulo Ventas - Próximamente."),
            "Legal": lambda: st.info("Módulo Legal - Próximamente."),
        }

        render_fn = MODULES.get(nav_department)
        if render_fn:
            render_fn()
        else:
            st.warning(f"No hay módulo implementado para: {nav_department}")
except Exception as e:
    st.error(f"Error al cargar sesión Supabase: {e}")
    st.info("Revisa que las tablas `public.users`, `public.roles`, `public.departments` y `public.user_departments` existan y que RLS permita leer los datos del usuario.")
