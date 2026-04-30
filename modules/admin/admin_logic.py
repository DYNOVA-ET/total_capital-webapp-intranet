"""Lógica de procesamiento para el módulo de Administración."""

import re
import pandas as pd

# Constantes por banco
BANCO_VE_POR_MAS = "ve_por_mas"
BANCO_VE_POR_MAS_HEADER_ROW = 9  # Los nombres de columnas están en la línea 10 (índice 9)

#diccionario con id y tags
tags = {
    "00000368682":"DGE USD",
    "00000712825":"DGE MXN",
    "00000469012":"BSI USD",
    "00000712804":"BSI MXN",
    "00000391197":"DGP USD",
    "00000712791":"DGP MXN",
    "00000642340":"SVC USD",
    "00000712833":"SVC MXN",
    "25600585353":"BSI MXN SC",
    "25601044520":"BSI MXN SC 2",
    "95600019492":"BSI USD SC",
    "95600993391":"BSI USD SC 2",
    "0124988817" : "DGP BBVA"

}


def _monto_salida_positivo(val):
    """Retiros como valor positivo: numérico con abs; texto sin '-' inicial."""
    if pd.isna(val):
        return pd.NA
    num = pd.to_numeric(val, errors="coerce")
    if pd.notna(num):
        return abs(float(num))
    s = str(val).strip()
    while s.startswith("-"):
        s = s[1:].lstrip()
    return s if s else pd.NA


def process_ve_por_mas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Procesa CSV del Banco VE POR MAS.
    - Headers en fila 10
    - Output: Fecha, Entrada, Salida, Concepto (Concepto extraído de DESCRIPCIÓN).
    """
    if df.empty:
        return pd.DataFrame(columns=["Fecha", "Entrada", "Salida", "Concepto"])

    # Detectar columna FECHA (mismo nombre en el CSV)
    fecha_col = None
    for col in df.columns:
        if str(col).strip().upper() == "FECHA":
            fecha_col = col
            break
    if fecha_col is None:
        raise ValueError("No se encontró la columna FECHA en el CSV.")

    # Detectar columna DESCRIPCIÓN
    desc_col = None
    for col in df.columns:
        if "descripci" in str(col).lower() or "descripcion" in str(col).lower():
            desc_col = col
            break
    if desc_col is None:
        raise ValueError("No se encontró la columna DESCRIPCIÓN en el CSV.")

    #detectar las columnas de retiros y depositos    
    retiros_col = None
    deposito_col = None
    for col in df.columns:
        col_lowe = str(col).lower()
        if "retiros" in col_lowe:
            retiros_col = col
        if "depósitos" in col_lowe:
            deposito_col = col
    if retiros_col is None or deposito_col is None:  #validación en caso de que no se encuentren las columnas 
        raise ValueError("No se encontraron las columnas RETIROS o DEPOSITOS en el CSV.")

    # Extraer CONCEPTO: texto después de "CONCEPTO:" hasta el siguiente " PALABRA:" o " PALABRA PALABRA:"
    # Ej: "CONCEPTO: IMPACTA REFERENCIA: 1 BENEFICIARIO: ..." -> solo "IMPACTA"
    # Split por el patrón " PALABRA:" (espacio + palabra + dos puntos)
    _FIELD_PATTERN = re.compile(r"\s+[A-Za-z0-9_]+(?:\s+[A-Za-z0-9_]+)*\s*:")

    def extract_concepto(text):
        if pd.isna(text):
            return ""
        text = str(text).strip()
        idx = text.upper().find("CONCEPTO:") #buscamos la palabra concepto

        if idx >= 0:  #si encontro "CONCEPTO:"
            after = text[idx + 9 :].strip()
            parts = _FIELD_PATTERN.split(after)
            clean_text = parts[0].strip() if parts else after
            
            palabras = clean_text.split()
            if palabras:
                ultimo_pedazo = palabras[-1]  #como el id siempre esta al final lo sacamos y lo guardamos para buscarlo en diccionario
                
                #verificamops si la ultima palabra es un id dentro del diccionario
                if ultimo_pedazo in tags:
                    tag_correspondiente = tags[ultimo_pedazo]
                    texto_sin_codigo = clean_text.replace("CODIGO", "").replace("CLIENTE", "") #borramos "CODIGO" y "CLIENTE"
                    texto_final = texto_sin_codigo.replace(ultimo_pedazo, tag_correspondiente)
                    return " ".join(texto_final.split())
        
            return clean_text

        #se busca sobre el texto, tenga o no "CONCEPTO"
        #si no encontro concepto busca traspaso o recepcion
        idx_traspaso = text.upper().find("TRASPASO")
        idx_recepcion = text.upper().find("RECEPCION")

        if idx_traspaso >= 0 or idx_recepcion >= 0:  
            #si alguna de las dos existe buscamos recepcion primero por que en las 
            #de recepcion tambien se encuentra la palabra traspaso
            if idx_recepcion >= 0: 
                operacion = "RECEPCION"
            else:
                operacion = "TRASPASO"

            parts = text.split()  
            id_banco = parts[-1]

            tag_final = tags.get(id_banco, id_banco)
            return f"{operacion} {tag_final}"  #regresamos la operacion con el tag 
        return text

    def _pick_entrada(row: pd.Series):
        v = row[deposito_col]
        if pd.notna(v) and str(v).strip() != "":
            return v
        return pd.NA

    def _pick_salida(row: pd.Series):
        v = row[retiros_col]
        if pd.notna(v) and str(v).strip() != "":
            return _monto_salida_positivo(v)
        return pd.NA

    result = pd.DataFrame(
        {
            "Fecha": df[fecha_col],
            "Entrada": df.apply(_pick_entrada, axis=1),
            "Salida": df.apply(_pick_salida, axis=1),
            "Concepto": df[desc_col].apply(extract_concepto),
        }
    )
    result = result[["Fecha", "Entrada", "Salida", "Concepto"]]

    # Quitar filas vacías
    result = result.dropna(subset=["Fecha"], how="all")
    result = result.replace(r"^\s*$", pd.NA, regex=True)
    result = result.dropna(how="all")

    return result


def process_bank_csv(df: pd.DataFrame, bank: str) -> pd.DataFrame:
    """
    Procesa CSV según el banco seleccionado.
    """
    if bank == BANCO_VE_POR_MAS:
        return process_ve_por_mas(df)
    raise ValueError(f"Banco no soportado: {bank}")
