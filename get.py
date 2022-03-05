import metric
import functools
import requests
import sqlite3
import sqlalchemy as db
import pandas as pd
import configparser
import load_config
from pathlib import Path
from typing import List, Optional
from typing import Callable
from multiprocessing import Pool

cfg: configparser.ConfigParser = load_config.cfg


def key_swallow(f: Callable[[str, Optional[requests.sessions.Session]],
                            Optional[dict]]) -> Callable[
                                [str, Optional[requests.sessions.Session]],
                                Optional[dict]]:
    """Wraps an API call function in order to eat KeyErrors

    This is used as a decorator throughout get.py

    Parameters
    ----------
    f : Callable[[str, Optional[requests.sessions.Session]], Optional[dict]]
        An api call with a given key to be looked up

    Returns
    -------
    Callable[[str, Optional[requests.sessions.Session]], Optional[dict]]
        An outer function that wraps f with a try/except block
    """

    @functools.wraps(f)
    def attempt(x: str,
                y: Optional[requests.sessions.Session] = None
                ) -> Optional[dict]:
        try:
            return f(x, y)
        except KeyError:
            return None
        return None
    return attempt


def yarn_swallow(f: Callable[[str, Optional[requests.sessions.Session]],
                             Optional[str]]) -> Callable[
                                 [str,
                                  Optional[requests.sessions.Session]],
                                 Optional[str]]:
    """Wraps an API call function in order to eat KeyErrors

    but for functions that can return strings

    Parameters
    ----------
    f : Callable[[str, Optional[requests.sessions.Session]], Optional[str]]
        An api call with a given key to be looked up

    Returns
    -------
    Callable[[str, Optional[requests.sessions.Session]], Optional[str]]
        An outer function that wraps f with a try/except block
    """

    @functools.wraps(f)
    def attempt(x: str,
                y: Optional[requests.sessions.Session] = None
                ) -> Optional[str]:
        try:
            return f(x, y)
        except KeyError:
            return None
        return None
    return attempt


def map_swallow(f: Callable[[dict],
                            Optional[dict]]) -> Callable[[dict],
                                                         Optional[dict]]:
    """Wraps an API call function in order to eat KeyErrors

    but for functions that take and return dictionaries

    Parameters
    ----------
    f : Callable[[dict], Optional[dict]]
        An api call with a given key to be looked up

    Returns
    -------
    Callable[[dict], Optional[dict]]
        An outer function that wraps f with a try/except block
    """

    @functools.wraps(f)
    def attempt(x: dict) -> Optional[dict]:
        try:
            return f(x)
        except KeyError:
            return None
        return None
    return attempt


def csv_meta(isbn: str, path: str
             ) -> Optional[pd.core.frame.DataFrame]:
    """Gets the metadata of an ISBN from a Comma Separated Values
    (.csv) file

    Parameters
    ----------
    isbn : str
        The ISBN of the work
    path : str
        The filesystem path to the csv file

    Returns
    -------
    Optional[pd.core.frame.DataFrame]
        The Pandas DataFrame of metadata from the database, or None
    """
    df: pd.core.frame.DataFrame = pd.read_csv(path)[['product_isbn',
                                                     'product_title',
                                                     'format',
                                                     'product_description',
                                                     'product_retail',
                                                     'publisher',
                                                     'product_weight',
                                                     'product_width',
                                                     'product_height',
                                                     'product_thickness',
                                                     'Author']]
    return df[df['product_isbn'] == isbn]


def sqlite_meta(isbn: str,
                c: Optional[sqlite3.Connection] = None
                ) -> Optional[pd.core.frame.DataFrame]:
    """Gets the metadata of an ISBN from the sqlite database

    Parameters
    ----------
    isbn : str
        The ISBN of the work
    c: Optional[sqlite3.Connection]
        An optional, existing sqlite3 connection to make the SQL query
        A new one will be created and closed within the function call
        if one is not provided as an argument

    Returns
    -------
    Optional[pd.core.frame.DataFrame]
        The Pandas DataFrame of metadata from the database, or None
    """
    assert all(list(map(str.isdigit, isbn)))           # input checks
    assert (isbn[:3] == '978') or (isbn[:3] == '979')  # to prevent
    assert len(isbn) == 13                             # sql injection
    assert type(isbn) == str
    if not c:
        with sqlite3.connect('isbn.db') as c:
            return pd.read_sql('SELECT * FROM ' +
                               'products WHERE product_isbn = ' +
                               isbn, con=c)
    else:
        return pd.read_sql('SELECT * FROM ' +
                           'products WHERE product_isbn = ' +
                           isbn, con=c)


