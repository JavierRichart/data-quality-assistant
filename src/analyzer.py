from src.normalizer import normalize_columns
from src.validators import (
    find_duplicate_columns,
    validate_required_columns
)

def analyze_dataframe(df):
    df = normalize_columns(df)

    required_columns = [
        "nombre",
        "ciudad",
        "edad"
    ]

    return {
        "dataframe": df,
        "duplicate_columns": find_duplicate_columns(df),
        "missing_columns": validate_required_columns(
            df,
            required_columns,
        ),
    }