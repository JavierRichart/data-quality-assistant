import streamlit as st

from src.analyzer import AnalysisReport
from src.validation_result import ValidationResult


def render_duplicate_columns(
    result: ValidationResult | None,
) -> None:
    if result is None or result.passed:
        return

    st.error(
        "Hay columnas duplicadas después de normalizar: "
        f"{', '.join(result.details)}"
    )

    st.stop()


def render_missing_columns(
    result: ValidationResult | None,
) -> None:
    if result is None or result.passed:
        return

    st.error(
        f"Faltan columnas: {', '.join(result.details)}"
    )


def render_null_values(
    result: ValidationResult | None,
) -> None:
    if result is None or result.passed:
        return

    null_details = {
        column: count
        for column, count in result.details.items()
        if count > 0
    }

    st.warning("Se han detectado valores vacíos:")

    for column, count in null_details.items():
        st.write(f"- `{column}`: {count}")


def render_data_types(
    result: ValidationResult | None,
) -> None:
    if result is None or result.passed:
        return

    st.error("Se han detectado tipos de datos incorrectos.")

    for column, error_details in result.details.items():
        st.write(f"**Columna:** `{column}`")
        st.write(
            f"Tipo esperado: `{error_details['expected']}`"
        )

        if "found" in error_details:
            st.write(
                "Tipo detectado por pandas: "
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


def render_date_format(
    result: ValidationResult | None,
) -> None:
    if result is None or result.passed:
        return

    st.error("Se han detectado fechas con formato incorrecto.")

    for column, error_details in result.details.items():
        st.write(f"**Columna:** `{column}`")
        st.write(
            "Formato esperado: "
            f"`{error_details['expected_format']}`"
        )

        rows = [
            row + 2
            for row in error_details["invalid_rows"]
        ]

        st.write(
            f"Filas del archivo con errores: `{rows}`"
        )

        st.write(
            "Valores incorrectos:",
            error_details["invalid_values"],
        )

        st.divider()


def render_duplicate_rows(
    result: ValidationResult | None,
) -> None:
    
    if result is None or result.passed:
        return

    count = result.details["count"]
    rows = [
        row + 2
        for row in result.details["duplicate_rows"]
    ]

    st.error(
        f"Se han encontrado "
        f"{count} filas duplicadas."
    )

    st.write(
        f"Filas: {rows}"
    )


def render_validation_report(
    report: AnalysisReport,
) -> None:
    st.subheader("Validación de datos")

    duplicate_rows = report.get_result(
        "duplicate_rows"
    )

    render_duplicate_columns(
        report.get_result("duplicate_columns")
    )

    render_missing_columns(
        report.get_result("required_columns")
    )

    render_null_values(
        report.get_result("null_data")
    )

    render_data_types(
        report.get_result("data_types")
    )

    render_date_format(
        report.get_result("date_format")
    )

    render_duplicate_rows(
        report.get_result("duplicate_rows"),
    )

    render_numeric_range(
        report.get_result("numeric_range")
    )

    if report.is_valid:
        st.success(
            "El archivo ha superado todas las validaciones."
        )


def render_numeric_range(
    result: ValidationResult | None,
) -> None:
    if result is None or result.passed:
        return

    st.error(
        "Se han detectado valores fuera del rango permitido."
    )

    for column, error_details in result.details.items():
        st.write(f"**Columna:** `{column}`")
        st.write(
            "Rango permitido: "
            f"`{error_details['minimum']}` - "
            f"`{error_details['maximum']}`"
        )

        rows = [
            row + 2
            for row in error_details["invalid_rows"]
        ]

        st.write(
            f"Filas del archivo con errores: `{rows}`"
        )

        st.write(
            "Valores incorrectos:",
            error_details["invalid_values"],
        )

        st.divider()