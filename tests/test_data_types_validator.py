import pandas as pd

from src.validators import DataTypesValidator


def test_detects_invalid_numeric_values():
    dataframe = pd.DataFrame(
        {
            "nombre": ["Ana", "Luis", "Marta"],
            "edad": [30, "desconocida", 40],
        }
    )

    validator = DataTypesValidator(
        expected_types={
            "nombre": "text",
            "edad": "number",
        }
    )

    result = validator.validate(dataframe)

    assert result.passed is False
    assert result.details["edad"]["expected"] == "number"
    assert result.details["edad"]["invalid_rows"] == [1]
    assert result.details["edad"]["invalid_values"] == ["desconocida"]


def test_passes_when_data_types_are_valid():
    dataframe = pd.DataFrame(
        {
            "nombre": ["Ana", "Luis"],
            "edad": [30, 40],
        }
    )

    validator = DataTypesValidator(
        expected_types={
            "nombre": "text",
            "edad": "number",
        }
    )

    result = validator.validate(dataframe)

    assert result.passed is True
    assert result.details == {}