import pandas as pd

from src.base_validator import BaseValidator
from src.validation_result import ValidationResult


class RequiredColumnsValidator(BaseValidator):
    def __init__(self, required_columns: list[str]):
        self.required_columns = required_columns


    def validate(
            self,
            dataframe: pd.DataFrame,
    ) -> ValidationResult:
        
        missing_columns = [
            column 
            for column in self.required_columns
            if column not in dataframe.columns
        ]

        return ValidationResult(
            name="required_columns",
            passed=not missing_columns,
            details=missing_columns
        )
    

class DuplicateColumnsValidator(BaseValidator):
    def validate(self, dataframe: pd.DataFrame) -> ValidationResult:
        duplicated = dataframe.columns[
            dataframe.columns.duplicated()
        ].tolist()

        return ValidationResult(
            name="duplicated_columns",
            passed=not duplicated,
            details=duplicated,
        )
    

class NullValuesValidator(BaseValidator):
    def validate(self, dataframe: pd.DataFrame) -> ValidationResult:
        null_data =  dataframe.isnull().sum().to_dict()

        return ValidationResult(
            name="null_data",
            passed=not any(null_data.values()),
            details=null_data
        )