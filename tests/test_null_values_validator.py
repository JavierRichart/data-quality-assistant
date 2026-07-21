import pandas as pd

from src.validators import NullValuesValidator


def test_detects_null_values():
    dataframe = pd.DataFrame(
        {
            "nombre": ["Ana", None],
            "ciudad": ["Madrid", "Sevilla"],
            "edad": [30, None],
        }
    )

    validator = NullValuesValidator()
    result = validator.validate(dataframe)

    assert result.passed is False
    assert result.details == {
        "nombre": 1,
        "ciudad": 0,
        "edad": 1,
    }


def test_passes_when_there_are_no_null_values():
    dataframe = pd.DataFrame(
        {
            "nombre": ["Ana", "Luis"],
            "ciudad": ["Madrid", "Sevilla"],
            "edad": [30, 40],
        }
    )

    validator = NullValuesValidator()
    result = validator.validate(dataframe)

    assert result.passed is True
    assert result.details == {
        "nombre": 0,
        "ciudad": 0,
        "edad": 0,
    }