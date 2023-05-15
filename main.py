#!/usr/bin/env python3

import log_setup
import field_trans
import choose
import pandas as pd
from typing import Union
from pathlib import Path

def import_csv(path: str) -> pd.core.frame.DataFrame:
    """Imports a csv containing items with ISBN data

    Parameters
    ----------
    path : str
        the path to the csv file

    Returns
    -------
    pd.core.frame.DataFrame
        A pandas dataframe representation of the csv file
    """
    return pd.read_csv(path)

def import_json(path_or_buf: Union[str, Path]) -> pd.core.frame.DataFrame:
    pass

def check_fields(df: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
    """Checks a dataframe for the metadata fields we expect from field_trans

    Parameters
    ----------
    df : pd.core.frame.DataFrame
        The pandas dataframe to be checked

    Returns
    -------
    pd.core.frame.DataFrame
        copy of input dataframe with expected fields, as empty series if added
    """
    res = df.copy()
    for i in field_trans.fields:
        if i not in df.columns:
            res[i] = pd.Series()
    return res


def set_product(row: pd.core.series.Series) -> pd.core.series.Series:
    """Populate a pandas series with metadata based on input series ISBN

    Parameters
    ----------
    row : pd.core.series.Series
        A pandas series containing a 'product_isbn' field

    Returns
    -------
    pd.core.series.Series
        A pandas series with metadata fields populated based off of the ISBN
    """
    res = row.copy()
    for i in row.index:
        if i in field_trans.fields:
            cell = field_trans.translate(i)(row['product_isbn'])
            res[i] = choose.wisely(cell) if type(cell) is dict else cell
    return res


def set_products(df: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
    """Returns a pandas dataframe with metadata generated from 'product_isbn'

    Parameters
    ----------
    df : pd.core.frame.DataFrame
        the dataframe from which to perform metadata lookups based on ISBN

    Returns
    -------
    pd.core.frame.DataFrame
        the new dataframe with populated metadata fields
    """
    res = df.copy()
    for i in df.index:
        res.iloc[i] = set_product(df.iloc[i])
    return res


def export_csv(df: pd.core.frame.DataFrame, path: str) -> None:
    """Exports a csv file from a pandas dataframe

    Parameters
    ----------
    df : pd.core.frame.DataFrame
        a pandas dataframe to be exported
    path : str
        the path where the csv file will be written

    Returns
    -------
    None
    """
    df.to_csv(path, index=False)

def csv_to_csv(read_path: str, write_path: str) -> None:
    """Reads a csv from read_path and writes a csv to
    write_path with the fields from field_trans populated
    with metadata from the api sources

    Parameters
    ----------
    read_path : str
        The path of the csv to be read
    write_path : str
        the path where the csv file will be written

    Returns
    -------
    None
    """
    export_csv(set_products(check_fields(import_csv(read_path))),
               write_path)
    return None

# sparse test code; plan to write more, but you should be able to glean
# basic usage from this and write some of your own tests
# isbn = "9780393009743"
# isbn_two = "9780596514983"
# isbn_three = "9781439501634"
# isbn_four = "9780934868075"
# log_setup.logger.debug("test")
# log_setup.logging.shutdown()
# test = import_csv('../isbn_meta_extra/products-export-1633955582.csv')
# test['image'] = pd.Series()
# test2 = test[[i for i in field_trans.fields]][:6]
# test3 = set_products(test2)
