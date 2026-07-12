import pandas as pd

def load_file(upload_file):
    if upload_file.name.endswith(".csv"):
        return pd.read_csv(upload_file)
    
    return pd.read_excel(upload_file)