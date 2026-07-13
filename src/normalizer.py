import unicodedata

def normalize_column_name(column_name):
    column_name = str(column_name).strip().lower()

    column_name = unicodedata.normalize(
        'NFKD',
        column_name,
    ).encode(
        'ascii',
        'ignore',
    ).decode('utf-8')

    column_name = column_name.replace(" ", "_")

    return column_name


def normalize_columns(df):
    df = df.copy()
    df.columns = [
        normalize_column_name(column)
        for column in df.columns
    ]

    return df