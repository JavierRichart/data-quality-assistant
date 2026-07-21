import pandas as pd

from src.validators import RequiredColumnsValidator


def test_detects_missing_required_columns():
    dataframe = pd.DataFrame(
        {
            "nombre": ["Ana", "Luis"],
            "edad": [30, 40],
        }
    )

    validator = RequiredColumnsValidator(
        required_columns=["nombre", "ciudad", "edad"]
    )

    result = validator.validate(dataframe)

    assert result.passed is False
    assert result.details == ["ciudad"]


def test_passes_when_all_required_columns_exist():
    dataframe = pd.DataFrame(
        {
            "nombre": ["Ana", "Luis"],
            "ciudad": ["Madrid", "Sevilla"],
            "edad": [30, 40],
        }
    )

    validator = RequiredColumnsValidator(
        required_columns=["nombre", "ciudad", "edad"]
    )

    result = validator.validate(dataframe)

    assert result.passed is True
    assert result.details == []