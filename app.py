"""Punto de entrada principal - Intranet Total Capital."""

import base64
from pathlib import Path

import streamlit as st

from config.theme import CUSTOM_CSS, LOGIN_PAGE_CSS
from config.supabase_auth import supabase_rest_select, supabase_sign_in, supabase_sign_up
from modules.admin import admin_ui
from modules.admin.users_ui import render as render_users_ui

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

    # Barra lateral
    if logo_path.exists():
        st.sidebar.image(str(logo_path), width=140)
    st.sidebar.markdown("---")
    st.sidebar.title("Total Capital")
    st.sidebar.markdown(f"**Hola, {full_name}**")
    st.sidebar.markdown(f"Rol: `{role_name}`")
    st.sidebar.markdown("---")

    if st.sidebar.button("Cerrar sesión", use_container_width=True):
        st.session_state.pop("supabase_access_token", None)
        st.session_state.pop("supabase_user_id", None)
        st.rerun()

    if role_name == "admin":
        seccion = st.sidebar.radio("Sección", ["Herramientas", "Usuarios"], index=0)
    else:
        seccion = "Herramientas"

    if seccion == "Usuarios":
        render_users_ui(access_token=access_token, current_user_id=user_id)
        st.stop()

    departamento = st.sidebar.selectbox(
        "Departamento",
        options=departamento_options,
        help="Selecciona el departamento para acceder a sus herramientas.",
    )

    st.sidebar.markdown("---")
    st.sidebar.caption("Intranet de Automatización v1.0")

    # Enrutamiento según departamento seleccionado
    MODULES = {
        "Administración": admin_ui.render,
        "RRHH": lambda: st.info("Módulo RRHH - Próximamente."),
        "Ventas": lambda: st.info("Módulo Ventas - Próximamente."),
        "Legal": lambda: st.info("Módulo Legal - Próximamente."),
    }

    render_fn = MODULES.get(departamento)
    if render_fn:
        render_fn()
    else:
        st.warning(f"No hay módulo implementado para: {departamento}")
except Exception as e:
    st.error(f"Error al cargar sesión Supabase: {e}")
    st.info("Revisa que las tablas `public.users`, `public.roles`, `public.departments` y `public.user_departments` existan y que RLS permita leer los datos del usuario.")
