import pandas as pd

from src.validators import DateFormatValidator


def test_detects_invalid_date_format():
    dataframe = pd.DataFrame(
        {
            "fecha": [
                "15-07-2026",
                "2026/07/16",
                "17-07-2026",
            ],
        }
    )

    validator = DateFormatValidator(
        date_columns=["fecha"],
        date_format="%d-%m-%Y",
    )

    result = validator.validate(dataframe)

    assert result.passed is False

    invalid_dates = result.details["invalid_dates"]

    assert invalid_dates["fecha"]["expected_format"] == "%d-%m-%Y"
    assert invalid_dates["fecha"]["invalid_rows"] == [1]
    assert invalid_dates["fecha"]["invalid_values"] == ["2026/07/16"]


def test_passes_when_date_formats_are_valid():
    dataframe = pd.DataFrame(
        {
            "fecha": [
                "15-07-2026",
                "16-07-2026",
                "17-07-2026",
            ],
        }
    )

    validator = DateFormatValidator(
        date_columns=["fecha"],
        date_format="%d-%m-%Y",
    )

    result = validator.validate(dataframe)

    assert result.passed is True
    assert result.details == {
        "invalid_dates": {},
    }