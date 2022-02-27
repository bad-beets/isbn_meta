#!/usr/bin/env python3

import numpy as np
import pandas as pd
import sqlite3


def isbn_gen() -> str:
    """Returns a randomly generated ISBN-13, within certain constraints
    Although this function generates a valid ISBN-13 according to the
    standard, the generated ISBN may still not be assigned to a title

    Parameters
    ----------

    Returns
    -------
    str
        the generated ISBN-13, represented as a string
    """
    rg_intermediate: list = list(range(6)) + list(range(600, 626)) + [65] \
        + [7] + list(range(80, 95)) + list(range(950, 990)) \
        + list(range(9917, 9990)) + list(range(99901, 99984))
    reg_groups_978: list = list(map(lambda x: str(x), rg_intermediate))
    reg_groups_979: list = ["8", "10", "11", "12"]
    prefix: str = np.random.choice(["978", "979"])
    if prefix == "978":
        group: str = np.random.choice(reg_groups_978)
    else:
        group: str = np.random.choice(reg_groups_979)
    pub_len: int = np.random.choice(list(range(2, 9 - len(group))))
    pub: str = str(np.random.choice(list(range(10**pub_len)))).zfill(pub_len)
    tit_len: int = 9 - (len(group) + pub_len)
    tit: str = str(np.random.choice(list(range(10**tit_len)))).zfill(tit_len)
    res: str = prefix + group + pub + tit

    def check_digit(partial_isbn: str) -> str:
        c: int = 0
        for i in range(len(partial_isbn)):
            if i % 2 == 0:
                c += (int(partial_isbn[i]))
            else:
                c += (int(partial_isbn[i]) * 3)
        res = (10 - (c % 10))
        return str(res) if res < 10 else "0"
    return res + check_digit(res)


def isbn_mc() -> str:
    """Returns a random known ISBN-13 from the database

    Parameters
    ----------

    Returns
    -------
    str
        the ISBN-13, represented as a string
    """
    conn: sqlite3.Connection = sqlite3.connect('isbn.db')
    df: pd.core.frame.DataFrame = pd.read_sql(
        '''SELECT isbn FROM mc_isbn''', conn)
    conn.close()
    return np.random.choice(df['isbn'])


def isbn_known() -> str:
    """Returns a random known ISBN-13 from the database

    Parameters
    ----------

    Returns
    -------
    str
        the ISBN-13, represented as a string
    """
    conn: sqlite3.Connection = sqlite3.connect('isbn.db')
    df: pd.core.frame.DataFrame = pd.read_sql(
        '''SELECT product_isbn FROM big_isbn''', conn)
    conn.close()
    return np.random.choice(df['product_isbn'])


def isbn_bogus() -> str:
    """Returns a bogus ISBN-13 that looks similar to a real one

    Parameters
    ----------

    Returns
    -------
    str
        the fake ISBN-13, represented as a string
    """
    prefix: str = np.random.choice(["978", "979"])
    infix: str = ''.join(np.random.permutation(['4', '3', '7', '7', '6',
                                                '1', '5', '6', 'O']))
    suffix: str = str(np.random.choice(list(range(10))))
    return prefix + infix + suffix
