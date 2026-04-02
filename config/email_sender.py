"""Envío de correo con adjuntos (SMTP). Configuración vía variables de entorno."""

import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def _get_smtp_config():
    """Obtiene configuración SMTP desde variables de entorno."""
    host = os.environ.get("SMTP_HOST", "").strip()
    port_str = os.environ.get("SMTP_PORT", "587").strip()
    user = os.environ.get("SMTP_USER", "").strip()
    password = os.environ.get("SMTP_PASSWORD", "").strip()
    from_addr = os.environ.get("EMAIL_FROM", user or "").strip()
    use_tls = os.environ.get("SMTP_USE_TLS", "true").lower() in ("true", "1", "yes")
    try:
        port = int(port_str)
    except ValueError:
        port = 587
    return {
        "host": host,
        "port": port,
        "user": user,
        "password": password,
        "from_addr": from_addr or user,
        "use_tls": use_tls,
    }


def is_email_configured() -> bool:
    """Indica si el envío de correo está configurado (SMTP_HOST y credenciales)."""
    cfg = _get_smtp_config()
    return bool(cfg["host"] and cfg["user"] and cfg["password"])


def send_email_with_attachment(
    to_emails: list[str],
    subject: str,
    body: str,
    attachment_bytes: bytes,
    attachment_filename: str,
) -> tuple[bool, str]:
    """
    Envía un correo con un archivo adjunto.

    Args:
        to_emails: Lista de direcciones de correo destino.
        subject: Asunto del correo.
        body: Cuerpo del mensaje (texto plano).
        attachment_bytes: Contenido binario del adjunto.
        attachment_filename: Nombre del archivo adjunto (ej: reporte.xlsx).

    Returns:
        (éxito, mensaje) — si éxito es False, mensaje describe el error.
    """
    to_emails = [e.strip() for e in to_emails if e and e.strip()]
    if not to_emails:
        return False, "No se indicó ningún correo destino."

    cfg = _get_smtp_config()
    if not cfg["host"] or not cfg["user"] or not cfg["password"]:
        return False, (
            "Envío de correo no configurado. Define las variables de entorno: "
            "SMTP_HOST, SMTP_USER, SMTP_PASSWORD (y opcionalmente SMTP_PORT, EMAIL_FROM, SMTP_USE_TLS)."
        )

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = cfg["from_addr"]
    msg["To"] = ", ".join(to_emails)
    msg.attach(MIMEText(body, "plain", "utf-8"))

    part = MIMEApplication(attachment_bytes, _subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    part.add_header("Content-Disposition", "attachment", filename=attachment_filename)
    msg.attach(part)

    try:
        if cfg["use_tls"]:
            with smtplib.SMTP(cfg["host"], cfg["port"]) as server:
                server.starttls()
                server.login(cfg["user"], cfg["password"])
                server.sendmail(cfg["from_addr"], to_emails, msg.as_string())
        else:
            with smtplib.SMTP(cfg["host"], cfg["port"]) as server:
                server.login(cfg["user"], cfg["password"])
                server.sendmail(cfg["from_addr"], to_emails, msg.as_string())
        return True, f"Correo enviado correctamente a: {', '.join(to_emails)}"
    except smtplib.SMTPAuthenticationError as e:
        return False, f"Error de autenticación SMTP: {e}"
    except smtplib.SMTPException as e:
        return False, f"Error al enviar el correo: {e}"
    except Exception as e:
        return False, f"Error inesperado: {e}"
