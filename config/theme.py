"""Colores corporativos y constantes para Total Capital."""


# CSS personalizado para la aplicación
CUSTOM_CSS = """
<style>
    /* Importación de fuentes (Montserrat para títulos, Poppins para texto) */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&family=Poppins:wght@300;400;500&display=swap');

    /* ── Keyframes globales ── */
    @keyframes sidebarContentIn {
        from { opacity: 0; transform: translateX(-14px); }
        to   { opacity: 1; transform: translateX(0); }
    }
    @keyframes navRowIn {
        from { opacity: 0; transform: translateX(-10px); }
        to   { opacity: 1; transform: translateX(0); }
    }
    @keyframes logoBounceIn {
        from { opacity: 0; transform: scale(0.85); }
        to   { opacity: 1; transform: scale(1); }
    }
    @media (prefers-reduced-motion: reduce) {
        * { animation: none !important; transition: none !important; }
    }

    body {
    font-family: 'Poppins', sans-serif;
    }
    section.main > div {
    background-color: white;
    padding: 2.5rem;
    border-radius: 16px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.05);
    margin-top: 1.5rem;
    }
    [data-testid="stAppViewContainer"] {
    background-color: #ffffff !important;
    }
    
    /* Botones globales */
    .stButton > button {
        border-radius: 8px !important;
        background-color: #4e5d77 !important;
        color: white !important;
        border: none !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 500 !important;
        font-family: 'Poppins', sans-serif !important;
        transition:
            transform 0.28s cubic-bezier(0.34, 1.56, 0.64, 1),
            box-shadow 0.25s ease,
            background-color 0.2s ease,
            color 0.2s ease !important;
    }
    .stButton > button:hover {
        background-color: #7ed957 !important;
        color: #003a40 !important;
        border: none !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 20px rgba(0, 58, 64, 0.22) !important;
    }
    .stButton > button:active {
        transform: translateY(-1px) !important;
        box-shadow: 0 3px 8px rgba(0, 58, 64, 0.15) !important;
    }
    /* ── Sidebar: base ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f4f4f5 0%, #efefef 100%) !important;
        border-right: 1px solid #e4e4e7 !important;
        padding-top: 0.75rem !important;
        color: #3f3f46 !important;
    }
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 0.25rem !important;
    }

    /* Contenido del sidebar: entra desde la izquierda al cargar */
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        animation: sidebarContentIn 0.45s cubic-bezier(0.22, 1, 0.36, 1) both;
    }

    /* Logo: bounce suave de entrada */
    [data-testid="stSidebar"] [data-testid="stImage"],
    [data-testid="stSidebar"] .element-container:has(img) {
        margin-bottom: 0.35rem !important;
        margin-top: 0 !important;
        animation: logoBounceIn 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) both;
    }
    [data-testid="stSidebar"] [data-testid="stImage"] img {
        transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    }
    [data-testid="stSidebar"] [data-testid="stImage"] img:hover {
        transform: scale(1.04) !important;
    }

    /* Textos del sidebar */
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] small,
    [data-testid="stSidebar"] .stMarkdown {
        color: #52525b !important;
    }
    [data-testid="stSidebar"] .tc-sidebar-brand-title {
        color: #18181b !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        margin: 0 !important;
    }
    [data-testid="stSidebar"] .tc-sidebar-section-label {
        color: #a1a1aa !important;
        font-size: 0.7rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.06em !important;
        text-transform: uppercase !important;
        margin: 1rem 0 0.4rem 0 !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: #e4e4e7 !important;
        background-color: #e4e4e7 !important;
        opacity: 1 !important;
        margin: 0.75rem 0 !important;
    }

    /* ── Nav rows: layout + stagger de entrada ── */
    [data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        align-items: stretch !important;
        gap: 0.2rem !important;
        margin-bottom: 0.08rem !important;
        border-radius: 8px !important;
        animation: navRowIn 0.4s cubic-bezier(0.22, 1, 0.36, 1) both;
    }
    [data-testid="stSidebar"] div[data-testid="stHorizontalBlock"]:nth-child(1) { animation-delay: 0.04s; }
    [data-testid="stSidebar"] div[data-testid="stHorizontalBlock"]:nth-child(2) { animation-delay: 0.08s; }
    [data-testid="stSidebar"] div[data-testid="stHorizontalBlock"]:nth-child(3) { animation-delay: 0.12s; }
    [data-testid="stSidebar"] div[data-testid="stHorizontalBlock"]:nth-child(4) { animation-delay: 0.16s; }
    [data-testid="stSidebar"] div[data-testid="stHorizontalBlock"]:nth-child(5) { animation-delay: 0.20s; }
    [data-testid="stSidebar"] div[data-testid="stHorizontalBlock"]:nth-child(6) { animation-delay: 0.24s; }
    [data-testid="stSidebar"] div[data-testid="stHorizontalBlock"]:nth-child(7) { animation-delay: 0.28s; }

    /* Columnas dentro de cada fila */
    [data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:first-child {
        flex: 0 0 1.75rem !important;
        width: 1.75rem !important;
        min-width: 1.75rem !important;
        max-width: 1.75rem !important;
    }
    [data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:last-child {
        flex: 1 1 auto !important;
        min-width: 0 !important;
    }
    [data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] div[data-testid="element-container"] {
        padding-left: 0 !important;
        padding-right: 0 !important;
    }

    /* Celda de icono */
    [data-testid="stSidebar"] .tc-nav-icon-cell {
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        min-height: 2.25rem !important;
        padding-left: 0.15rem !important;
        transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    }
    [data-testid="stSidebar"] .tc-nav-icon-cell img {
        display: block !important;
        width: 1.25rem !important;
        height: 1.25rem !important;
        object-fit: contain !important;
        transition: opacity 0.2s ease !important;
    }

    /* ── Botones de nav: base ── */
    [data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] .stButton {
        width: 100% !important;
    }
    [data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] .stButton > button {
        display: flex !important;
        justify-content: flex-start !important;
        align-items: center !important;
        width: 100% !important;
        text-align: left !important;
        background-color: transparent !important;
        color: #27272a !important;
        border: none !important;
        border-radius: 8px !important;
        border-left: 3px solid transparent !important;
        box-shadow: none !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        padding: 0.45rem 0.5rem 0.45rem 0.35rem !important;
        min-height: 2.25rem !important;
        box-sizing: border-box !important;
        transition:
            background-color 0.18s ease,
            color 0.18s ease,
            transform 0.22s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    }

    /* Hover: slide leve a la derecha */
    [data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] .stButton > button:hover {
        background-color: #e8e8ea !important;
        color: #003a40 !important;
        border: none !important;
        border-left: 3px solid #b0b8c1 !important;
        transform: translateX(3px) !important;
        box-shadow: none !important;
    }

    /* ── Ítem activo ── */
    [data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] .stButton > button[data-testid="baseButton-primary"],
    [data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] .stButton > button[data-testid="stBaseButton-primary"] {
        background-color: transparent !important;
        color: #003a40 !important;
        border: none !important;
        border-left: 3px solid transparent !important;
        font-weight: 600 !important;
    }
    [data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] .stButton > button[data-testid="baseButton-primary"]:hover,
    [data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] .stButton > button[data-testid="stBaseButton-primary"]:hover {
        background-color: transparent !important;
        color: #003a40 !important;
        border-left: 3px solid transparent !important;
        transform: translateX(2px) !important;
    }

    /* Fila activa completa: fondo pill + barra verde lima */
    [data-testid="stSidebar"] div[data-testid="stHorizontalBlock"]:has(.stButton > button[data-testid="baseButton-primary"]),
    [data-testid="stSidebar"] div[data-testid="stHorizontalBlock"]:has(.stButton > button[data-testid="stBaseButton-primary"]) {
        background: linear-gradient(90deg, rgba(0,58,64,0.08) 0%, rgba(0,58,64,0.04) 100%) !important;
        border-radius: 8px !important;
        border-left: 3px solid #7ed957 !important;
        box-sizing: border-box !important;
    }
    [data-testid="stSidebar"] div[data-testid="stHorizontalBlock"]:has(.stButton > button[data-testid="baseButton-primary"]):hover,
    [data-testid="stSidebar"] div[data-testid="stHorizontalBlock"]:has(.stButton > button[data-testid="stBaseButton-primary"]):hover {
        background: linear-gradient(90deg, rgba(0,58,64,0.12) 0%, rgba(0,58,64,0.06) 100%) !important;
    }
    [data-testid="stSidebar"] div[data-testid="stHorizontalBlock"]:has(.stButton > button[data-testid="baseButton-primary"]) .stButton > button,
    [data-testid="stSidebar"] div[data-testid="stHorizontalBlock"]:has(.stButton > button[data-testid="stBaseButton-primary"]) .stButton > button {
        background-color: transparent !important;
        border-left-color: transparent !important;
    }
    [data-testid="stSidebar"] div[data-testid="stHorizontalBlock"]:has(.stButton > button[data-testid="baseButton-primary"]) .stButton > button:hover,
    [data-testid="stSidebar"] div[data-testid="stHorizontalBlock"]:has(.stButton > button[data-testid="stBaseButton-primary"]) .stButton > button:hover {
        background-color: transparent !important;
        border-left-color: transparent !important;
    }
    /* Icono de fila activa: más saturado */
    [data-testid="stSidebar"] div[data-testid="stHorizontalBlock"]:has(.stButton > button[data-testid="baseButton-primary"]) .tc-nav-icon-cell img,
    [data-testid="stSidebar"] div[data-testid="stHorizontalBlock"]:has(.stButton > button[data-testid="stBaseButton-primary"]) .tc-nav-icon-cell img {
        opacity: 1 !important;
        filter: brightness(0) saturate(100%) invert(16%) sepia(60%) saturate(700%) hue-rotate(155deg) !important;
    }

    [data-testid="stSidebar"] .stSelectbox div {
        color: #27272a !important;
    }
    
    /* Títulos usando Montserrat y color Primario */
    h1, h2, h3 {
        color: #003a40 !important; /* Color Primario */
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700 !important;
    }

    /* Opcional: Si usas métricas o textos de éxito, usa el verde (#7ed957) */
    [data-testid="stMetricValue"] {
        color: #7ed957 !important;
    }


</style>
"""

