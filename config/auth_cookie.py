"""Persistencia de sesión Supabase en cookie (refresh_token) para sobrevivir a F5 / recarga."""

from __future__ import annotations

import base64
import json
from datetime import datetime, timedelta

import streamlit as st

from config.supabase_auth import supabase_refresh_session

# Nombre de cookie estable (versión en el nombre por si cambias el formato)
COOKIE_NAME = "tc_intra_sb_rt_v1"
_MAX_AGE_SEC = 60 * 60 * 24 * 30  # 30 días
_HYDRATION_RERUNS = 2  # CookieManager suele devolver {} hasta 1–2 reruns tras F5


def _user_id_from_jwt(access_token: str) -> str | None:
    """Extrae `sub` del JWT si la respuesta de refresh no trae `user`."""
    try:
        parts = access_token.split(".")
        if len(parts) < 2:
            return None
        payload = parts[1] + "=" * (4 - len(parts[1]) % 4)
        data = json.loads(base64.urlsafe_b64decode(payload.encode("ascii")))
        sub = data.get("sub")
        return str(sub) if sub else None
    except Exception:
        return None


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
    # La librería pone expires a +1 día si no pasas expires_at; forzamos 30 días.
    expires = datetime.now() + timedelta(days=30)
    cm.set(
        COOKIE_NAME,
        refresh_token,
        key=_next_cookie_op_key("tc_rt_set"),
        max_age=_MAX_AGE_SEC,
        expires_at=expires,
        path="/",
        same_site="lax",
        secure=True,  # Solo HTTPS
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
        st.session_state.pop("_tc_ck_hydration_pass", None)
        return

    cm = _get_cookie_manager()
    bag = cm.get_all()
    if not isinstance(bag, dict):
        bag = {}
    rt = bag.get(COOKIE_NAME) or cm.get(COOKIE_NAME)

    if not rt:
        # Tras F5 el iframe de cookies a menudo devuelve {} hasta uno o más reruns.
        n = int(st.session_state.get("_tc_ck_hydration_pass", 0))
        if n < _HYDRATION_RERUNS:
            st.session_state["_tc_ck_hydration_pass"] = n + 1
            st.rerun()
        return

    st.session_state.pop("_tc_ck_hydration_pass", None)

    ok, data = supabase_refresh_session(str(rt))
    if not ok or not isinstance(data, dict):
        clear_supabase_refresh_cookie()
        return

    access = data.get("access_token")
    user_obj = data.get("user") if isinstance(data.get("user"), dict) else {}
    uid = user_obj.get("id") or (access and _user_id_from_jwt(str(access)))
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
        "_tc_ck_hydration_pass",
        "_tc_cookie_manager",
    ):
        st.session_state.pop(k, None)
    clear_supabase_refresh_cookie()
