import streamlit as st
from src.loader import load_file
from src.validators import (
    validate_required_columns, 
    find_duplicate_columns
    )
from src.normalizer import normalize_columns


st.set_page_config(
    page_title="Data Quality Assistant",
    page_icon="🔍",
    layout="wide"
)

st.title("Data Quality Assistant")
st.write("Sube un archivo Excel/CSV para analizar")

uploaded_file = st.file_uploader(
    "Selecciona un archivo",
    type=["xlsx","csv"]
)

if uploaded_file is not None:
    try:
        df = load_file(uploaded_file)
        df = normalize_columns(df)
        duplicate_columns = find_duplicate_columns(df)

        st.success("Archivo cargado correctamente")

        required_columns = ["nombre", "ciudad", "edad"]

        missing_columns  = validate_required_columns(
            df,
            required_columns,
        )

        st.subheader("Validación de columnas")

        if duplicate_columns:
            st.error(
                f"Hay columnas duplicadas después de normalizar: "
                f"{', '.join(duplicate_columns)}"
            )
            st.stop()

        if missing_columns:
            st.error(
                f"Faltan columnas: {', '.join(missing_columns)}"
            )

        else:
            st.success(
                "Todas las columnas obligatorias están presentes "
                "y no hay duplicados."
            )
        st.subheader("Resumen")
        col1, col2 = st.columns(2)

        col1.metric("Filas", len(df))
        col2.metric("Columnas", len(df.columns))

        st.subheader("Vista previa")
        st.dataframe(df.head(20), use_container_width=True)

        st.subheader("Columnas detectadas")
        st.write(list(df.columns))

    except Exception as error:
        st.error(f"No se ha podido leer el archivo: {error}")