from dataclasses import dataclass

import pandas as pd

from src.config import VALIDATION_WEIGHTS
from src.normalizer import normalize_columns
from src.validation_result import ValidationResult
from src.validators import (
    RequiredColumnsValidator,
    DuplicateColumnsValidator,
    DuplicateRowsValidator,
    NullValuesValidator,
    DataTypesValidator,
    DateFormatValidator,
    NumericRangeValidator,
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
    
    @property
    def quality_score(self) -> int:
        score = 0

        for result in self.validation_results:
            weight = VALIDATION_WEIGHTS.get(result.name, 0)

            if result.passed:
                score += weight

        return score
    
    @property
    def quality_level(self) -> str:
        if self.quality_score >= 90:
            return "Excelente"
        
        if self.quality_score >= 75:
            return "Buena"
        
        if self.quality_score >= 50:
            return "Mejorable"
        
        return "Baja"
    
    @property
    def quality_icon(self) -> str:
        if self.quality_score >= 90:
            return "🟢"

        if self.quality_score >= 75:
            return "🟡"

        if self.quality_score >= 50:
            return "🟠"

        return "🔴"

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
        ),
        DateFormatValidator(
            date_columns=["fecha_alta"],
        ),
        DuplicateRowsValidator(),
        NumericRangeValidator(
            ranges={
                "edad": (0, 120),
            }
        ),
    ]

    results = [
        validator.validate(normalized_df)
        for validator in validators
    ]

    return AnalysisReport(
        dataframe=normalized_df,
        validation_results=results,
    )