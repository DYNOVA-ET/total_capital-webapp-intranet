"""Iconos SVG (línea fina) para la barra lateral."""

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


def icon_for_department(name: str) -> str:
    """Devuelve el icono SVG apropiado según el nombre del departamento."""
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
