"""Persistencia de sesión Supabase en cookie (refresh_token) para sobrevivir a F5 / recarga."""

from __future__ import annotations

import streamlit as st

from config.supabase_auth import supabase_refresh_session

# Nombre de cookie estable (versión en el nombre por si cambias el formato)
COOKIE_NAME = "tc_intra_sb_rt_v1"
_MAX_AGE_SEC = 60 * 60 * 24 * 30  # 30 días


def _get_cookie_manager():
    if "_tc_cookie_manager" not in st.session_state:
        from extra_streamlit_components import CookieManager

        st.session_state["_tc_cookie_manager"] = CookieManager(key="tc_intra_cm_v1")
    return st.session_state["_tc_cookie_manager"]


def _next_cookie_op_key(prefix: str) -> str:
    n = st.session_state.get("_tc_ck_op", 0) + 1
    st.session_state["_tc_ck_op"] = n
    return f"{prefix}_{n}"


def persist_supabase_refresh_cookie(refresh_token: str) -> None:
    """Guarda el refresh token en el navegador (misma pestaña / origen)."""
    if not refresh_token:
        return
    cm = _get_cookie_manager()
    cm.set(
        COOKIE_NAME,
        refresh_token,
        key=_next_cookie_op_key("tc_rt_set"),
        max_age=_MAX_AGE_SEC,
        path="/",
        same_site="lax",
    )


def clear_supabase_refresh_cookie() -> None:
    """Elimina la cookie de sesión prolongada."""
    try:
        cm = _get_cookie_manager()
        cm.delete(COOKIE_NAME, key=_next_cookie_op_key("tc_rt_del"))
    except Exception:
        pass
    st.session_state.pop("_tc_cookie_manager", None)


def restore_supabase_session_from_cookie() -> None:
    """Si no hay sesión en session_state pero existe refresh en cookie, renueva tokens."""
    if st.session_state.get("supabase_access_token") and st.session_state.get("supabase_user_id"):
        return

    cm = _get_cookie_manager()
    rt = cm.get(COOKIE_NAME)
    if not rt:
        return

    ok, data = supabase_refresh_session(str(rt))
    if not ok or not isinstance(data, dict):
        clear_supabase_refresh_cookie()
        return

    access = data.get("access_token")
    user_obj = data.get("user") if isinstance(data.get("user"), dict) else {}
    uid = user_obj.get("id")
    if not access or not uid:
        clear_supabase_refresh_cookie()
        return

    st.session_state["supabase_access_token"] = access
    st.session_state["supabase_user_id"] = uid
    st.session_state["supabase_email"] = user_obj.get("email") or ""

    new_rt = data.get("refresh_token")
    if new_rt:
        persist_supabase_refresh_cookie(str(new_rt))


def clear_full_supabase_auth() -> None:
    """Cierra sesión en memoria y borra la cookie de refresh."""
    for k in (
        "supabase_access_token",
        "supabase_user_id",
        "supabase_email",
        "nav_main",
        "nav_department",
        "admin_open_edit_uid",
        "admin_open_delete_uid",
    ):
        st.session_state.pop(k, None)
    clear_supabase_refresh_cookie()
