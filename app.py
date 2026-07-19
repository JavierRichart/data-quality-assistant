import streamlit as st

from src.analyzer import analyze_dataframe
from src.loader import load_file
from src.report_renderer import render_validation_report


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

        df = report.dataframe

        st.success("Archivo cargado correctamente")

        render_validation_report(report)

        st.subheader("Resumen")
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Filas", report.total_rows)
        col2.metric("Columnas", report.total_columns)
        col3.metric(
            "Validaciones fallidas",
            report.error_count,
        )
        col4.metric(
            "Calidad de los datos",
            f"{report.quality_score}/100",
        )
        
        st.subheader("Vista previa")
        st.dataframe(
            df.head(20),
            use_container_width=True,
        )

        st.subheader("Columnas detectadas")
        st.write(list(df.columns))

    except Exception as error:
        st.error(
            f"No se ha podido leer el archivo: {error}"
        )