import pandas as pd
import pathlib


def read_file(path):
    ext = pathlib.Path(path).suffix

    if ext == '.csv':
        df = pd.read_csv(path)

        if len(df.columns) <= 1:
            df = pd.read_csv(path, sep=';')

    elif ext == '.xlsx' or ext == '.xls':
        df = pd.read_excel(path)

    elif ext == '.tcv':
        df = pd.read_excel(path, sep='\t')

    else:
        df = pd.DataFrame()
    return df


def get_class_columns(path, num):
    df = read_file(path)
    return df.loc[:, df.nunique() < num].columns