def mariadb_meta(isbn: str,
                 c: Optional[db.engine.base.Connection] = None
                 ) -> Optional[pd.core.frame.DataFrame]:
    """Gets the metadata of an ISBN from a MariaDB mysql database

    Parameters
    ----------
    isbn : str
        The ISBN of the work
    c: Optional[db.engine.base.Connection]
        An optional, existing sqlalchemy connection to make the SQL query
        A new one will be created and closed within the function call
        if one is not provided as an argument

    Returns
    -------
    Optional[pd.core.frame.DataFrame]
        The Pandas DataFrame of metadata from the database, or None
    """
    assert all(list(map(str.isdigit, isbn)))           # input checks
    assert (isbn[:3] == '978') or (isbn[:3] == '979')  # to prevent
    assert len(isbn) == 13                             # sql injection
    assert type(isbn) == str

    def uri_gen(cfg: configparser.ConfigParser = cfg
                ) -> str:
        return ''.join([cfg['mariadb']['proto'], '://',
                        cfg['mariadb']['user'], ':',
                        cfg['mariadb']['auth'], '@',
                        cfg['mariadb']['server'], '/',
                        cfg['mariadb']['db']])

    def db_select(df: pd.core.frame.DataFrame
                  ) -> pd.core.frame.DataFrame:
        return df[['product_isbn',
                   'product_title',
                   'product_description',
                   'product_retail',
                   'product_weight',
                   'product_width',
                   'product_height',
                   'product_thickness',
                   ]]  # still needs format, publisher, Author
    if not c:
        engine = db.create_engine(uri_gen())
        with engine.connect() as c:
            return db_select(pd.read_sql(
                'SELECT * FROM ' +
                'product WHERE product_isbn = ' +
                isbn, con=c))
    else:
        return db_select(pd.read_sql(
            'SELECT * FROM ' +
            'product WHERE product_isbn = ' +
            isbn, con=c))


def df_meta(isbn: str,
            df: pd.core.frame.DataFrame
            ) -> Optional[pd.core.frame.DataFrame]:
    """Gets the metadata of an ISBN from a Pandas DataFrame

    Parameters
    ----------
    isbn : str
        The ISBN of the work
    df: pd.core.frame.DataFrame
        A Pandas DataFrame containing ISBN metadata

    Returns
    -------
    Optional[pd.core.frame.DataFrame]
        The Pandas DataFrame of metadata from the database, or None
    """
    return df[df['product_isbn'] == isbn]


@yarn_swallow
def gvol_from_isbn(isbn: str,
                   s: Optional[requests.sessions.Session] = None
                   ) -> Optional[str]:
    """Gets a google books volume id from the API using a given ISBN

    Parameters
    ----------
    isbn : str
        The ISBN of the work
    s: Optional[requests.sessions.Session]
        An optional, existing requests session to make the API call
        A new one will be created and closed within the function call
        if one is not provided as an argument

    Returns
    -------
    Optional[str]
        The Google Books Volume ID string, or None if not found
    """

    if not s:
        with requests.Session() as s:
            r: requests.models.Response = s.get(cfg['gobo']['uri'] + isbn)
            if r.status_code == 200:
                return r.json()["items"][0]['id']
    else:
        r: requests.models.Response = s.get(cfg['gobo']['uri'] + isbn)
        if r.status_code == 200:
            return r.json()["items"][0]['id']
    return None


