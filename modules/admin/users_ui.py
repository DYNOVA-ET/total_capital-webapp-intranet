"""Panel admin para gestionar usuarios.

Requiere que el rol del usuario autenticado sea `admin` según `public.users.role_id`.
"""

from __future__ import annotations

import base64
import hashlib
import html
from datetime import datetime
from typing import Any

import streamlit as st

from config.supabase_auth import (
    supabase_admin_create_user,
    supabase_admin_delete_user,
    supabase_admin_update_user_password,
    supabase_log_audit,
    supabase_rest_delete,
    supabase_rest_patch,
    supabase_rest_post,
    supabase_rest_select,
)
from config.password_validator import validate_password_strength, get_password_checklist

USERS_PAGE_CSS = """
<style>
.tc-users-head {
    margin-bottom: 1.25rem;
}
.tc-users-title-row {
    display: flex;
    align-items: baseline;
    flex-wrap: wrap;
    gap: 0.5rem 0.75rem;
    margin: 0 0 0.35rem 0;
}
.tc-users-title {
    font-family: 'Montserrat', 'Poppins', sans-serif;
    font-size: 1.65rem;
    font-weight: 700;
    color: #111827 !important;
    margin: 0 !important;
    letter-spacing: -0.02em;
}
.tc-users-count {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 1.75rem;
    height: 1.5rem;
    padding: 0 0.45rem;
    font-size: 0.8rem;
    font-weight: 600;
    color: #6b7280;
    background: #f3f4f6;
    border-radius: 6px;
}
.tc-users-subtitle {
    margin: 0;
    font-size: 0.95rem;
    color: #6b7280 !important;
    line-height: 1.45;
}
.tc-users-table-wrap {
    width: 100%;
    overflow-x: auto;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    background: #fff;
    margin-bottom: 1.25rem;
}
.tc-users-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.875rem;
}
.tc-users-table thead th {
    text-align: left;
    padding: 0.85rem 1rem;
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #9ca3af;
    background: #f9fafb;
    border-bottom: 1px solid #e5e7eb;
    white-space: nowrap;
}
.tc-users-table tbody td {
    padding: 0.75rem 1rem;
    border-bottom: 1px solid #f3f4f6;
    vertical-align: middle;
    color: #374151;
}
.tc-users-table tbody tr:last-child td {
    border-bottom: none;
}
.tc-users-table tbody tr:hover td {
    background: #fafafa;
}
.tc-users-cell-name {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    min-width: 180px;
}
.tc-user-avatar {
    flex-shrink: 0;
    width: 2.25rem;
    height: 2.25rem;
    border-radius: 9999px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.7rem;
    font-weight: 700;
    color: #fff !important;
    letter-spacing: 0.02em;
}
.tc-users-name-text {
    font-weight: 600;
    color: #111827 !important;
}
.tc-users-mail a {
    color: #2563eb !important;
    text-decoration: underline;
    font-weight: 400;
}
.tc-users-mail a:hover {
    color: #1d4ed8 !important;
}
.tc-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.25rem 0.65rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 600;
    white-space: nowrap;
}
.tc-badge-active {
    background: #dcfce7;
    color: #166534 !important;
}
.tc-badge-inactive {
    background: #fee2e2;
    color: #991b1b !important;
}
.tc-badge-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: currentColor;
    opacity: 0.85;
}
.tc-users-footer {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
    padding: 0.5rem 0 0;
    font-size: 0.8rem;
    color: #6b7280 !important;
}
.tc-users-empty {
    padding: 2.5rem 1.5rem;
    text-align: center;
    color: #6b7280;
    border: 1px dashed #e5e7eb;
    border-radius: 12px;
    background: #f9fafb;
}
</style>
"""

# Iconos en línea (misma línea visual que el navbar / Heroicons outline)
_ICO_LINE = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" '
    'viewBox="0 0 24 24" stroke-width="1.5" stroke="#3f3f46">'
    '<path stroke-linecap="round" stroke-linejoin="round" d="{d}"/></svg>'
)
_ICO_EDIT_LINE = _ICO_LINE.format(
    d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125",
)
_ICO_KEY_LINE = _ICO_LINE.format(
    d="M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z",
)
_ICO_TRASH_LINE = _ICO_LINE.format(
    d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0",
)


