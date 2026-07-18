from dataclasses import dataclass

import pandas as pd

from src.normalizer import normalize_columns
from src.validation_result import ValidationResult
from src.validators import (
    RequiredColumnsValidator,
    DuplicateColumnsValidator,
    NullValuesValidator,
    DataTypesValidator,
)

@dataclass
class AnalysisReport:
    dataframe: pd.DataFrame
    validation_results: list[ValidationResult]
    
    @property
    def total_rows(self) -> int:
        return len(self.dataframe)
    
    @property
    def total_columns(self) -> int:
        return len(self.dataframe.columns)
    
    @property
    def is_valid(self) -> bool:
        return all(
            result.passed
            for result in self.validation_results
        )
    
    @property
    def error_count(self) -> int:
        return sum(
            1
            for result in self.validation_results
            if not result.passed
        )
    

    def get_result(self, name: str) -> ValidationResult | None:
        for result in self.validation_results:
            if result.name == name:
                return result
            
        return None
    

def analyze_dataframe(df: pd.DataFrame) -> AnalysisReport:
    normalized_df = normalize_columns(df)

    validators = [
        RequiredColumnsValidator(
            ["nombre", "ciudad", "edad"]
        ),
        DuplicateColumnsValidator(),
        NullValuesValidator(),
        DataTypesValidator(
            {
                "nombre": "text",
                "ciudad": "text",
                "edad": "number",
            }
        )
    ]

    results = [
        validator.validate(normalized_df)
        for validator in validators
    ]

    return AnalysisReport(
        dataframe=normalized_df,
        validation_results=results,
    )