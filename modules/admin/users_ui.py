"""Panel admin para gestionar usuarios.

Requiere que el rol del usuario autenticado sea `admin` según `public.users.role_id`.
"""

from __future__ import annotations

from typing import Any

import streamlit as st

from config.supabase_auth import (
    supabase_rest_delete,
    supabase_rest_patch,
    supabase_rest_post,
    supabase_rest_select,
    supabase_admin_create_user,
    supabase_admin_update_user_password,
)


def _sql_hint_for_missing_column(column_name: str) -> str:
    return (
        f"Falta la columna `{column_name}` en `public.users`. "
        "Ejecuta en Supabase SQL Editor: "
        f"`alter table public.users add column if not exists {column_name} boolean default true;`"
    )


def render(*, access_token: str, current_user_id: str) -> None:
    st.subheader("Usuarios")

    # 1) Catálogos
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

    # 0) Crear usuario (admin)
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

                ok, res = supabase_admin_create_user(
                    email=email,
                    password=password,
                    full_name=full_name,
                    role_name=role_name,
                    departments=dept_names,
                    email_confirm=True,
                )
                if not ok:
                    st.error(f"No se pudo crear el usuario: {res}")
                    return

                try:
                    st.toast("Usuario creado con éxito.")
                except Exception:
                    st.success("Usuario creado con éxito.")
                st.rerun()

    if st.button("Crear usuario", use_container_width=True):
        _create_user_dialog()

    # 2) Lista de usuarios
    users_select = "id,full_name,email,role_id,active"
    ok, users_rows = supabase_rest_select(
        table_or_view="users",
        access_token=access_token,
        query_params={"select": users_select, "order": "full_name"},
    )

    if not ok:
        # Si falla por columna no existente, damos hint.
        err_msg = str(users_rows)
        if "active" in err_msg and "column" in err_msg:
            st.error(_sql_hint_for_missing_column("active"))
        elif "email" in err_msg and "column" in err_msg:
            # Reintentar sin email (solo para que el panel funcione).
            users_select = "id,full_name,role_id,active"
            ok, users_rows = supabase_rest_select(
                table_or_view="users",
                access_token=access_token,
                query_params={"select": users_select, "order": "full_name"},
            )
            if not ok:
                st.error(f"No se pudo leer `public.users`: {users_rows}")
                return
        else:
            st.error(f"No se pudo leer `public.users`: {err_msg}")
        return

    if not users_rows:
        st.info("No hay usuarios.")
        return

    # 3) Selector de usuario a editar
    def _label(u: dict[str, Any]) -> str:
        fn = u.get("full_name") or ""
        em = u.get("email") or ""
        return f"{fn} ({em})" if fn and em else (fn or em or str(u.get("id")))

    users = users_rows
    id_to_label = {str(u["id"]): _label(u) for u in users if u.get("id")}
    user_ids = list(id_to_label.keys())

    selected_user_id = st.selectbox("Selecciona un usuario", options=user_ids, format_func=lambda x: id_to_label.get(x, x))
    selected_user = next((u for u in users if str(u.get("id")) == selected_user_id), None)
    if not selected_user:
        st.error("Usuario no encontrado en el listado.")
        return

    selected_full_name = st.text_input("Nombre", value=str(selected_user.get("full_name") or ""))
    selected_email = st.text_input("Email", value=str(selected_user.get("email") or ""), disabled=True)

    # Cambiar contraseña
    st.markdown("### Cambiar contraseña")
    new_password = st.text_input("Nueva contraseña", type="password", placeholder="Ej: 12345678")

    # Active/Inactive
    selected_active = st.checkbox("Activo", value=bool(selected_user.get("active", True)))

    # Rol
    current_role_id = selected_user.get("role_id")
    selected_role_id = st.selectbox(
        "Rol",
        options=[r["id"] for r in roles],
        index=([r["id"] for r in roles].index(current_role_id) if current_role_id in [r["id"] for r in roles] else 0),
        format_func=lambda rid: role_id_to_name.get(str(rid), str(rid)),
    )

    # Departamentos (multi)
    ok, selected_ud_rows = supabase_rest_select(
        table_or_view="user_departments",
        access_token=access_token,
        query_params={"select": "department_id", "user_id": f"eq.{selected_user_id}"},
    )
    selected_dept_ids: list[str] = []
    if ok and isinstance(selected_ud_rows, list):
        selected_dept_ids = [str(r["department_id"]) for r in selected_ud_rows if r.get("department_id")]

    selected_dept_ids = st.multiselect(
        "Departamentos",
        options=[d["id"] for d in departments],
        default=selected_dept_ids,
        format_func=lambda did: dept_id_to_name.get(str(did), str(did)),
    )

    # 4) Guardar cambios
    if st.button("Guardar cambios", type="primary", use_container_width=True):
        if str(selected_user_id) == str(current_user_id) and str(selected_role_id) != str(
            next((r["id"] for r in roles if r["name"] == "admin"), "")
        ):
            st.warning("Estás intentando cambiar tu propio rol fuera de admin. Podrías perder acceso después del guardado.")

        # PATCH users
        ok, res = supabase_rest_patch(
            table_or_view="users",
            access_token=access_token,
            query_params={"id": f"eq.{selected_user_id}"},
            payload={
                "full_name": selected_full_name,
                "active": bool(selected_active),
                "role_id": selected_role_id,
            },
        )
        if not ok:
            st.error(f"No se pudo actualizar `users`: {res}")
            return

        # Actualizar user_departments (reemplazo total)
        ok, res_del = supabase_rest_delete(
            table_or_view="user_departments",
            access_token=access_token,
            query_params={"user_id": f"eq.{selected_user_id}"},
        )
        if not ok:
            st.error(f"No se pudo limpiar `user_departments`: {res_del}")
            return

        if selected_dept_ids:
            payload = [{"user_id": selected_user_id, "department_id": did} for did in selected_dept_ids]
            ok, res_post = supabase_rest_post(
                table_or_view="user_departments",
                access_token=access_token,
                query_params=None,
                payload=payload,
            )
            if not ok:
                st.error(f"No se pudo insertar `user_departments`: {res_post}")
                return

        # Notificación tipo toast (si tu versión de Streamlit lo soporta).
        try:
            st.toast("Cambios guardados con éxito.")
        except Exception:
            st.success("Cambios guardados con éxito.")
        st.rerun()

    # Botón independiente para cambiar contraseña (para no mezclar con guardar info).
    if st.button("Cambiar contraseña", use_container_width=True):
        if not new_password:
            st.error("Ingresa una nueva contraseña.")
            st.stop()

        ok, res = supabase_admin_update_user_password(
            user_id=selected_user_id,
            new_password=new_password,
            email_confirm=None,
        )
        if not ok:
            st.error(f"No se pudo cambiar la contraseña: {res}")
            return

        try:
            st.toast("Contraseña actualizada con éxito.")
        except Exception:
            st.success("Contraseña actualizada con éxito.")
        st.rerun()