# CSS específico del módulo de Administración
ADMIN_MODULE_CSS = """
<style>
    /* ── Animaciones del módulo ── */
    @keyframes adminFadeUp {
        from { opacity: 0; transform: translateY(14px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes adminScaleIn {
        from { opacity: 0; transform: scale(0.97); }
        to   { opacity: 1; transform: scale(1); }
    }

    /* ── Header del módulo ── */
    .tc-admin-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 1.25rem 1.5rem;
        background: linear-gradient(135deg, #003a40 0%, #004d55 100%);
        border-radius: 12px;
        margin-bottom: 1.5rem;
        animation: adminFadeUp 0.45s cubic-bezier(0.22, 1, 0.36, 1) both;
    }
    .tc-admin-header-icon {
        font-size: 2rem;
        line-height: 1;
    }
    .tc-admin-header-text h2 {
        color: #ffffff !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.3rem !important;
        margin: 0 0 0.2rem 0 !important;
    }
    .tc-admin-header-text p {
        color: rgba(255,255,255,0.7) !important;
        font-family: 'Poppins', sans-serif !important;
        font-size: 0.85rem !important;
        margin: 0 !important;
    }

    /* ── Zona de carga de archivos ── */
    [data-testid="stFileUploader"] {
        border: 2px dashed #d1d5db !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        background: #fafafa !important;
        transition: border-color 0.2s ease, background 0.2s ease !important;
        animation: adminFadeUp 0.5s cubic-bezier(0.22, 1, 0.36, 1) 0.1s both;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #7ed957 !important;
        background: #f6fef2 !important;
    }

    /* ── Cards de archivo (expanders) ── */
    [data-testid="stExpander"] {
        border: 1px solid #e5e7eb !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        box-shadow: 0 2px 8px rgba(0, 58, 64, 0.06) !important;
        margin-bottom: 1rem !important;
        animation: adminScaleIn 0.4s cubic-bezier(0.22, 1, 0.36, 1) both;
        transition: box-shadow 0.25s ease, border-color 0.2s ease !important;
    }
    [data-testid="stExpander"]:hover {
        box-shadow: 0 6px 20px rgba(0, 58, 64, 0.1) !important;
        border-color: #b8d4c8 !important;
    }
    [data-testid="stExpander"] summary {
        background: #f8fafb !important;
        padding: 0.75rem 1rem !important;
        font-family: 'Poppins', sans-serif !important;
        font-weight: 500 !important;
        color: #003a40 !important;
    }

    /* ── Stagger de entrada para múltiples expanders ── */
    [data-testid="stExpander"]:nth-child(1) { animation-delay: 0.05s; }
    [data-testid="stExpander"]:nth-child(2) { animation-delay: 0.10s; }
    [data-testid="stExpander"]:nth-child(3) { animation-delay: 0.15s; }
    [data-testid="stExpander"]:nth-child(4) { animation-delay: 0.20s; }

    /* ── Sección de descarga ── */
    .tc-download-section {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border: 1px solid #86efac;
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        margin-top: 1rem;
        animation: adminFadeUp 0.4s cubic-bezier(0.22, 1, 0.36, 1) both;
    }
    .tc-download-section h3 {
        color: #003a40 !important;
        font-size: 1rem !important;
        margin: 0 0 0.75rem 0 !important;
    }

    /* ── Badge de resultado ── */
    .tc-result-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: #003a40;
        color: #7ed957;
        font-family: 'Poppins', sans-serif;
        font-size: 0.78rem;
        font-weight: 600;
        padding: 0.25rem 0.7rem;
        border-radius: 99px;
        margin-bottom: 0.5rem;
    }

    @media (prefers-reduced-motion: reduce) {
        * { animation: none !important; transition: none !important; }
    }
</style>
"""

