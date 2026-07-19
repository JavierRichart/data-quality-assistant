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
        data_types = report.get_result("data_types")

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

        data_type_details = (
            data_types.details
            if data_types is not None
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

        if data_type_details:
            st.error("Se han detectado tipos de datos incorrectos.")

            for column, error_details in data_type_details.items():
                st.write(f"**Columna:** `{column}`")
                st.write(
                    f"Tipo esperado: `{error_details['expected']}`"
                )

                if "found" in error_details:
                    st.write(
                        f"Tipo detectado por pandas: "
                        f"`{error_details['found']}`"
                    )

                if "invalid_rows" in error_details:
                    rows = [
                        row + 2
                        for row in error_details["invalid_rows"]
                    ]

                    st.write(
                        f"Filas del archivo con errores: `{rows}`"
                    )

                if "invalid_values" in error_details:
                    st.write(
                        "Valores incorrectos:",
                        error_details["invalid_values"],
                    )

                if "error" in error_details:
                    st.write(
                        f"Error: {error_details['error']}"
                    )

                st.divider()

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