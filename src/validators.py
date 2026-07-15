import pandas as pd

from src.base_validator import BaseValidator

class RequiredColumnsValidator(BaseValidator):
    def __init__(self, required_columns: list[str]):
        self.required_columns = required_columns


    def validate_required_columns(df, required_columns):
        missing_columns = [
            column
            for column in required_columns
            if column not in df.columns
        ]

        return missing_columns


def find_duplicate_columns(df):
    duplicated = df.columns[df.columns.duplicated()].tolist()
    return duplicated


def find_null_values(df):
    return df.isnull().sum().to_dict()