"""Supabase Auth helpers (login/register).

Este módulo se usa desde Streamlit. Lee credenciales desde `st.secrets`.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from urllib.parse import urlencode
from typing import Any


def _get_supabase_secrets() -> dict[str, str]:
    import streamlit as st

    try:
        secrets = st.secrets["supabase"]  # type: ignore[index]
    except Exception:
        secrets = {}
    url = secrets.get("url")
    anon_key = secrets.get("anon_key")
    service_role_key = secrets.get("service_role_key")
    if not url or not anon_key:
        raise ValueError(
            "Faltan credenciales de Supabase en `.streamlit/secrets.toml`: "
            "asegúrate de definir [supabase].url y [supabase].anon_key."
        )
    return {
        "url": str(url),
        "anon_key": str(anon_key),
        "service_role_key": str(service_role_key) if service_role_key else "",
    }


def _supabase_request_json(
    *,
    method: str,
    endpoint: str,
    anon_key: str,
    access_token: str | None = None,
    query_params: dict[str, str] | None = None,
    payload: dict[str, Any] | None = None,
) -> Any:
    url = endpoint
    if query_params:
        url = f"{url}?{urlencode(query_params, doseq=True)}"

    headers: dict[str, str] = {
        "apikey": anon_key,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"

    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(url, method=method, headers=headers, data=data)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = resp.read().decode("utf-8") if resp is not None else ""
            return json.loads(body) if body else None
    except urllib.error.HTTPError as e:
        raw = ""
        try:
            raw = e.read().decode("utf-8")  # type: ignore[union-attr]
        except Exception:
            raw = ""
        try:
            err = json.loads(raw) if raw else {}
        except Exception:
            err = {}
        if isinstance(err, dict):
            raise RuntimeError(
                err.get("error_description")
                or err.get("msg")
                or err.get("message")
                or err.get("error")
                or raw
                or str(e)
            ) from e
        raise RuntimeError(raw or str(e)) from e


def supabase_sign_up(email: str, password: str, user_metadata: dict[str, Any]) -> tuple[bool, str]:
    """Crea un usuario en Supabase y dispara el correo de confirmación (si está habilitado).

    Retorna: (ok, mensaje).
    """

    cfg = _get_supabase_secrets()
    endpoint = f"{cfg['url'].rstrip('/')}/auth/v1/signup"

    payload: dict[str, Any] = {
        "email": email,
        "password": password,
        # GoTrue guarda esto en `raw_user_meta_data`
        "data": user_metadata,
    }

    req = urllib.request.Request(
        endpoint,
        method="POST",
        headers={
            "apikey": cfg["anon_key"],
            "Content-Type": "application/json",
        },
        data=json.dumps(payload).encode("utf-8"),
    )

    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = resp.read().decode("utf-8") if resp is not None else ""
            data = json.loads(body) if body else {}

        # En muchos casos no habrá session si requiere confirmación.
        if isinstance(data, dict) and data.get("message"):
            return True, str(data["message"])
        return True, "Registro creado. Revisa tu correo para confirmar tu cuenta."

    except urllib.error.HTTPError as e:
        raw = ""
        try:
            raw = e.read().decode("utf-8")  # type: ignore[union-attr]
        except Exception:
            raw = ""
        try:
            err = json.loads(raw) if raw else {}
        except Exception:
            err = {}

        # Estructuras típicas: { error: "...", error_description: "..."} o {msg: "..."}
        if isinstance(err, dict):
            msg = err.get("error_description") or err.get("msg") or err.get("error") or raw or str(e)
        else:
            msg = raw or str(e)
        return False, f"Error al registrar en Supabase: {msg}"


def supabase_sign_in(email: str, password: str) -> tuple[bool, dict[str, Any] | str]:
    """Autentica contra Supabase Auth (GoTrue) usando Email/Password.

    Devuelve (ok, data) donde data contiene típicamente `access_token`, `refresh_token`, y `user`.
    """
    cfg = _get_supabase_secrets()
    endpoint = f"{cfg['url'].rstrip('/')}/auth/v1/token"

    try:
        data = _supabase_request_json(
            method="POST",
            endpoint=endpoint,
            anon_key=cfg["anon_key"],
            query_params={"grant_type": "password"},
            payload={"email": email, "password": password},
        )
        if not isinstance(data, dict):
            return False, "Respuesta inesperada de Supabase."
        if "access_token" not in data:
            # GoTrue suele devolver {error, error_description} en HTTPError; si llega aquí, es raro.
            return False, str(data)
        return True, data
    except Exception as e:
        return False, str(e)


def supabase_refresh_session(refresh_token: str) -> tuple[bool, dict[str, Any] | str]:
    """Obtiene un nuevo access_token (y opcionalmente refresh_token) con el refresh_token de GoTrue."""
    cfg = _get_supabase_secrets()
    endpoint = f"{cfg['url'].rstrip('/')}/auth/v1/token"
    rt = (refresh_token or "").strip()
    if not rt:
        return False, "refresh_token vacío."

    try:
        data = _supabase_request_json(
            method="POST",
            endpoint=endpoint,
            anon_key=cfg["anon_key"],
            query_params={"grant_type": "refresh_token"},
            payload={"refresh_token": rt},
        )
        if not isinstance(data, dict):
            return False, "Respuesta inesperada de Supabase."
        if "access_token" not in data:
            return False, str(data.get("error_description") or data.get("msg") or data)
        return True, data
    except Exception as e:
        return False, str(e)


def supabase_rest_select(
    *,
    table_or_view: str,
    access_token: str,
    query_params: dict[str, str],
) -> tuple[bool, list[dict[str, Any]] | str]:
    """Hace un SELECT genérico contra PostgREST respetando RLS."""
    cfg = _get_supabase_secrets()
    endpoint = f"{cfg['url'].rstrip('/')}/rest/v1/{table_or_view.lstrip('/')}"

    try:
        data = _supabase_request_json(
            method="GET",
            endpoint=endpoint,
            anon_key=cfg["anon_key"],
            access_token=access_token,
            query_params=query_params,
        )
        if data is None:
            return True, []
        if isinstance(data, list):
            return True, data
        # A veces PostgREST devuelve dict con error; tratamos como error legible.
        return False, str(data)
    except Exception as e:
        return False, str(e)


def supabase_rest_patch(
    *,
    table_or_view: str,
    access_token: str,
    query_params: dict[str, str],
    payload: dict[str, Any],
) -> tuple[bool, Any | str]:
    """PATCH genérico contra PostgREST respetando RLS."""
    cfg = _get_supabase_secrets()
    endpoint = f"{cfg['url'].rstrip('/')}/rest/v1/{table_or_view.lstrip('/')}"

    try:
        data = _supabase_request_json(
            method="PATCH",
            endpoint=endpoint,
            anon_key=cfg["anon_key"],
            access_token=access_token,
            query_params=query_params,
            payload=payload,
        )
        return True, data
    except Exception as e:
        return False, str(e)


def supabase_rest_post(
    *,
    table_or_view: str,
    access_token: str,
    query_params: dict[str, str] | None,
    payload: list[dict[str, Any]],
    prefer_merge_duplicates: bool = True,
) -> tuple[bool, Any | str]:
    """POST/Upsert genérico contra PostgREST (recomendado con Prefer resolution=merge-duplicates)."""
    cfg = _get_supabase_secrets()
    endpoint = f"{cfg['url'].rstrip('/')}/rest/v1/{table_or_view.lstrip('/')}"

    headers_extra: dict[str, str] = {}
    if prefer_merge_duplicates:
        # Compatibilidad con PostgREST: evita duplicados si existe la PK.
        headers_extra["Prefer"] = "resolution=merge-duplicates"

    # Reutilizamos el request helper pero sin soporte de headers extra; implementamos mínimo aquí.
    url = endpoint
    if query_params:
        url = f"{url}?{urlencode(query_params, doseq=True)}"

    req_headers: dict[str, str] = {
        "apikey": cfg["anon_key"],
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    req_headers.update(headers_extra)
    if access_token:
        req_headers["Authorization"] = f"Bearer {access_token}"

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, method="POST", headers=req_headers, data=data)

    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = resp.read().decode("utf-8") if resp is not None else ""
            return True, json.loads(body) if body else None
    except urllib.error.HTTPError as e:
        raw = ""
        try:
            raw = e.read().decode("utf-8")  # type: ignore[union-attr]
        except Exception:
            raw = ""
        try:
            err = json.loads(raw) if raw else {}
        except Exception:
            err = {}
        if isinstance(err, dict):
            msg = err.get("error_description") or err.get("msg") or err.get("error") or raw or str(e)
        else:
            msg = raw or str(e)
        return False, msg
    except Exception as e:
        return False, str(e)


def supabase_rest_delete(
    *,
    table_or_view: str,
    access_token: str,
    query_params: dict[str, str],
) -> tuple[bool, Any | str]:
    """DELETE genérico contra PostgREST respetando RLS."""
    cfg = _get_supabase_secrets()
    endpoint = f"{cfg['url'].rstrip('/')}/rest/v1/{table_or_view.lstrip('/')}"

    try:
        data = _supabase_request_json(
            method="DELETE",
            endpoint=endpoint,
            anon_key=cfg["anon_key"],
            access_token=access_token,
            query_params=query_params,
            payload=None,
        )
        return True, data
    except Exception as e:
        return False, str(e)


def supabase_admin_create_user(
    *,
    email: str,
    password: str,
    full_name: str,
    role_name: str,
    departments: list[str],
    email_confirm: bool = True,
) -> tuple[bool, Any | str]:
    """Crea un usuario en Supabase Auth usando service_role_key (solo backend).

    Espera que tu trigger use `raw_user_meta_data.role` y `raw_user_meta_data.departments`.
    """
    cfg = _get_supabase_secrets()
    if not cfg.get("service_role_key"):
        return False, "Falta [supabase].service_role_key en `.streamlit/secrets.toml`."

    endpoint = f"{cfg['url'].rstrip('/')}/auth/v1/admin/users"

    email = (email or "").strip().lower()
    if not email:
        return False, "Email requerido."
    if not password:
        return False, "Contraseña requerida."

    username = email.split("@", 1)[0].strip().lower() or email

    payload = {
        "email": email,
        "password": password,
        # No manda correo de confirmación si está soportado por tu configuración.
        "email_confirm": email_confirm,
        "user_metadata": {
            "username": username,
            "name": (full_name or "").strip() or username,
            "role": role_name,
            "departments": departments,
        },
    }

    try:
        data = _supabase_request_json(
            method="POST",
            endpoint=endpoint,
            anon_key=cfg["service_role_key"],  # apikey header
            access_token=cfg["service_role_key"],  # Authorization bearer
            payload=payload,
        )
        return True, data
    except Exception as e:
        return False, str(e)


def supabase_admin_update_user_password(
    *,
    user_id: str,
    new_password: str,
    email_confirm: bool | None = None,
) -> tuple[bool, Any | str]:
    """Actualiza la contraseña de un usuario en Supabase Auth (GoTrue) usando service_role_key.

    Requiere que el usuario tenga autenticación por email/password.
    """
    cfg = _get_supabase_secrets()
    if not cfg.get("service_role_key"):
        return False, "Falta [supabase].service_role_key en `.streamlit/secrets.toml`."
    if not user_id:
        return False, "user_id requerido."
    if not new_password:
        return False, "new_password requerido."

    uid = str(user_id).strip()
    # Hosted Supabase usa plural: /admin/users/{id} (el singular /admin/user/ devuelve 404).
    endpoint = f"{cfg['url'].rstrip('/')}/auth/v1/admin/users/{uid}"
    payload: dict[str, Any] = {"password": new_password}
    if email_confirm is not None:
        payload["email_confirm"] = email_confirm

    try:
        data = _supabase_request_json(
            method="PUT",
            endpoint=endpoint,
            anon_key=cfg["anon_key"],
            access_token=cfg["service_role_key"],
            query_params=None,
            payload=payload,
        )
        return True, data
    except Exception as e:
        return False, str(e)


def supabase_admin_delete_user(*, user_id: str) -> tuple[bool, Any | str]:
    """Elimina un usuario en Supabase Auth (GoTrue) con service_role_key."""
    cfg = _get_supabase_secrets()
    if not cfg.get("service_role_key"):
        return False, "Falta [supabase].service_role_key en `.streamlit/secrets.toml`."
    uid = str(user_id).strip()
    if not uid:
        return False, "user_id requerido."

    endpoint = f"{cfg['url'].rstrip('/')}/auth/v1/admin/users/{uid}"
    try:
        _supabase_request_json(
            method="DELETE",
            endpoint=endpoint,
            anon_key=cfg["service_role_key"],
            access_token=cfg["service_role_key"],
            query_params=None,
            payload=None,
        )
        return True, None
    except Exception as e:
        return False, str(e)

