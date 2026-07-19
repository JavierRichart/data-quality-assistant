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
            details=missing_columns,
        )


class DuplicateColumnsValidator(BaseValidator):
    def validate(self, dataframe: pd.DataFrame) -> ValidationResult:
        duplicate_columns = dataframe.columns[
            dataframe.columns.duplicated()
        ].tolist()

        return ValidationResult(
            name="duplicate_columns",
            passed=not duplicate_columns,
            details=duplicate_columns,
        )


class NullValuesValidator(BaseValidator):
    def validate(self, dataframe: pd.DataFrame) -> ValidationResult:
        null_data = dataframe.isnull().sum().to_dict()

        return ValidationResult(
            name="null_data",
            passed=not any(null_data.values()),
            details=null_data,
        )


class DataTypesValidator(BaseValidator):
    def __init__(self, expected_types: dict[str, str]):
        self.expected_types = expected_types

    def validate(self, dataframe: pd.DataFrame) -> ValidationResult:
        invalid_types = {}

        for column, expected_type in self.expected_types.items():
            if column not in dataframe.columns:
                continue

            column_data = dataframe[column]

            if expected_type == "number":
                converted_data = pd.to_numeric(
                    column_data,
                    errors="coerce",
                )

                invalid_mask = (
                    converted_data.isna()
                    & column_data.notna()
                )

            elif expected_type == "text":
                invalid_mask = column_data.apply(
                    lambda value: (
                        pd.notna(value)
                        and not isinstance(value, str)
                    )
                )

            else:
                invalid_types[column] = {
                    "expected": expected_type,
                    "error": "Unsupported expected type",
                }
                continue

            if invalid_mask.any():
                invalid_types[column] = {
                    "expected": expected_type,
                    "found": str(column_data.dtype),
                    "invalid_rows": dataframe.index[
                        invalid_mask
                    ].tolist(),
                    "invalid_values": column_data[
                        invalid_mask
                    ].tolist(),
                }

        return ValidationResult(
            name="data_types",
            passed=not invalid_types,
            details=invalid_types,
        )