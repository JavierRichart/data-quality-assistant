import pandas as pd

from src.validators import NumericRangeValidator


def test_detects_values_outside_numeric_range():
    dataframe = pd.DataFrame(
        {
            "edad": [30, -5, 145],
        }
    )

    validator = NumericRangeValidator(
        ranges={
            "edad": (0, 120),
        }
    )

    result = validator.validate(dataframe)

    assert result.passed is False
    assert result.details["edad"]["minimum"] == 0
    assert result.details["edad"]["maximum"] == 120
    assert result.details["edad"]["invalid_rows"] == [1, 2]
    assert result.details["edad"]["invalid_values"] == [-5, 145]


def test_passes_when_values_are_inside_numeric_range():
    dataframe = pd.DataFrame(
        {
            "edad": [18, 30, 75],
        }
    )

    validator = NumericRangeValidator(
        ranges={
            "edad": (0, 120),
        }
    )

    result = validator.validate(dataframe)

    assert result.passed is True
    assert result.details == {}