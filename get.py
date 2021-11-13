import metric
import functools
import requests
import load_config
from pathlib import Path
from typing import List, Dict, Optional
from typing import Callable

cfg: dict = load_config.cfg


def key_swallow(f: Callable[[str], dict]) -> Callable[[str], dict]:
    """Wraps an API call function in order to eat KeyErrors

    This is used as a decorator throughout get.py

    Parameters
    ----------
    f : function
        An api call with a given key to be looked up

    Returns
    -------
    function
        An outer function that wraps f with a try/except block
    """

    @functools.wraps(f)
    def attempt(x: str) -> dict:
        try:
            return f(x)
        except KeyError:
            return None
        return None
    return attempt


@key_swallow
def gvol_from_isbn(isbn: str) -> str:
    """Gets a google books volume id from the API using a given ISBN

    Parameters
    ----------
    isbn : str
        The ISBN of the work

    Returns
    -------
    str
        The Google Books Volume ID string, or None if not found
    """

    r: requests.models.Response = requests.get(cfg['gobo']['uri'] + isbn)
    if r.status_code == 200:
        return(r.json()["items"][0]['id'])
    return None


@key_swallow
def gobo_meta(isbn: str) -> dict:
    """Gets the metadata of an ISBN from the Google Books API

    Parameters
    ----------
    isbn : str
        The ISBN of the work

    Returns
    -------
    dict
        The dictionary of metadata from the API, or None
    """

    vol_id: Optional[str] = gvol_from_isbn(isbn)
    if vol_id:
        r: requests.models.Response = requests.get(
            cfg['gobo']['vol_uri'] + vol_id, params=cfg['gobo_params'])
        if r.status_code == 200:
            return r.json()["volumeInfo"]
    return None


@key_swallow
def ol_meta(isbn: str) -> dict:
    """Gets the metadata of an ISBN from the OpenLibrary API

    Parameters
    ----------
    isbn : str
        The ISBN of the work

    Returns
    -------
    dict
        The dictionary of metadata from the API, or None
    """

    r: requests.models.Response = requests.get(
        cfg['ol']['uri'] + isbn, params=cfg['ol_params'])
    if r.status_code == 200:
        return r.json()['ISBN:' + isbn]
    return None


@key_swallow
def isbndb_meta(isbn: str) -> dict:
    """Gets the metadata of an ISBN from the ISBNDB API

    Parameters
    ----------
    isbn : str
        The ISBN of the work

    Returns
    -------
    dict
        The dictionary of metadata from the API, or None
    """

    r: requests.models.Response = requests.get(
        cfg['isbndb']['uri'] + "book/" + isbn,
        headers=cfg['isbndb_headers'])
    if r.status_code == 200:
        return r.json()['book']
    return None


@functools.lru_cache
# cache results using the least recently used algo in functools module
def meta(isbn: str, method: List[Callable[[str], dict]] =
         [gobo_meta, ol_meta, isbndb_meta]) -> dict:
    """Gets the metadata for a given ISBN from various API sources

    Parameters
    ----------
    isbn : str
        The ISBN of the work
    method : list
        A list of functions that implement specific API lookups

    Returns
    -------
    dict
        A dictionary of API names mapped to returned metadata from each
    """

    def prettify(x: Callable[[str], dict]) -> str:
        # get API names from their functions using the closure dunder
        return x.__closure__[0].cell_contents.__name__.split('_')[0]
    m_names: List[str] = list(map(prettify, method))
    meta: List[dict] = [m(isbn) for m in method]
    return {k: v for (k, v) in zip(m_names, meta)}


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

    @key_swallow
    def wrapped(x: dict) -> dict:
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
    function
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

    m: Dict[dict] = meta(isbn)
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

    m: Dict[dict] = meta(isbn)
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


def ol_cover(isbn: str) -> str:
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

    m: Dict[dict] = meta(isbn)
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
