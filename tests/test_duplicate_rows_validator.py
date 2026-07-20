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