@key_swallow
def gobo_meta(isbn: str,
              s: Optional[requests.sessions.Session] = None
              ) -> Optional[dict]:
    """Gets the metadata of an ISBN from the Google Books API

    Parameters
    ----------
    isbn : str
        The ISBN of the work
    s: Optional[requests.sessions.Session]
        An optional, existing requests session to make the API call
        A new one will be created and closed within the function call
        if one is not provided as an argument

    Returns
    -------
    Optional[dict]
        The dictionary of metadata from the API, or None
    """

    if not s:
        with requests.Session() as s:
            vol_id: Optional[str] = gvol_from_isbn(isbn, s)
            if vol_id:
                r: requests.models.Response = s.get(
                    cfg['gobo']['vol_uri'] + vol_id, params=cfg['gobo_params'])
                if r.status_code == 200:
                    return r.json()["volumeInfo"]
    else:
        vol_id: Optional[str] = gvol_from_isbn(isbn, s)
        if vol_id:
            r: requests.models.Response = s.get(
                cfg['gobo']['vol_uri'] + vol_id, params=cfg['gobo_params'])
            if r.status_code == 200:
                return r.json()["volumeInfo"]
    return None


@key_swallow
def ol_meta(isbn: str,
            s: Optional[requests.sessions.Session] = None
            ) -> Optional[dict]:
    """Gets the metadata of an ISBN from the OpenLibrary API

    Parameters
    ----------
    isbn : str
        The ISBN of the work
    s: Optional[requests.sessions.Session]
        An optional, existing requests session to make the API call
        A new one will be created and closed within the function call
        if one is not provided as an argument

    Returns
    -------
    Optional[dict]
        The dictionary of metadata from the API, or None
    """

    if not s:
        with requests.Session() as s:
            r: requests.models.Response = s.get(
                cfg['ol']['uri'] + isbn, params=cfg['ol_params'])
            if r.status_code == 200:
                return r.json()['ISBN:' + isbn]
    else:
        r: requests.models.Response = s.get(
            cfg['ol']['uri'] + isbn, params=cfg['ol_params'])
        if r.status_code == 200:
            return r.json()['ISBN:' + isbn]
    return None


@key_swallow
def isbndb_meta(isbn: str,
                s: Optional[requests.sessions.Session] = None
                ) -> Optional[dict]:
    """Gets the metadata of an ISBN from the ISBNDB API

    Parameters
    ----------
    isbn : str
        The ISBN of the work
    s: Optional[requests.sessions.Session]
        An optional, existing requests session to make the API call
        A new one will be created and closed within the function call
        if one is not provided as an argument

    Returns
    -------
    Optional[dict]
        The dictionary of metadata from the API, or None
    """

    if not s:
        with requests.Session() as s:
            r: requests.models.Response = s.get(
                cfg['isbndb']['uri'] + "book/" + isbn,
                headers=cfg['isbndb_headers'])
            if r.status_code == 200:
                return r.json()['book']
    else:
        r: requests.models.Response = s.get(
            cfg['isbndb']['uri'] + "book/" + isbn,
            headers=cfg['isbndb_headers'])
        if r.status_code == 200:
            return r.json()['book']
    return None


def multi_helper(isbn: str,
                 s: Optional[requests.sessions.Session],
                 f: Callable[[str,
                              Optional[requests.sessions.Session]],
                             Optional[dict]]
                 ) -> Optional[dict]:
    """Helper function used for partial application inside meta
    multi_helper takes three argumens, and calls the last argument
    with the first two as its own arguments
    lambdas, closures, and local functions cannot be pickled
    (serialized) for multiprocessing, hence the top-level definition

    Parameters
    ----------
    isbn : str
        The ISBN of the work
    s: Optional[requests.sessions.Session]
        An optional, existing requests session to make the API call
        A new one will be created and closed within the function call
        if one is not provided as an argument
    f: Callable[[str, Optional[requests.sessions.Session]],
                             Optional[dict]]

    Returns
    -------
    Optional[dict]
        A dictionary representing the returned API data
    """
    return f(isbn, s)


