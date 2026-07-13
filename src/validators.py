
def validate_required_columns(df, required_columns):
    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    return missing_columns