import metric
import functools
import requests
import load_config

cfg = load_config.cfg


def key_swallow(f):
    def attempt(x):
        try:
            return f(x)
        except KeyError:
            return None
        return None
    return attempt


@key_swallow
def gvol_from_isbn(isbn):
    r = requests.get(cfg['gobo']['uri'] + isbn)
    if r.status_code == 200:
        return(r.json()["items"][0]['id'])
    return None


@key_swallow
def gobo_meta(isbn):
    vol_id = gvol_from_isbn(isbn)
    if vol_id:
        r = requests.get(cfg['gobo']['vol_uri'] + vol_id,
                         params=cfg['gobo_params'])
        if r.status_code == 200:
            return r.json()["volumeInfo"]
    return None


@key_swallow
def ol_meta(isbn):
    r = requests.get(cfg['ol']['uri'] + isbn, params=cfg['ol_params'])
    if r.status_code == 200:
        return r.json()['ISBN:' + isbn]
    return None


@key_swallow
def isbndb_meta(isbn):
    r = requests.get(cfg['isbndb']['uri'] + "book/" + isbn,
                     headers=cfg['isbndb_headers'])
    if r.status_code == 200:
        return r.json()['book']
    return None


@functools.lru_cache
def meta(isbn, method=[gobo_meta, ol_meta, isbndb_meta]):
    def prettify(x):
        return x.__closure__[0].cell_contents.__name__.split('_')[0]
    m_names = list(map(prettify, method))
    meta = [m(isbn) for m in method]
    return {k: v for (k, v) in zip(m_names, meta)}


def field(f, isbn):
    m = meta(isbn)

    @key_swallow
    def wrapped(x):
        return x[f]
    return {k + '_' + f: wrapped(v) for (k, v) in m.items() if v}


def gf_partial(f):
    return functools.partial(field, f)


title = gf_partial("title")
subtitle = gf_partial("subtitle")
authors = gf_partial("authors")
published_date = gf_partial("publishedDate")
description = gf_partial("description")
industry_identifiers = gf_partial("industryIdentifiers")
page_count = gf_partial("printedPageCount")
msrp = gf_partial("msrp")
binding = gf_partial("binding")


def publisher(isbn):
    m = meta(isbn)
    res = {}
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


def dimensions(isbn):
    m = meta(isbn)
    res = {}
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
def width(isbn):
    res = dimensions(isbn)
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
def height(isbn):
    res = dimensions(isbn)
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
def thickness(isbn):
    res = dimensions(isbn)
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
def weight(isbn):
    res = dimensions(isbn)
    if res['isbndb']:
        res['isbndb'] = res['isbndb'].split(',')[2].split(':')[1][1:]
    return {'isbndb': res['isbndb']}


def ol_cover(isbn):
    url = cfg['ol']['covers_uri'] + isbn + cfg['ol']['covers_suffix']
    r = requests.get(url)
    if r.status_code == 200:
        return url
    else:
        return None


def image_url(isbn):
    m = meta(isbn)
    res = {}
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
