from dataclasses import dataclass

import pandas as pd

from src.normalizer import normalize_columns
from src.validators import (
    find_duplicate_columns,
    validate_required_columns
)

@dataclass
class AnalysisReport:
    dataframe: pd.DataFrame
    duplicate_columns: list[str]
    missing_columns: list[str]

    @property
    def is_valid(self) -> bool:
        return not self.duplicate_columns and not self.missing_columns
    
    @property
    def total_rows(self) -> int:
        return len(self.dataframe)
    
    @property
    def total_columns(self) -> int:
        return len(self.dataframe.columns)
    
    @property
    def error_count(self) -> int:
        return len(self.duplicate_columns) + len(self.missing_columns)

def analyze_dataframe(df):
    normalized_df = normalize_columns(df)

    required_columns = [
        "nombre",
        "ciudad",
        "edad",
    ]

    return AnalysisReport(
        dataframe=normalized_df,
        duplicate_columns=find_duplicate_columns(normalized_df),
        missing_columns=validate_required_columns(
            normalized_df,
            required_columns
        ),
    )