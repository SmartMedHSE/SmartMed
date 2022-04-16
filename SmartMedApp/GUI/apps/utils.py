import os
import pathlib
import sys

import pandas as pd

sys.path.append("..")


def remove_if_exists():
    if os.path.exists('settings.py'):
        os.remove('settings.py')


def read_file(path):
    df = pd.DataFrame()
    _ext = pathlib.Path(path).suffix

    if _ext == '.csv':
        df = pd.read_csv(path)

    # if len(df.columns) <= 1:
    #     df = pd.read_csv(path, sep=';')
    if _ext == '.xlsx' or _ext == '.xls':
        df = pd.read_excel(path)
    elif _ext == '.tcv':
        df = pd.read_excel(path, sep='\t')
    else:
        df = pd.read_csv(path)
    return df


def check_first_group_cross(path):
    df = read_file(path)
    if df.loc[0, 'Group'] == 'R':
        return 'R'
    else:
        return 'T'


def check_group_column(path):
    df = read_file(path)
    if 'Group' in df.columns:
        return True
    else:
        return False


def get_class_columns(path, num):
    df = read_file(path)
    return df.loc[:, df.nunique() < num].columns
