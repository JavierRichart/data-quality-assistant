import pandas as pd

from src.analyzer import analyze_dataframe


def test_analyze_dataframe_returns_valid_report():
    dataframe = pd.DataFrame(
        {
            " Nombre ": ["Ana", "Luis"],
            "CIUDAD": ["Madrid", "Sevilla"],
            "Edad": [30, 40],
            "Fecha Alta": [
                "15-07-2026",
                "16-07-2026",
            ],
        }
    )

    report = analyze_dataframe(dataframe)

    assert report.is_valid is True
    assert report.error_count == 0
    assert report.total_rows == 2
    assert report.total_columns == 4

    assert list(report.dataframe.columns) == [
        "nombre",
        "ciudad",
        "edad",
        "fecha_alta",
    ]

    assert report.quality_score == 100
    assert report.quality_level == "Excelente"
    assert report.quality_icon == "🟢"


def test_analyze_dataframe_returns_invalid_report():
    dataframe = pd.DataFrame(
        {
            "Nombre": ["Ana", "Luis", "Luis"],
            "Ciudad": ["Madrid", "Sevilla", "Sevilla"],
            "Edad": [150, 40, 40],
            "Fecha Alta": [
                "fecha_invalida",
                "16-07-2026",
                "16-07-2026",
            ],
        }
    )

    report = analyze_dataframe(dataframe)

    assert report.is_valid is False
    assert report.error_count == 3

    assert report.get_result("duplicate_rows").passed is False
    assert report.get_result("date_format").passed is False
    assert report.get_result("numeric_range").passed is False

    assert report.quality_score == 65
    assert report.quality_level == "Mejorable"
    assert report.quality_icon == "🟠"


def test_analyze_dataframe_handles_optional_date_column():
    dataframe = pd.DataFrame(
        {
            "nombre": ["Ana", "Luis"],
            "ciudad": ["Madrid", "Sevilla"],
            "edad": [30, 40],
        }
    )

    report = analyze_dataframe(dataframe)

    date_result = report.get_result("date_format")

    assert date_result is not None
    assert date_result.passed is True
    assert date_result.details == {
        "invalid_dates": {},
    }

    assert report.is_valid is True
    assert report.quality_score == 100


def test_analyze_empty_dataframe():
    dataframe = pd.DataFrame()

    report = analyze_dataframe(dataframe)

    assert report.total_rows == 0
    assert report.total_columns == 0
    assert report.is_valid is False

    required_result = report.get_result("required_columns")

    assert required_result is not None
    assert required_result.passed is False
    assert required_result.details == [
        "nombre",
        "ciudad",
        "edad",
    ]