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
    if not url or not anon_key:
        raise ValueError(
            "Faltan credenciales de Supabase en `.streamlit/secrets.toml`: "
            "asegúrate de definir [supabase].url y [supabase].anon_key."
        )
    return {"url": str(url), "anon_key": str(anon_key)}


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

