import streamlit as st
from src.loader import load_file
from src.analyzer import analyze_dataframe


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
        report = analyze_dataframe(df)
        
        df = report.dataframe
        duplicate_columns = report.duplicate_columns
        missing_columns = report.missing_columns
        st.success("Archivo cargado correctamente")

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

        if report.is_valid:
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