# CSS específico de la página de Perfil
PROFILE_PAGE_CSS = """
<style>
    /* ── Animaciones ── */
    @keyframes profileFadeUp {
        from { opacity: 0; transform: translateY(16px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes avatarPop {
        from { opacity: 0; transform: scale(0.8); }
        to   { opacity: 1; transform: scale(1); }
    }

    /* ── Hero card: gradiente en el stHorizontalBlock (columnas del hero) ── */
    .tc-hero-marker { display: none; }
    [data-testid="stHorizontalBlock"]:has(.tc-hero-marker) {
        background: linear-gradient(135deg, #003a40 0%, #004d55 100%) !important;
        border-radius: 16px !important;
        padding: 1.25rem 2rem !important;
        margin-bottom: 1.25rem !important;
        align-items: center !important;
        animation: profileFadeUp 0.45s cubic-bezier(0.22, 1, 0.36, 1) both;
    }

    /* ── Avatar: st.button nativo estilizado como círculo ── */
    [data-testid="stHorizontalBlock"]:has(.tc-hero-marker) [data-testid="stBaseButton-secondary"] {
        border-radius: 50% !important;
        width: 72px !important;
        height: 72px !important;
        min-height: 72px !important;
        background: rgba(126, 217, 87, 0.15) !important;
        border: 2px solid rgba(126, 217, 87, 0.5) !important;
        color: #7ed957 !important;
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        font-family: 'Montserrat', sans-serif !important;
        padding: 0 !important;
        animation: avatarPop 0.55s cubic-bezier(0.34, 1.56, 0.64, 1) 0.1s both !important;
        transition: border-color 0.2s ease, background 0.2s ease,
                    transform 0.2s ease, box-shadow 0.2s ease !important;
    }
    [data-testid="stHorizontalBlock"]:has(.tc-hero-marker) [data-testid="stBaseButton-secondary"]:hover {
        border-color: #7ed957 !important;
        background: rgba(126, 217, 87, 0.28) !important;
        transform: scale(1.06) !important;
        box-shadow: 0 0 0 4px rgba(126, 217, 87, 0.15) !important;
    }

    .tc-profile-name {
        color: #ffffff !important;
        font-family: 'Montserrat', sans-serif !important;
        font-size: 1.35rem !important;
        font-weight: 700 !important;
        margin: 0 0 0.2rem 0 !important;
        line-height: 1.2 !important;
    }
    .tc-profile-email {
        color: rgba(255,255,255,0.65) !important;
        font-family: 'Poppins', sans-serif !important;
        font-size: 0.83rem !important;
        margin: 0 0 0.5rem 0 !important;
    }
    .tc-role-badge {
        display: inline-block;
        background: rgba(126, 217, 87, 0.18);
        color: #7ed957;
        border: 1px solid rgba(126, 217, 87, 0.45);
        border-radius: 99px;
        font-family: 'Poppins', sans-serif;
        font-size: 0.7rem;
        font-weight: 600;
        padding: 0.2rem 0.65rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    /* ── Cards de info ── */
    .tc-profile-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,58,64,0.05);
        animation: profileFadeUp 0.5s cubic-bezier(0.22, 1, 0.36, 1) both;
    }
    .tc-profile-card:nth-child(2) { animation-delay: 0.08s; }
    .tc-profile-card:nth-child(3) { animation-delay: 0.14s; }

    .tc-profile-section-label {
        color: #9ca3af !important;
        font-family: 'Poppins', sans-serif !important;
        font-size: 0.7rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.07em !important;
        text-transform: uppercase !important;
        margin: 0 0 0.6rem 0 !important;
    }

    /* ── Chips de departamento ── */
    .tc-dept-chips {
        display: flex;
        flex-wrap: wrap;
        gap: 0.4rem;
        margin-top: 0.25rem;
    }
    .tc-dept-chip {
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        background: #f0fdf4;
        border: 1px solid #86efac;
        color: #003a40;
        font-family: 'Poppins', sans-serif;
        font-size: 0.82rem;
        font-weight: 500;
        padding: 0.3rem 0.85rem;
        border-radius: 99px;
        transition: background 0.2s ease, border-color 0.2s ease;
    }
    .tc-dept-chip:hover {
        background: #dcfce7;
        border-color: #4ade80;
    }

    /* ── Emoji picker dialog: botones de emoji cuadrados ── */
    [data-testid="stDialog"] [data-testid="stBaseButton-secondary"] {
        font-size: 1.5rem !important;
        min-height: 52px !important;
        padding: 0 !important;
        border-radius: 10px !important;
        border-color: #e5e7eb !important;
        transition: transform 0.15s ease, border-color 0.15s ease, background 0.15s ease !important;
    }
    [data-testid="stDialog"] [data-testid="stBaseButton-secondary"]:hover {
        border-color: #7ed957 !important;
        background: #f0fdf4 !important;
        transform: scale(1.12) !important;
    }
    [data-testid="stDialog"] [data-testid="stBaseButton-primary"] {
        font-size: 1.5rem !important;
        min-height: 52px !important;
        padding: 0 !important;
        border-radius: 10px !important;
        background: rgba(126, 217, 87, 0.15) !important;
        border: 2px solid #7ed957 !important;
        color: #003a40 !important;
        transform: scale(1.06) !important;
    }

    /* ── Sección cambio de contraseña ── */
    .tc-password-section-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.75rem;
    }
    .tc-password-section-header span {
        color: #003a40;
        font-family: 'Montserrat', sans-serif;
        font-weight: 600;
        font-size: 0.95rem;
    }

    @media (prefers-reduced-motion: reduce) {
        * { animation: none !important; transition: none !important; }
    }
</style>
"""

