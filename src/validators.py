import pandas as pd

from src.base_validator import BaseValidator


class RequiredColumnsValidator(BaseValidator):
    def __init__(self, required_columns: list[str]):
        self.required_columns = required_columns


    def validate(self, dataframe: pd.DataFrame) -> list[str]:
        return [
            column
            for column in self.required_columns
            if column not in dataframe.columns
        ]


class DuplicateColumnsValidator(BaseValidator):
    def validate(self, dataframe: pd.DataFrame) -> list[str]:
        return dataframe.columns[
            dataframe.columns.duplicated()
        ].tolist()
    

class NullValuesValidator(BaseValidator):
    def validate(self, dataframe: pd.DataFrame) -> dict[str, int]:
        return dataframe.isnull().sum().to_dict()