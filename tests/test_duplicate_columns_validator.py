import pandas as pd

from src.validators import DuplicateColumnsValidator


def test_detects_duplicate_columns():
    dataframe = pd.DataFrame(
        [
            ["Ana", 30, "Madrid"],
            ["Luis", 40, "Sevilla"],
        ],
        columns=["nombre", "edad", "nombre"],
    )

    validator = DuplicateColumnsValidator()
    result = validator.validate(dataframe)

    assert result.passed is False
    assert result.details == ["nombre"]


def test_passes_when_columns_are_unique():
    dataframe = pd.DataFrame(
        {
            "nombre": ["Ana", "Luis"],
            "edad": [30, 40],
            "ciudad": ["Madrid", "Sevilla"],
        }
    )

    validator = DuplicateColumnsValidator()
    result = validator.validate(dataframe)

    assert result.passed is True
    assert result.details == []