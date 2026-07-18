import streamlit as st

from src.analyzer import analyze_dataframe
from src.loader import load_file


st.set_page_config(
    page_title="Data Quality Assistant",
    page_icon="🔍",
    layout="wide",
)

st.title("Data Quality Assistant")
st.write("Sube un archivo Excel/CSV para analizar")

uploaded_file = st.file_uploader(
    "Selecciona un archivo",
    type=["xlsx", "csv"],
)

if uploaded_file is not None:
    try:
        df = load_file(uploaded_file)
        report = analyze_dataframe(df)

        duplicate_columns = report.get_result("duplicate_columns")
        missing_columns = report.get_result("required_columns")
        null_values = report.get_result("null_data")

        duplicate_details = (
            duplicate_columns.details
            if duplicate_columns is not None
            else []
        )

        missing_details = (
            missing_columns.details
            if missing_columns is not None
            else []
        )

        null_details = (
            {
                column: count
                for column, count in null_values.details.items()
                if count > 0
            }
            if null_values is not None
            else {}
        )

        df = report.dataframe

        st.success("Archivo cargado correctamente")

        st.subheader("Validación de columnas")

        if duplicate_details:
            st.error(
                "Hay columnas duplicadas después de normalizar: "
                f"{', '.join(duplicate_details)}"
            )
            st.stop()

        if missing_details:
            st.error(
                f"Faltan columnas: {', '.join(missing_details)}"
            )

        if null_details:
            st.warning("Se han detectado valores vacíos:")

            for column, count in null_details.items():
                st.write(f"- {column}: {count}")

        if report.is_valid:
            st.success(
                "El archivo ha superado todas las validaciones."
            )

        st.subheader("Resumen")
        col1, col2, col3 = st.columns(3)

        col1.metric("Filas", report.total_rows)
        col2.metric("Columnas", report.total_columns)
        col3.metric("Validaciones fallidas", report.error_count)

        st.subheader("Vista previa")
        st.dataframe(df.head(20), use_container_width=True)

        st.subheader("Columnas detectadas")
        st.write(list(df.columns))

    except Exception as error:
        st.error(f"No se ha podido leer el archivo: {error}")