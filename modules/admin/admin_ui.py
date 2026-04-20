"""Interfaz del módulo de Administración."""

import io
import re
import streamlit as st
import pandas as pd
from modules.admin import admin_logic
from config.email_sender import is_email_configured, send_email_with_attachment
from config.theme import ADMIN_MODULE_CSS

# Mapa: nombre visible en UI → clave interna de banco
BANCOS: dict[str, str] = {
    "Banco VE POR MAS": admin_logic.BANCO_VE_POR_MAS,
}


def validate_csv_upload(file) -> tuple[bool, str]:
    """Validate file before processing."""
    MAX_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_TYPES = {'csv', 'text/csv', 'application/csv'}
    
    if file.size > MAX_SIZE:
        return False, "Archivo > 10MB"
    if file.name.split('.')[-1].lower() != 'csv':
        return False, "Solo archivos CSV permitidos"
    return True, ""


def _read_bank_csv(uploaded_file, header_idx: int) -> pd.DataFrame:
    """Lee CSV delimitado por coma o punto y coma (inferencia + fallback)."""
    def _load(encoding: str, sep: str | None) -> pd.DataFrame:
        uploaded_file.seek(0)
        if sep is None:
            return pd.read_csv(
                uploaded_file,
                encoding=encoding,
                header=header_idx,
                sep=None,
                engine="python",
            )
        return pd.read_csv(uploaded_file, encoding=encoding, header=header_idx, sep=sep)

    def _needs_semicolon_fallback(df: pd.DataFrame) -> bool:
        if df.shape[1] != 1:
            return False
        if ";" in str(df.columns[0]):
            return True
        if len(df) > 0:
            v = df.iat[0, 0]
            if pd.notna(v) and ";" in str(v):
                return True
        return False

    for encoding in ("utf-8", "latin-1"):
        try:
            df = _load(encoding, None)
            if _needs_semicolon_fallback(df):
                df = _load(encoding, ";")
            return df
        except UnicodeDecodeError:
            continue

    raise RuntimeError("No se pudo leer el CSV con utf-8 ni latin-1.")


def _sanitize_sheet_name(name: str, max_len: int = 31) -> str:
    """Nombre de hoja Excel válido (sin caracteres prohibidos)."""
    name = re.sub(r'[\\/*?:\[\]]', '', name)
    return name[:max_len] if len(name) > max_len else name


def render():
    """Renderiza la interfaz del módulo de Administración."""
    if "admin_file_settings" not in st.session_state:
        st.session_state.admin_file_settings = {}
    if "admin_results" not in st.session_state:
        st.session_state.admin_results = {}

    st.markdown(ADMIN_MODULE_CSS, unsafe_allow_html=True)

    st.markdown("""
    <div class="tc-admin-header">
        <div class="tc-admin-header-icon">🏦</div>
        <div class="tc-admin-header-text">
            <h2>Administración</h2>
            <p>Procesamiento de estados de cuenta bancarios (CSV → Excel)</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "Sube uno o varios archivos CSV",
        type=["csv"],
        accept_multiple_files=True,
        help="Cada archivo puede ser de un banco distinto. Configura banco y línea de encabezados por archivo.",
    )

    if not uploaded_files:
        st.info("Sube uno o varios archivos CSV para comenzar.")
        st.session_state.admin_results = {}
        return

    # Inicializar configuración por archivo si no existe
    for f in uploaded_files:
        if f.name not in st.session_state.admin_file_settings:
            st.session_state.admin_file_settings[f.name] = {
                "bank": list(BANCOS.keys())[0],
                "header_row": 10,
            }

    # Validar archivos
    invalid_files = []
    for f in uploaded_files:
        valid, msg = validate_csv_upload(f)
        if not valid:
            invalid_files.append(f"{f.name}: {msg}")
    
    if invalid_files:
        for msg in invalid_files:
            st.error(msg)
        st.stop()

    # Formulario por cada archivo
    for uploaded_file in uploaded_files:
        settings = st.session_state.admin_file_settings[uploaded_file.name]
        with st.expander(f"📄 {uploaded_file.name}", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                bank_options = list(BANCOS.keys())
                bank_index = bank_options.index(settings["bank"]) if settings["bank"] in bank_options else 0
                new_bank = st.selectbox(
                    "Banco",
                    options=bank_options,
                    index=bank_index,
                    key=f"bank_{uploaded_file.name}",
                )
            with col2:
                header_row = st.number_input(
                    "Línea de encabezados",
                    min_value=1,
                    max_value=50,
                    value=settings["header_row"],
                    step=1,
                    key=f"header_{uploaded_file.name}",
                )

            st.session_state.admin_file_settings[uploaded_file.name] = {
                "bank": new_bank,
                "header_row": header_row,
            }

            bank_key = BANCOS[new_bank]
            header_idx = header_row - 1 if bank_key == admin_logic.BANCO_VE_POR_MAS else 0

            df = _read_bank_csv(uploaded_file, header_idx)

            st.dataframe(df.head(10), use_container_width=True, height=200)

            if st.button("Procesar", key=f"process_{uploaded_file.name}", type="primary"):
                with st.spinner(f"Procesando {uploaded_file.name}..."):
                    try:
                        result_df = admin_logic.process_bank_csv(df, bank_key)
                        st.session_state.admin_results[uploaded_file.name] = result_df
                        st.success(f"✓ {uploaded_file.name} procesado")
                    except Exception as e:
                        st.error(f"Error: {e}")
                        if uploaded_file.name in st.session_state.admin_results:
                            del st.session_state.admin_results[uploaded_file.name]

            if uploaded_file.name in st.session_state.admin_results:
                result_df = st.session_state.admin_results[uploaded_file.name]
                st.dataframe(result_df, use_container_width=True, height=150)

    # Descarga combinada si hay resultados
    if st.session_state.admin_results:
        n = len(st.session_state.admin_results)
        st.markdown(f"""
        <div class="tc-download-section">
            <span class="tc-result-badge">✓ {n} archivo{"s" if n != 1 else ""} procesado{"s" if n != 1 else ""}</span>
            <h3>Descargar resultados</h3>
        </div>
        """, unsafe_allow_html=True)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            for filename, result_df in st.session_state.admin_results.items():
                sheet_name = _sanitize_sheet_name(filename.replace(".csv", ""))
                result_df.to_excel(writer, index=False, sheet_name=sheet_name)
        output.seek(0)
        st.download_button(
            label="⬇ Descargar todo (Excel con varias hojas)",
            data=output,
            file_name="estados_cuenta_procesados.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary",
        )