@functools.lru_cache
# cache results using the least recently used algo in functools module
def meta(isbn: str, method: List[Callable[
        [str, Optional[requests.sessions.Session]], Optional[dict]]] =
         [gobo_meta, ol_meta, isbndb_meta],
         s: Optional[requests.sessions.Session] = None
         ) -> Optional[dict]:
    """Gets the metadata for a given ISBN from various API sources

    Parameters
    ----------
    isbn : str
        The ISBN of the work
    method : list
        A list of functions that implement specific API lookups
    s: Optional[requests.sessions.Session]
        An optional, existing requests session to make the API call
        A new one will be created and closed within the function call
        if one is not provided as an argument

    Returns
    -------
    Optional[dict]
        A dictionary of API names mapped to returned metadata from each
    """

    def prettify(x: Callable[
            [str, Optional[requests.sessions.Session]],
            Optional[dict]]
                 ) -> str:
        # get API names from their functions using the closure dunder
        return x.__closure__[0].cell_contents.__name__.split('_')[0]

    m_names: List[str] = list(map(prettify, method))
    if not s:
        with requests.Session() as s:
            with Pool(6) as p:
                meta: List[Optional[dict]] = [m for m in p.map(
                    functools.partial(multi_helper, isbn, s), method)]
                return {k: v for (k, v) in zip(m_names, meta)}
    else:
        with Pool(6) as p:
            meta: List[Optional[dict]] = [m for m in p.map(
                functools.partial(multi_helper, isbn, s), method)]
            return {k: v for (k, v) in zip(m_names, meta)}
    return None


def field(f: str, isbn: str) -> dict:
    """Gets field data for a Given ISBN and field

    Parameters
    ----------
    f : str
        The field we're interested in
    isbn : str
        The ISBN of the work

    Returns
    -------
    dict
        a dictionary of specified field data from each API searched
    """

    m: dict = meta(isbn)

    @map_swallow
    def wrapped(x: dict) -> Optional[dict]:
        # helper function to do the lookups on the returned metadata
        return x[f]
    return {k + '_' + f: wrapped(v) for (k, v) in m.items() if v}


def gf_partial(f: str) -> Callable[[str], dict]:
    """A helper for partial application of the field function

    Parameters
    ----------
    f : str
        The field of interest

    Returns
    -------
    Callable[[str], dict]
        a partial application of the field function using f as the field
    """

    return functools.partial(field, f)


# here partial application saves us a lot of extraneous code
title: Callable[[str], dict] = gf_partial("title")
subtitle: Callable[[str], dict] = gf_partial("subtitle")
authors: Callable[[str], dict] = gf_partial("authors")
published_date: Callable[[str], dict] = gf_partial("publishedDate")
description: Callable[[str], dict] = gf_partial("description")
industry_identifiers: Callable[[str], dict] = gf_partial(
    "industryIdentifiers")
page_count: Callable[[str], dict] = gf_partial("printedPageCount")
msrp: Callable[[str], dict] = gf_partial("msrp")
binding: Callable[[str], dict] = gf_partial("binding")


def gen_doc():
    """Generates docstrings for field partials
    """

    f: List[Callable[[str], dict]] = [title, subtitle, authors,
                                      published_date, description,
                                      industry_identifiers, page_count,
                                      msrp, binding]
    g: List[str] = ["title", "subtitle", "authors", "published_date",
                    "description", "industry_identifiers", "page_count",
                    "msrp", "binding"]

    def into_doc(field: str) -> str:
        # returns neat docstrings with fields inserted appropriately
        return Path('doc_template').read_text().replace('replace_me',
                                                        field)
    for i in range(len(f)):
        f[i].__doc__ = into_doc(g[i])
    return None


gen_doc()


def publisher(isbn: str) -> dict:
    """Gets the publisher of an ISBN from metadata API sources

    Parameters
    ----------
    isbn : str
        The ISBN of the work

    Returns
    -------
    dict
        a dictionary of publisher data from each API searched
    """

    m: dict = meta(isbn)
    res: dict = {}
    for i in m.keys():
        if m[i]:
            if i == 'ol':
                try:
                    res[i] = m[i]['publishers']
                except KeyError:
                    res[i] = None
            else:
                try:
                    res[i] = m[i]['publisher']
                except KeyError:
                    res[i] = None
        else:
            res[i] = None
    return res


