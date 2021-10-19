#!/usr/bin/env python3

import log_setup
import field_trans
import pandas as pd


def import_csv(path):
    return pd.read_csv(path)


def set_product(row):
    res = row.copy()
    for i in row.index:
        res[i] = field_trans.translate(i)(row['product_isbn'])
    return res


def set_products(df):
    res = df.copy()
    for i in df.index:
        res.iloc[i] = set_product(df.iloc[i])
    return res


def export_csv(df, path):
    df.to_csv(path)


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