def _svg_icon_button_label(svg: str) -> str:
    """Imagen en Markdown para `st.button` (icono vectorial, no emoji)."""
    b64 = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return f"![](data:image/svg+xml;base64,{b64})"


def _strip_legacy_admin_user_query_params() -> None:
    """Si la URL trae params viejos de enlaces <a>, abre el modal y limpia la barra (sin recarga completa)."""
    mapping = (
        ("admin_edit_user", "admin_open_edit_uid"),
        ("admin_delete_user", "admin_open_delete_uid"),
    )
    for qp_key, ss_key in mapping:
        if qp_key not in st.query_params:
            continue
        raw = st.query_params[qp_key]
        val = raw if isinstance(raw, str) else (raw[0] if raw else None)
        if val:
            st.session_state[ss_key] = str(val)
            if ss_key == "admin_open_edit_uid":
                st.session_state.pop("admin_open_delete_uid", None)
            else:
                st.session_state.pop("admin_open_edit_uid", None)
        try:
            del st.query_params[qp_key]
        except Exception:
            pass


def _delete_user_everywhere(*, access_token: str, user_id: str) -> tuple[bool, str]:
    """Quita departamentos, fila en public.users y usuario en Auth (con reintentos según FK)."""
    uid = str(user_id).strip()

    ok_auth, err_auth = supabase_admin_delete_user(user_id=uid)
    if ok_auth:
        return True, ""

    ok_d, res_d = supabase_rest_delete(
        table_or_view="user_departments",
        access_token=access_token,
        query_params={"user_id": f"eq.{uid}"},
    )
    if not ok_d:
        return False, f"user_departments: {res_d}"

    ok_u, res_u = supabase_rest_delete(
        table_or_view="users",
        access_token=access_token,
        query_params={"id": f"eq.{uid}"},
    )
    if not ok_u:
        return False, f"users: {res_u}"

    ok_auth2, err_auth2 = supabase_admin_delete_user(user_id=uid)
    if ok_auth2:
        return True, ""
    return False, str(err_auth2 or err_auth)


def _sql_hint_for_missing_column(column_name: str) -> str:
    return (
        f"Falta la columna `{column_name}` en `public.users`. "
        "Ejecuta en Supabase SQL Editor: "
        f"`alter table public.users add column if not exists {column_name} boolean default true;`"
    )


def _initials(full_name: str, email: str) -> str:
    n = (full_name or "").strip()
    if n:
        parts = n.split()
        if len(parts) >= 2:
            return (parts[0][0] + parts[-1][0]).upper()
        return (n[:2]).upper()
    local = (email or "").split("@")[0].strip()
    return (local[:2] or "?").upper()


def _avatar_color(seed: str) -> str:
    h = int(hashlib.md5(seed.encode("utf-8"), usedforsecurity=False).hexdigest()[:8], 16)
    hue = h % 360
    return f"hsl({hue} 42% 42%)"


_MESES_CORTO = (
    "ene",
    "feb",
    "mar",
    "abr",
    "may",
    "jun",
    "jul",
    "ago",
    "sep",
    "oct",
    "nov",
    "dic",
)


def _fmt_joined(val: Any) -> str:
    if val is None or val == "":
        return "—"
    s = str(val).replace("Z", "+00:00")
    try:
        if "T" in s:
            raw = s.replace("Z", "")
            if raw.endswith("+00:00"):
                raw = raw[:-6]
            dt = datetime.fromisoformat(raw)
            mes = _MESES_CORTO[dt.month - 1]
            return f"{dt.day} {mes} {dt.year}, {dt.strftime('%H:%M')}"
    except (ValueError, TypeError):
        pass
    return s[:16] if len(s) > 16 else s


def _fetch_users(access_token: str) -> tuple[bool, list[dict[str, Any]] | str, bool]:
    """Devuelve (ok, filas o mensaje de error, tiene_created_at)."""
    select_variants = (
        "id,full_name,email,role_id,active,created_at",
        "id,full_name,email,role_id,active",
        "id,full_name,role_id,active",
    )
    last_err = ""
    for users_select in select_variants:
        ok, users_rows = supabase_rest_select(
            table_or_view="users",
            access_token=access_token,
            query_params={"select": users_select, "order": "full_name"},
        )
        if ok:
            has_ca = "created_at" in users_select
            return True, users_rows, has_ca
        last_err = str(users_rows)
        if "active" in last_err and "column" in last_err:
            return False, _sql_hint_for_missing_column("active"), False
    return False, last_err, False


