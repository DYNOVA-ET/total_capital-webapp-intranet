"""Interfaz del módulo de Administración."""

import io
import re
import streamlit as st
import pandas as pd
from modules.admin import admin_logic
from config.email_sender import is_email_configured, send_email_with_attachment

# Bancos disponibles
BANCOS = {
    "Banco VE POR MAS": admin_logic.BANCO_VE_POR_MAS,
}


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

    st.title("Administración")
    st.markdown("Procesamiento de estados de cuenta bancarios (CSV).")

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

            try:
                df = pd.read_csv(uploaded_file, encoding="utf-8", header=header_idx)
            except UnicodeDecodeError:
                df = pd.read_csv(uploaded_file, encoding="latin-1", header=header_idx)

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
        st.markdown("---")
        st.subheader("Descargar resultados")
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            for filename, result_df in st.session_state.admin_results.items():
                sheet_name = _sanitize_sheet_name(filename.replace(".csv", ""))
                result_df.to_excel(writer, index=False, sheet_name=sheet_name)
        output.seek(0)
        st.download_button(
            label="Descargar todo (Excel con varias hojas)",
            data=output,
            file_name="estados_cuenta_procesados.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary",
        )
