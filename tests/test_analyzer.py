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