import pandas as pd

from src.validators import DuplicateRowsValidator

def test_detects_duplicate_rows():
    dataframe = pd.DataFrame(
        {
            "nombre": ["Ana", "Luis", "Ana"],
            "ciudad": ["Madrid", "Sevilla", "Madrid"],
            "edad": [30, 40, 30],
        }
    )

    validator = DuplicateRowsValidator()

    result = validator.validate(dataframe)

    assert result.passed is False
    assert result.details["count"] == 1
    assert result.details["duplicate_rows"] == [2]


def test_passes_when_there_are_no_duplicate_rows():
    dataframe = pd.DataFrame(
        {
            "nombre": ["Ana", "Luis", "Marta"],
            "ciudad": ["Madrid", "Sevilla", "Bilbao"],
            "edad": [30, 40, 35],
        }
    )

    validator = DuplicateRowsValidator()
    result = validator.validate(dataframe)

    assert result.passed is True
    assert result.details["count"] == 0
    assert result.details["duplicate_rows"] == []