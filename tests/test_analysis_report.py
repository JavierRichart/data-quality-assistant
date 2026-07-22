import pandas as pd
import pytest

from src.analyzer import AnalysisReport
from src.validation_result import ValidationResult


ALL_VALIDATIONS = [
    "required_columns",
    "duplicate_columns",
    "duplicate_rows",
    "data_types",
    "numeric_range",
    "null_data",
    "date_format",
]


def create_report(passed_validations: set[str]) -> AnalysisReport:
    results = [
        ValidationResult(
            name=name,
            passed=name in passed_validations,
            details={},
        )
        for name in ALL_VALIDATIONS
    ]

    return AnalysisReport(
        dataframe=pd.DataFrame(),
        validation_results=results,
    )


@pytest.mark.parametrize(
    "passed_validations, expected_score, expected_level, expected_icon",
    [
        (
            set(ALL_VALIDATIONS),
            100,
            "Excelente",
            "🟢",
        ),
        (
            {
                "required_columns",
                "data_types",
                "numeric_range",
                "duplicate_columns",
                "duplicate_rows",
                "null_data",
            },
            90,
            "Excelente",
            "🟢",
        ),
        (
            {
                "required_columns",
                "data_types",
                "duplicate_columns",
                "duplicate_rows",
                "null_data",
            },
            75,
            "Buena",
            "🟡",
        ),
        (
            {
                "required_columns",
                "numeric_range",
                "duplicate_columns",
            },
            50,
            "Mejorable",
            "🟠",
        ),
        (
            {
                "required_columns",
                "duplicate_columns",
            },
            35,
            "Baja",
            "🔴",
        ),
    ],
)
def test_quality_classification(
    passed_validations,
    expected_score,
    expected_level,
    expected_icon,
):
    report = create_report(passed_validations)

    assert report.quality_score == expected_score
    assert report.quality_level == expected_level
    assert report.quality_icon == expected_icon


def test_get_result_returns_matching_validation():
    report = create_report(
        {
            "required_columns",
            "duplicate_columns",
        }
    )

    result = report.get_result("required_columns")

    assert result is not None
    assert result.name == "required_columns"
    assert result.passed is True


def test_get_result_returns_none_when_validation_does_not_exist():
    report = create_report(set())

    result = report.get_result("unknown_validation")

    assert result is None