# CSS solo para la página de login (se inyecta solo cuando no hay sesión)
LOGIN_PAGE_CSS = """
<style>
    /* ── Keyframes ── */
    @keyframes loginSlideLeft {
        from { opacity: 0; transform: translateX(-28px); }
        to   { opacity: 1; transform: translateX(0); }
    }
    @keyframes loginSlideRight {
        from { opacity: 0; transform: translateX(28px); }
        to   { opacity: 1; transform: translateX(0); }
    }
    @keyframes loginFadeUp {
        from { opacity: 0; transform: translateY(14px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes logoEntrance {
        from { opacity: 0; transform: scale(0.88); }
        to   { opacity: 1; transform: scale(1); }
    }
    @keyframes shakeError {
        0%, 100% { transform: translateX(0); }
        15%  { transform: translateX(-7px); }
        30%  { transform: translateX(7px); }
        45%  { transform: translateX(-4px); }
        60%  { transform: translateX(4px); }
        75%  { transform: translateX(-2px); }
        90%  { transform: translateX(2px); }
    }
    @keyframes inputFocusBorder {
        from { box-shadow: 0 0 0 0px rgba(126, 217, 87, 0); }
        to   { box-shadow: 0 0 0 3px rgba(126, 217, 87, 0.25); }
    }
    @media (prefers-reduced-motion: reduce) {
        * { animation: none !important; transition: none !important; }
    }

    /* ── Fondo y layout ── */
    [data-testid="stSidebar"] {
        visibility: hidden !important;
    }
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #f0f4f7 0%, #e8edf2 100%) !important;
    }
    section.main > div {
        background: transparent !important;
        box-shadow: none !important;
        padding: 2rem 1.5rem !important;
    }

    /* ── Columna izquierda: formulario (entra desde la izquierda) ── */
    .login-page [data-testid="column"]:first-child {
        animation: loginSlideLeft 0.55s cubic-bezier(0.22, 1, 0.36, 1) both;
    }
    [data-testid="column"]:first-child > div {
        overflow: visible !important;
        min-height: auto !important;
    }

    /* ── Columna derecha: branding (entra desde la derecha, con delay) ── */
    .login-page [data-testid="column"]:last-child {
        animation: loginSlideRight 0.65s cubic-bezier(0.22, 1, 0.36, 1) both;
        animation-delay: 0.08s;
    }
    .login-page [data-testid="column"]:last-child > div {
        background: #0d0d0d !important;
        border-radius: 1.25rem !important;
        padding: 3.5rem 2.5rem 2rem 3.5rem !important;
        min-height: 80vh;
        display: flex !important;
        flex-direction: column !important;
        justify-content: flex-start !important;
        align-items: center !important;
        gap: 0.85rem !important;
        box-sizing: border-box !important;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.18) !important;
    }

    /* ── Branding box ── */
    .login-branding-box {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        text-align: center !important;
        width: 100% !important;
        box-sizing: border-box !important;
        margin-top: 2rem !important;
        margin-left: 1.5rem !important;
        background-color: #ffffff !important;
        padding: 2rem !important;
        border-radius: 1rem !important;
        animation: loginFadeUp 0.7s cubic-bezier(0.22, 1, 0.36, 1) both;
        animation-delay: 0.2s;
    }
    .login-branding-logo {
        width: 520px !important;
        max-width: 100% !important;
        height: auto !important;
        margin-bottom: 0.85rem !important;
        animation: logoEntrance 0.8s cubic-bezier(0.22, 1, 0.36, 1) both;
        animation-delay: 0.3s;
    }
    .login-branding-title,
    .login-branding-box h3 {
        color: #003a40 !important;
        font-family: 'Montserrat', 'Poppins', sans-serif !important;
        font-weight: 700 !important;
        margin: 0 0 0.25rem 0 !important;
    }
    .login-branding-subtitle {
        color: #003a40 !important;
        margin: 0 !important;
        font-size: 0.95rem !important;
    }

    /* ── Inputs: transición suave en focus con glow ── */
    .login-page section.main input,
    [data-testid="stTextInput"] input {
        border-radius: 8px !important;
        border: 1.5px solid #e0e0e0 !important;
        background-color: white !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    }
    .login-page section.main input:focus,
    [data-testid="stTextInput"] input:focus {
        border-color: #7ed957 !important;
        box-shadow: 0 0 0 3px rgba(126, 217, 87, 0.2) !important;
        outline: none !important;
    }

    /* ── Formulario y visibilidad ── */
    [data-testid="stForm"] {
        overflow: visible !important;
    }
    section.main [data-testid="stForm"] .stButton,
    section.main .stButton > button {
        visibility: visible !important;
        display: inline-flex !important;
        opacity: 1 !important;
    }

    /* ── Botón "Ingresar": fondo oscuro + hover elástico ── */
    .login-page .stButton > button,
    section.main [data-testid="stForm"] .stButton > button {
        background-color: #003a40 !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-family: 'Poppins', sans-serif !important;
        width: 100% !important;
        padding: 0.65rem 1.5rem !important;
        transition:
            transform 0.28s cubic-bezier(0.34, 1.56, 0.64, 1),
            box-shadow 0.25s ease,
            background-color 0.2s ease !important;
    }
    .login-page .stButton > button:hover,
    section.main [data-testid="stForm"] .stButton > button:hover {
        background-color: #004d55 !important;
        color: white !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 28px rgba(0, 58, 64, 0.3) !important;
    }
    .login-page .stButton > button:active,
    section.main [data-testid="stForm"] .stButton > button:active {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(0, 58, 64, 0.2) !important;
    }

    /* ── Shake en mensajes de error ── */
    [data-testid="stAlert"][data-baseweb="notification"] {
        animation: shakeError 0.45s cubic-bezier(0.36, 0.07, 0.19, 0.97) both;
    }

    /* ── Título del formulario (subheader) ── */
    .login-page h2, .login-page h3 {
        animation: loginFadeUp 0.5s cubic-bezier(0.22, 1, 0.36, 1) both;
    }

    /* ── Caption inferior ── */
    .login-page small, .login-page .stCaption {
        animation: loginFadeUp 0.6s cubic-bezier(0.22, 1, 0.36, 1) both;
        animation-delay: 0.15s;
    }
</style>
"""