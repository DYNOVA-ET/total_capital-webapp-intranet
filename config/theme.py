"""Colores corporativos y constantes para Total Capital."""


# CSS personalizado para la aplicación
CUSTOM_CSS = """
<style>
    /* Importación de fuentes (Montserrat para títulos, Poppins para texto) */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&family=Poppins:wght@300;400;500&display=swap');

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
    
    /* Botones con bordes redondeados y color Primario (#003a40) */
    .stButton > button {
        border-radius: 8px !important;
        background-color: #4e5d77 !important;
        color: white !important;
        border: none !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 500 !important;
        font-family: 'Poppins', sans-serif !important;
        transition: all 0.2s ease !important;
    }
    
    /* Hover del botón con color Secundario (#4e5d77) */
    .stButton > button:hover {
        background-color: #7ed957 !important;
        color: #003a40 !important;
        border: none !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    /* Sidebar clara, estilo intranet minimal */
    [data-testid="stSidebar"] {
    background-color: #f4f4f5 !important;
    border-right: 1px solid #e4e4e7 !important;
    padding-top: 0.75rem !important;
    }
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 0.25rem !important;
    }
    [data-testid="stSidebar"] .element-container:first-of-type,
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div:first-child {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    [data-testid="stSidebar"] [data-testid="stImage"],
    [data-testid="stSidebar"] .element-container:has(img) {
        margin-bottom: 0.35rem !important;
        margin-top: 0 !important;
    }

    [data-testid="stSidebar"] {
    color: #3f3f46 !important;
    }
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

    /* Filas de navegación (icono + botón en columnas): bloques horizontales en la sidebar */
    [data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        align-items: center !important;
        gap: 0.35rem !important;
        margin-bottom: 0.08rem !important;
    }
    [data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:first-child {
        flex: 0 0 2rem !important;
        width: 2rem !important;
        min-width: 2rem !important;
        max-width: 2rem !important;
    }
    [data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] .tc-nav-icon-wrap {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        color: #3f3f46 !important;
    }
    [data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] .tc-nav-icon-wrap svg {
        stroke: #3f3f46 !important;
    }
    [data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] .stButton {
        width: 100% !important;
    }
    [data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] .stButton > button {
        width: 100% !important;
        text-align: left !important;
        justify-content: flex-start !important;
        background-color: transparent !important;
        color: #27272a !important;
        border: none !important;
        border-radius: 8px !important;
        box-shadow: none !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        padding: 0.45rem 0.65rem !important;
        min-height: 2.25rem !important;
    }
    [data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] .stButton > button:hover {
        background-color: #e4e4e7 !important;
        color: #18181b !important;
        border: none !important;
        transform: none !important;
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

# CSS solo para la página de login (se inyecta solo cuando no hay sesión)
LOGIN_PAGE_CSS = """
<style>
    /* Ocultar sidebar en pantalla de login */
    [data-testid="stSidebar"] {
        visibility: hidden !important;
    }

    .login-page [data-testid="stAppViewContainer"] {
        background-color: #f5f5f5 !important;
    }

    /* Panel derecho: fondo oscuro, contenido centrado y desplazado abajo/derecha */
    .login-page [data-testid="column"]:last-child > div {
        background: #0d0d0d !important;
        border-radius: 1rem !important;
        padding: 3.5rem 2.5rem 2rem 3.5rem !important;
        min-height: 80vh;
        display: flex !important;
        flex-direction: column !important;
        justify-content: flex-start !important;
        align-items: center !important;
        gap: 0.85rem !important;
        box-sizing: border-box !important;
    }

    /* Contenedor del logo y texto (mover con margin/padding aquí) */
    .login-branding-box {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        text-align: center !important;
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
        margin-top: 2rem !important;
        margin-left: 1.5rem !important;
        background-color: #ffffff !important;
        padding: 2rem !important;
        border-radius: 1rem !important;
    }
    .login-branding-logo {
        width: 520px !important;
        max-width: 100% !important;
        height: auto !important;
        margin-bottom: 0.85rem !important;
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

    /* Columna izquierda: no recortar contenido (evitar que el botón Login desaparezca) */
    [data-testid="column"]:first-child > div {
        overflow: visible !important;
        min-height: auto !important;
    }

    /* Formulario de login y botón siempre visibles */
    [data-testid="stForm"] {
        overflow: visible !important;
    }
    section.main [data-testid="stForm"] .stButton,
    section.main .stButton > button {
        visibility: visible !important;
        display: inline-flex !important;
        opacity: 1 !important;
    }

    /* Inputs del formulario de login: redondeados, borde gris */
    .login-page section.main input {
        border-radius: 8px !important;
        border: 1px solid #e0e0e0 !important;
        background-color: white !important;
    }

    /* Botón de login: estilo "Sign in" (fondo oscuro) */
    .login-page .stButton > button,
    section.main [data-testid="stForm"] .stButton > button {
        background-color: #0d0d0d !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
    }
    .login-page .stButton > button:hover,
    section.main [data-testid="stForm"] .stButton > button:hover {
        background-color: #003a40 !important;
        color: white !important;
    }

    /* Enlace "¿No tienes cuenta? Regístrate" / "Inicia sesión" con Montserrat */
    .login-register-prompt {
        font-family: 'Montserrat', 'Poppins', sans-serif !important;
        font-weight: 500 !important;
        color: #003a40 !important;
    }
    .login-register-prompt a {
        font-family: 'Montserrat', 'Poppins', sans-serif !important;
        font-weight: 600 !important;
        color: #003a40 !important;
    }
</style>
"""