def render(*, access_token: str, current_user_id: str) -> None:
    st.markdown(USERS_PAGE_CSS, unsafe_allow_html=True)
    _strip_legacy_admin_user_query_params()

    ok, roles_rows = supabase_rest_select(
        table_or_view="roles",
        access_token=access_token,
        query_params={"select": "id,name", "order": "name"},
    )
    if not ok:
        st.error(f"No se pudo leer `roles`: {roles_rows}")
        return
    roles = [{"id": r["id"], "name": r["name"]} for r in roles_rows if r.get("id")]

    ok, departments_rows = supabase_rest_select(
        table_or_view="departments",
        access_token=access_token,
        query_params={"select": "id,name", "order": "name"},
    )
    if not ok:
        st.error(f"No se pudo leer `departments`: {departments_rows}")
        return
    departments = [{"id": d["id"], "name": d["name"]} for d in departments_rows if d.get("id")]

    role_id_to_name = {str(r["id"]): str(r["name"]) for r in roles}
    dept_id_to_name = {str(d["id"]): str(d["name"]) for d in departments}

    @st.dialog("Crear usuario")
    def _create_user_dialog() -> None:
        st.caption("Se crea el usuario en Supabase Auth y se poblarán tablas con el trigger.")

        with st.form("form_create_user", clear_on_submit=False):
            full_name = st.text_input("Nombre", placeholder="SEBASTIAN VALLEJO")
            email = st.text_input("Correo", placeholder="sebastian@dynovaet.com")
            role_name = st.selectbox(
                "Rol",
                options=[r["name"] for r in roles],
                index=([r["name"] for r in roles].index("user") if "user" in [r["name"] for r in roles] else 0),
            )
            dept_names = st.multiselect(
                "Departamentos",
                options=[d["name"] for d in departments],
                default=[d["name"] for d in departments if d["name"] == "General"],
            )
            password = st.text_input("Contraseña", type="password")

            submitted = st.form_submit_button("Crear usuario")
            if submitted:
                if not full_name or not email or not password:
                    st.error("Nombre, correo y contraseña son obligatorios.")
                    return
                if not dept_names:
                    st.error("Selecciona al menos un departamento.")
                    return

                ok_c, res = supabase_admin_create_user(
                    email=email,
                    password=password,
                    full_name=full_name,
                    role_name=role_name,
                    departments=dept_names,
                    email_confirm=True,
                )
                if not ok_c:
                    st.error(f"No se pudo crear el usuario: {res}")
                    return

                # Log audit
                supabase_log_audit(
                    access_token=access_token,
                    user_id=current_user_id,  # Admin who created
                    action="user_created",
                    resource_type="user",
                    resource_id=res.get("user_id") if isinstance(res, dict) else None,
                    new_values={
                        "email": email,
                        "full_name": full_name,
                        "role": role_name,
                        "departments": dept_names,
                    },
                )

                try:
                    st.toast("Usuario creado con éxito.")
                except Exception:
                    st.success("Usuario creado con éxito.")
                st.rerun()

    ok_u, users_payload, has_created_at = _fetch_users(access_token)
    if not ok_u:
        if isinstance(users_payload, str) and users_payload.startswith("Falta la columna"):
            st.error(users_payload)
        else:
            st.error(f"No se pudo leer `public.users`: {users_payload}")
        return

    users_rows = users_payload
    if not isinstance(users_rows, list):
        st.error("Respuesta inesperada al leer usuarios.")
        return

    users: list[dict[str, Any]] = users_rows
    n_total = len(users)

    @st.dialog("Editar usuario")
    def _edit_user_dialog(selected_user_id: str) -> None:
        su = next((u for u in users if str(u.get("id")) == selected_user_id), None)
        if not su:
            st.error("Usuario no encontrado.")
            return
        ks = f"ed_{selected_user_id}_"
        st.caption(str(su.get("email") or "Sin correo"))

        selected_full_name = st.text_input("Nombre", value=str(su.get("full_name") or ""), key=f"{ks}fn")
        st.text_input("Email", value=str(su.get("email") or ""), disabled=True, key=f"{ks}em")

        selected_active = st.checkbox("Activo", value=bool(su.get("active", True)), key=f"{ks}act")

        cur_rid = su.get("role_id")
        sel_role = st.selectbox(
            "Rol",
            options=[r["id"] for r in roles],
            index=([r["id"] for r in roles].index(cur_rid) if cur_rid in [r["id"] for r in roles] else 0),
            format_func=lambda rid: role_id_to_name.get(str(rid), str(rid)),
            key=f"{ks}role",
        )

        ok_ud, ud_rows = supabase_rest_select(
            table_or_view="user_departments",
            access_token=access_token,
            query_params={"select": "department_id", "user_id": f"eq.{selected_user_id}"},
        )
        def_dept: list[str] = []
        if ok_ud and isinstance(ud_rows, list):
            def_dept = [str(r["department_id"]) for r in ud_rows if r.get("department_id")]

        sel_depts = st.multiselect(
            "Departamentos",
            options=[d["id"] for d in departments],
            default=def_dept,
            format_func=lambda did: dept_id_to_name.get(str(did), str(did)),
            key=f"{ks}dept",
        )

        if st.button("Guardar cambios", type="primary", use_container_width=True, key=f"{ks}save"):
            if str(selected_user_id) == str(current_user_id) and str(sel_role) != str(
                next((r["id"] for r in roles if r["name"] == "admin"), "")
            ):
                st.warning(
                    "Estás cambiando tu propio rol fuera de admin; podrías perder acceso al guardar."
                )

            ok_p, res = supabase_rest_patch(
                table_or_view="users",
                access_token=access_token,
                query_params={"id": f"eq.{selected_user_id}"},
                payload={
                    "full_name": selected_full_name,
                    "active": bool(selected_active),
                    "role_id": sel_role,
                },
            )
            if not ok_p:
                st.error(f"No se pudo actualizar `users`: {res}")
                return

            ok_del, res_del = supabase_rest_delete(
                table_or_view="user_departments",
                access_token=access_token,
                query_params={"user_id": f"eq.{selected_user_id}"},
            )
            if not ok_del:
                st.error(f"No se pudo limpiar `user_departments`: {res_del}")
                return

            if sel_depts:
                payload = [{"user_id": selected_user_id, "department_id": did} for did in sel_depts]
                ok_po, res_post = supabase_rest_post(
                    table_or_view="user_departments",
                    access_token=access_token,
                    query_params=None,
                    payload=payload,
                )
                if not ok_po:
                    st.error(f"No se pudo insertar `user_departments`: {res_post}")
                    return

            st.session_state.pop("admin_open_edit_uid", None)
            try:
                st.toast("Cambios guardados con éxito.")
            except Exception:
                st.success("Cambios guardados con éxito.")
            
            # Log audit
            supabase_log_audit(
                access_token=access_token,
                user_id=current_user_id,
                action="user_updated",
                resource_type="user",
                resource_id=selected_user_id,
                old_values={
                    "full_name": su.get("full_name"),
                    "active": su.get("active"),
                    "role_id": su.get("role_id"),
                },
                new_values={
                    "full_name": selected_full_name,
                    "active": selected_active,
                    "role_id": sel_role,
                    "departments": sel_depts,
                },
            )
            
            st.rerun()

        if st.button("Cerrar", use_container_width=True, key=f"{ks}close"):
            st.session_state.pop("admin_open_edit_uid", None)
            st.rerun()

    @st.dialog("Cambiar contraseña")
    def _change_password_dialog(selected_user_id: str) -> None:
        su = next((u for u in users if str(u.get("id")) == selected_user_id), None)
        if not su:
            st.error("Usuario no encontrado.")
            return
        st.caption(f"Cambiar contraseña para: {su.get('email') or 'Sin correo'}")

        pw_key = f"pw_{selected_user_id}"
        new_password = st.text_input(
            "Nueva contraseña",
            type="password",
            placeholder="Mínimo 12 caracteres, mayúsculas, números y símbolos",
            key=pw_key,
        )
        
        # Mostrar checklist si hay algo escrito
        if new_password:
            checklist = get_password_checklist(new_password)
            st.markdown("**Requisitos de la contraseña:**")
            for req, met in checklist.items():
                icon = "✅" if met else "❌"
                st.markdown(f"{icon} {req}")
        
        if st.button("Actualizar contraseña", type="primary", use_container_width=True, key=f"pw_save_{selected_user_id}"):
            new_pw_val = st.session_state.get(pw_key, "")
            if not new_pw_val:
                st.error("Escribe una nueva contraseña.")
                return
            if not validate_password_strength(new_pw_val)[0]:
                st.error(validate_password_strength(new_pw_val)[1])
                return
            ok_pw, res = supabase_admin_update_user_password(
                user_id=selected_user_id,
                new_password=new_pw_val,
                email_confirm=None,
            )
            if not ok_pw:
                st.error(f"No se pudo cambiar la contraseña: {res}")
                return
            st.session_state.pop("admin_open_change_pw_uid", None)
            try:
                st.toast("Contraseña actualizada.")
            except Exception:
                st.success("Contraseña actualizada.")
            
            # Log audit
            supabase_log_audit(
                access_token=access_token,
                user_id=current_user_id,
                action="user_password_changed",
                resource_type="user",
                resource_id=selected_user_id,
            )
            
            st.rerun()

        if st.button("Cerrar", use_container_width=True, key=f"pw_close_{selected_user_id}"):
            st.session_state.pop("admin_open_change_pw_uid", None)
            st.rerun()

    @st.dialog("Eliminar usuario")
    def _delete_user_dialog(selected_user_id: str) -> None:
        su = next((u for u in users if str(u.get("id")) == selected_user_id), None)
        if not su:
            st.error("Usuario no encontrado.")
            return
        if str(selected_user_id) == str(current_user_id):
            st.error("No puedes eliminar tu propia cuenta desde aquí.")
            return

        fn = su.get("full_name") or su.get("email") or selected_user_id
        st.warning(f"¿Eliminar definitivamente a **{fn}**? Esta acción no se puede deshacer.")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Cancelar", use_container_width=True, key=f"dl_cancel_{selected_user_id}"):
                st.session_state.pop("admin_open_delete_uid", None)
                st.rerun()
        with c2:
            if st.button("Eliminar", type="primary", use_container_width=True, key=f"dl_go_{selected_user_id}"):
                ok_del, msg = _delete_user_everywhere(access_token=access_token, user_id=selected_user_id)
                if not ok_del:
                    st.error(f"No se pudo eliminar: {msg}")
                    return
                st.session_state.pop("admin_open_delete_uid", None)
                try:
                    st.toast("Usuario eliminado.")
                except Exception:
                    st.success("Usuario eliminado.")
                
                # Log audit
                supabase_log_audit(
                    access_token=access_token,
                    user_id=current_user_id,
                    action="user_deleted",
                    resource_type="user",
                    resource_id=selected_user_id,
                    old_values={
                        "email": su.get("email"),
                        "full_name": su.get("full_name"),
                    },
                )
                
                st.rerun()

    if st.session_state.get("admin_open_edit_uid"):
        _edit_user_dialog(st.session_state["admin_open_edit_uid"])
    elif st.session_state.get("admin_open_change_pw_uid"):
        _change_password_dialog(st.session_state["admin_open_change_pw_uid"])
    elif st.session_state.get("admin_open_delete_uid"):
        _delete_user_dialog(st.session_state["admin_open_delete_uid"])

    # —— Cabecera tipo dashboard ——
    st.markdown(
        f"""
        <div class="tc-users-head">
            <div class="tc-users-title-row">
                <h1 class="tc-users-title">Gestión de usuarios</h1>
                <span class="tc-users-count">{n_total}</span>
            </div>
            <p class="tc-users-subtitle">
                Administra los miembros del equipo, roles y permisos desde aquí.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    role_names_sorted = sorted({role_id_to_name.get(str(u.get("role_id")), "—") for u in users})

    t1, t2, t3 = st.columns([2.2, 2, 1.1], gap="medium")
    with t1:
        search_q = st.text_input(
            "Buscar",
            key="admin_users_search",
            placeholder="Nombre o correo…",
        )
    with t2:
        role_pick = st.multiselect(
            "Rol",
            options=[x for x in role_names_sorted if x and x != "—"],
            key="admin_users_role_filter",
            placeholder="Todos los roles",
        )
    with t3:
        st.markdown("<div style='height:1.6rem'></div>", unsafe_allow_html=True)
        if st.button("+ Crear usuario", use_container_width=True, type="primary"):
            _create_user_dialog()

    st.markdown(
        "<div style='margin:0 0 1rem 0;padding-bottom:1rem;border-bottom:1px solid #e5e7eb'></div>",
        unsafe_allow_html=True,
    )

    sq = (search_q or "").strip().lower()
    active_roles = set(role_pick) if role_pick else None

    def _passes_filters(u: dict[str, Any]) -> bool:
        rname = role_id_to_name.get(str(u.get("role_id")), "")
        if active_roles is not None and rname not in active_roles:
            return False
        if not sq:
            return True
        fn = (u.get("full_name") or "").lower()
        em = (u.get("email") or "").lower()
        return sq in fn or sq in em

    filtered = [u for u in users if _passes_filters(u)]
    n_filt = len(filtered)

    sig = f"{sq}|{','.join(sorted(active_roles or []))}"
    if st.session_state.get("admin_users_filter_sig") != sig:
        st.session_state["admin_users_page_idx"] = 0
        st.session_state["admin_users_filter_sig"] = sig

    prev_pp = st.session_state.get("admin_users_prev_per_page")
    pp_c1, pp_c2 = st.columns([1, 4])
    with pp_c1:
        per_page = st.selectbox(
            "Filas por página",
            options=[10, 15, 25, 50],
            index=1,
            key="admin_users_per_page",
        )
    with pp_c2:
        st.caption("Vista tipo tabla · Usa los filtros para acotar el listado.")
    if prev_pp is not None and prev_pp != per_page:
        st.session_state["admin_users_page_idx"] = 0
    st.session_state["admin_users_prev_per_page"] = per_page

    n_pages = max(1, (n_filt + per_page - 1) // per_page)
    if "admin_users_page_idx" not in st.session_state:
        st.session_state["admin_users_page_idx"] = 0
    page_idx = min(st.session_state["admin_users_page_idx"], n_pages - 1)
    page_idx = max(0, page_idx)
    st.session_state["admin_users_page_idx"] = page_idx

    start = page_idx * per_page
    chunk = filtered[start : start + per_page]
    end_show = start + len(chunk)

    if not filtered:
        st.markdown(
            '<p class="tc-users-empty">No hay usuarios que coincidan con los filtros.</p>',
            unsafe_allow_html=True,
        )
    else:
        joined_header = "Fecha de alta"
        _gw = [2.35, 2.65, 1.05, 1.2, 1.35, 1.05]
        _hlabs = (
            "Nombre completo",
            "Correo",
            "Rol",
            "Estado",
            joined_header,
            "Acciones",
        )
        with st.container(border=True):
            hdr = st.columns(_gw, gap="small")
            for i, lab in enumerate(_hlabs):
                align = "text-align:right;" if i == len(_hlabs) - 1 else ""
                hdr[i].markdown(
                    f'<span style="font-size:0.7rem;font-weight:600;text-transform:uppercase;'
                    f'letter-spacing:0.05em;color:#9ca3af;{align}display:block;">{html.escape(lab)}</span>',
                    unsafe_allow_html=True,
                )
            st.markdown(
                '<div style="height:1px;background:#e5e7eb;margin:0.35rem 0 0.5rem 0"></div>',
                unsafe_allow_html=True,
            )

            for row_i, u in enumerate(chunk):
                uid = str(u.get("id") or "")
                fn = u.get("full_name") or "—"
                em = u.get("email") or ""
                rname = role_id_to_name.get(str(u.get("role_id")), "—")
                is_active = bool(u.get("active", True))
                joined = _fmt_joined(u.get("created_at")) if has_created_at else "—"

                ini = html.escape(_initials(str(fn), str(em)))
                av_bg = _avatar_color(uid or em or fn)
                fn_e = html.escape(str(fn))
                em_e = html.escape(str(em))
                mail_href = html.escape(f"mailto:{em}", quote=True) if em else "#"
                r_e = html.escape(str(rname))

                if is_active:
                    badge = (
                        '<span class="tc-badge tc-badge-active">'
                        '<span class="tc-badge-dot"></span>Activo</span>'
                    )
                else:
                    badge = (
                        '<span class="tc-badge tc-badge-inactive">'
                        '<span class="tc-badge-dot"></span>Inactivo</span>'
                    )

                mail_cell = f'<a href="{mail_href}">{em_e}</a>' if em else "—"

                row = st.columns(_gw, gap="small")
                with row[0]:
                    st.markdown(
                        f'<div class="tc-users-cell-name">'
                        f'<div class="tc-user-avatar" style="background:{av_bg}">{ini}</div>'
                        f'<span class="tc-users-name-text">{fn_e}</span></div>',
                        unsafe_allow_html=True,
                    )
                with row[1]:
                    st.markdown(
                        f'<div class="tc-users-mail">{mail_cell}</div>',
                        unsafe_allow_html=True,
                    )
                with row[2]:
                    st.markdown(
                        f'<span style="color:#374151;font-size:0.875rem;">{r_e}</span>',
                        unsafe_allow_html=True,
                    )
                with row[3]:
                    st.markdown(badge, unsafe_allow_html=True)
                with row[4]:
                    st.markdown(
                        f'<span style="color:#374151;font-size:0.875rem;">{html.escape(joined)}</span>',
                        unsafe_allow_html=True,
                    )
                with row[5]:
                    b_ed, b_pw, b_dl = st.columns(3, gap="small")
                    with b_ed:
                        if st.button(
                            _svg_icon_button_label(_ICO_EDIT_LINE),
                            key=f"tbl_ed_{uid}_{page_idx}_{row_i}",
                            help="Editar usuario",
                            type="tertiary",
                            use_container_width=True,
                        ):
                            st.session_state["admin_open_edit_uid"] = uid
                            st.session_state.pop("admin_open_delete_uid", None)
                            st.session_state.pop("admin_open_change_pw_uid", None)
                            st.rerun()
                    with b_pw:
                        if st.button(
                            _svg_icon_button_label(_ICO_KEY_LINE),
                            key=f"tbl_pw_{uid}_{page_idx}_{row_i}",
                            help="Cambiar contraseña",
                            type="tertiary",
                            use_container_width=True,
                        ):
                            st.session_state["admin_open_change_pw_uid"] = uid
                            st.session_state.pop("admin_open_edit_uid", None)
                            st.session_state.pop("admin_open_delete_uid", None)
                            st.rerun()
                    with b_dl:
                        if st.button(
                            _svg_icon_button_label(_ICO_TRASH_LINE),
                            key=f"tbl_dl_{uid}_{page_idx}_{row_i}",
                            help="Eliminar usuario",
                            type="tertiary",
                            use_container_width=True,
                        ):
                            st.session_state["admin_open_delete_uid"] = uid
                            st.session_state.pop("admin_open_edit_uid", None)
                            st.session_state.pop("admin_open_change_pw_uid", None)
                            st.rerun()

                if row_i < len(chunk) - 1:
                    st.markdown(
                        '<div style="height:1px;background:#f3f4f6;margin:0.25rem 0"></div>',
                        unsafe_allow_html=True,
                    )

    st.markdown(
        f"""
        <div class="tc-users-footer">
            <span>Mostrando <strong>{start + 1 if n_filt else 0}–{end_show}</strong> de <strong>{n_filt}</strong> usuario(s) filtrado(s) · Total en sistema: {n_total}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c_prev, c_next, c_pp = st.columns([1, 1, 2])
    with c_prev:
        if st.button("← Anterior", disabled=page_idx <= 0, key="admin_users_prev"):
            st.session_state["admin_users_page_idx"] = max(0, page_idx - 1)
            st.rerun()
    with c_next:
        if st.button("Siguiente →", disabled=page_idx >= n_pages - 1, key="admin_users_next"):
            st.session_state["admin_users_page_idx"] = min(n_pages - 1, page_idx + 1)
            st.rerun()
    with c_pp:
        st.caption(f"Página {page_idx + 1} de {n_pages} · {per_page} filas por página")