def dimensions(isbn: str) -> dict:
    """Gets the dimensions of an ISBN from metadata API sources

    Parameters
    ----------
    isbn : str
        The ISBN of the work

    Returns
    -------
    dict
        a dictionary of dimension data from each API searched
    """

    m: dict = meta(isbn)
    res: dict = {}
    for i in m.keys():
        if m[i]:
            if i == 'gobo':
                try:
                    res[i] = metric.metric_conversion(m[i]['dimensions'])
                except KeyError:
                    res[i] = None
            else:
                try:
                    res[i] = m[i]['dimensions']
                except KeyError:
                    res[i] = None
        else:
            res[i] = None
    return res


@key_swallow
def width(isbn: str) -> dict:
    """Gets the width of an ISBN from metadata API sources

    Parameters
    ----------
    isbn : str
        The ISBN of the work

    Returns
    -------
    dict
        a dictionary of width data from each API searched
    """

    res: dict = dimensions(isbn)
    for i in res:
        if res[i] is not None:
            if i == 'gobo':
                res[i] = res[i]['width']
            elif i == 'isbndb':
                res[i] = res[i].split(',')[1].split(':')[1][1:]
        else:
            res[i] = None
    return res


@key_swallow
def height(isbn: str) -> dict:
    """Gets the height of an ISBN from metadata API sources

    Parameters
    ----------
    isbn : str
        The ISBN of the work

    Returns
    -------
    dict
        a dictionary of height data from each API searched
    """

    res: dict = dimensions(isbn)
    for i in res:
        if res[i] is not None:
            if i == 'gobo':
                res[i] = res[i]['height']
            elif i == 'isbndb':
                res[i] = res[i].split(',')[0].split(':')[1][1:]
        else:
            res[i] = None
    return res


@key_swallow
def thickness(isbn: str) -> dict:
    """Gets the thickness of an ISBN from metadata API sources

    Parameters
    ----------
    isbn : str
        The ISBN of the work

    Returns
    -------
    dict
        a dictionary of thickness data from each API searched
    """

    res: dict = dimensions(isbn)
    for i in res:
        if res[i] is not None:
            if i == 'gobo':
                res[i] = res[i]['thickness']
            elif i == 'isbndb':
                res[i] = res[i].split(',')[3].split(':')[1][1:]
        else:
            res[i] = None
    return res


@key_swallow
def weight(isbn: str) -> dict:
    """Gets the weight of an ISBN from metadata API sources

    Parameters
    ----------
    isbn : str
        The ISBN of the work

    Returns
    -------
    dict
        a dictionary of weight data from each API searched
    """

    res: dict = dimensions(isbn)
    if res['isbndb']:
        res['isbndb'] = res['isbndb'].split(',')[2].split(':')[1][1:]
    return {'isbndb': res['isbndb']}


def ol_cover(isbn: str) -> Optional[str]:
    """Gets the cover of an ISBN from OpenLibrary Covers

    Parameters
    ----------
    isbn : str
        The ISBN of the work

    Returns
    -------
    str
        the URI of the cover on OpenLibrary, or None
    """

    url: str = cfg['ol']['covers_uri'] + isbn + cfg['ol']['covers_suffix']
    r: requests.models.Response = requests.get(url)
    if r.status_code == 200:
        return url
    else:
        return None


def image_url(isbn: str) -> dict:
    """Gets the image url of an ISBN from metadata API sources

    Parameters
    ----------
    isbn : str
        The ISBN of the work

    Returns
    -------
    dict
        a dictionary of image url data from each API searched
    """

    m: dict = meta(isbn)
    res: dict = {}
    for i in m.keys():
        if m[i]:
            if i == 'gobo':
                try:
                    res[i] = m[i]['imageLinks']
                except KeyError:
                    res[i] = None
            elif i == 'ol':
                res[i] = ol_cover(isbn)
            else:
                try:
                    res[i] = m[i]['image']
                except KeyError:
                    res[i] = None
        else:
            res[i] = None
    return res
