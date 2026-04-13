def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    Enforce password complexity requirements.
    Returns (is_valid, message)
    """
    checks = {
        "length": len(password) >= 12,
        "upper": any(c.isupper() for c in password),
        "lower": any(c.islower() for c in password),
        "digit": any(c.isdigit() for c in password),
        "special": any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password),
    }
    is_valid = all(checks.values())
    if is_valid:
        message = "✓ Contraseña cumple con los requisitos de seguridad"
    else:
        message = "La contraseña no cumple con los requisitos"
    return is_valid, message, checks


def get_password_checklist(password: str) -> dict[str, bool]:
    """
    Returns a dict with password requirements and their status.
    """
    return {
        "Mínimo 12 caracteres": len(password) >= 12,
        "Al menos una mayúscula": any(c.isupper() for c in password),
        "Al menos una minúscula": any(c.islower() for c in password),
        "Al menos un número": any(c.isdigit() for c in password),
        "Al menos un carácter especial (!@#$%^&* etc.)": any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password),
    }