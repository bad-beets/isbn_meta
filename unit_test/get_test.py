#!/usr/bin/env python3

import pytest
import hypothesis
import requests
import pandas as pd
import isbn_gen
import get
from typing import Optional


def test_key_swallow_return_none() -> None:
    """Checks the value returned by the key_swallow
    function to ensure that None is returned on KeyError
    dictionary lookups

    Parameters
    ----------

    Returns
    -------
    None
    """
    test_dict_inner_eins: dict = {"double": "double", "toil": "and trouble"}
    test_dict_inner_zwei: dict = {"fire": "burn", "and": "cauldron bubble"}
    test_dict_outer: dict = {"lorem": test_dict_inner_eins,
                             "ipsum": test_dict_inner_zwei}

    with requests.Session() as s:
        @get.key_swallow
        def inner(x: str,
                  y: Optional[requests.sessions.Session]) -> Optional[dict]:
            return test_dict_outer[x]
        assert inner("dolor sit amet", s) is None


def test_key_swallow_return_some() -> None:
    """Checks the value returned by the key_swallow
    function to ensure that the expected value is returned
    by the wrapped function when there is no KeyError

    Parameters
    ----------

    Returns
    -------
    None
    """
    test_dict_inner_eins: dict = {"double": "double", "toil": "and trouble"}
    test_dict_inner_zwei: dict = {"fire": "burn", "and": "cauldron bubble"}
    test_dict_outer: dict = {"lorem": test_dict_inner_eins,
                             "ipsum": test_dict_inner_zwei}

    with requests.Session() as s:
        @get.key_swallow
        def inner(x: str,
                  y: Optional[requests.sessions.Session]) -> Optional[dict]:
            return test_dict_outer[x]
        assert inner("lorem", s) is test_dict_inner_eins
        assert inner("ipsum", s) is test_dict_inner_zwei


def test_key_swallow_return_error() -> None:
    """Checks the error returned by the key_swallow
    function to ensure that errors other than KeyError
    are propagated correctly from dictionary lookups
    in the inner function

    Parameters
    ----------

    Returns
    -------
    None
    """
    test_dict_inner_eins: dict = {"double": "double", "toil": "and trouble"}
    test_dict_inner_zwei: dict = {"fire": "burn", "and": "cauldron bubble"}
    test_dict_outer: dict = {"lorem": test_dict_inner_eins,
                             "ipsum": test_dict_inner_zwei}

    with requests.Session() as s:
        @get.key_swallow
        def inner(x: str,
                  y: Optional[requests.sessions.Session]) -> Optional[dict]:
            a: int = 0
            b: int = 10 / a
            b: int = 0
            return test_dict_outer[x[b] + x[1:]]
        with pytest.raises(ZeroDivisionError):
            assert inner("lorem", s) is test_dict_inner_eins


def test_yarn_swallow_return_none() -> None:
    """Checks the value returned by the yarn_swallow
    function to ensure that None is returned on KeyError
    dictionary lookups

    Parameters
    ----------

    Returns
    -------
    None
    """
    inner_eins: str = "Superiora de inferioribus, inferiora de superioribus,"
    inner_zwei: str = "prodigiorum operatio ex uno, quemadmodum omnia ex"
    inner_drei: str = "uno eodemque ducunt originem,"
    inner_vier: str = "una eademque consilii administratione."
    test_dict_outer: dict = {"lorem": inner_eins,
                             "ipsum": inner_zwei,
                             "dolor": inner_drei,
                             "sit": inner_vier}

    with requests.Session() as s:
        @get.yarn_swallow
        def inner(x: str,
                  y: Optional[requests.sessions.Session]) -> Optional[str]:
            return test_dict_outer[x]
        assert inner("dolor sit amet", s) is None


def test_yarn_swallow_return_some() -> None:
    """Checks the value returned by the yarn_swallow
    function to ensure that the expected value is returned
    by the wrapped function when there is no KeyError

    Parameters
    ----------

    Returns
    -------
    None
    """
    inner_eins: str = "Superiora de inferioribus, inferiora de superioribus,"
    inner_zwei: str = "prodigiorum operatio ex uno, quemadmodum omnia ex"
    inner_drei: str = "uno eodemque ducunt originem,"
    inner_vier: str = "una eademque consilii administratione."
    test_dict_outer: dict = {"lorem": inner_eins,
                             "ipsum": inner_zwei,
                             "dolor": inner_drei,
                             "sit": inner_vier}

    with requests.Session() as s:
        @get.yarn_swallow
        def inner(x: str,
                  y: Optional[requests.sessions.Session]) -> Optional[str]:
            return test_dict_outer[x]
        assert inner("lorem", s) is inner_eins
        assert inner("ipsum", s) is inner_zwei
        assert inner("dolor", s) is inner_drei
        assert inner("sit", s) is inner_vier


def test_yarn_swallow_return_error() -> None:
    """Checks the error returned by the yarn_swallow
    function to ensure that errors other than KeyError
    are propagated correctly from dictionary lookups
    in the inner function

    Parameters
    ----------

    Returns
    -------
    None
    """
    inner_eins: str = "Superiora de inferioribus, inferiora de superioribus,"
    inner_zwei: str = "prodigiorum operatio ex uno, quemadmodum omnia ex"
    inner_drei: str = "uno eodemque ducunt originem,"
    inner_vier: str = "una eademque consilii administratione."
    test_dict_outer: dict = {"lorem": inner_eins,
                             "ipsum": inner_zwei,
                             "dolor": inner_drei,
                             "sit": inner_vier}

    with requests.Session() as s:
        @get.yarn_swallow
        def inner(x: str,
                  y: Optional[requests.sessions.Session]) -> Optional[str]:
            a: int = 0
            b: int = 10 / a
            b: int = 0
            return test_dict_outer[x[b] + x[1:]]
        with pytest.raises(ZeroDivisionError):
            assert inner("lorem", s) is inner_eins
            assert inner("ipsum", s) is inner_zwei
            assert inner("dolor", s) is inner_drei
            assert inner("sit", s) is inner_vier


def test_map_swallow_return_none() -> None:
    """Checks the value returned by the map_swallow
    function to ensure that None is returned on KeyError
    dictionary lookups

    Parameters
    ----------

    Returns
    -------
    None
    """
    inner_eins: str = "be ever thus that men speak not of"
    inner_zwei: str = "Thee as One but as None and let"
    inner_drei: str = "them speak not of thee at all since"
    inner_vier: str = "thou art continuous."
    test_outer_un: dict = {"lorem": inner_eins,
                           "ipsum": inner_zwei,
                           "dolor": inner_drei,
                           "sit": inner_vier}
    test_outer_deux: dict = {"A.A": test_outer_un}
    test_outer_trois: dict = {"vvvVvvVvVv": test_outer_deux}

    @get.map_swallow
    def inner(k: dict) -> Optional[dict]:
        if k is test_outer_un:
            return test_outer_un
        elif k is test_outer_deux:
            return k["mephisto"]
        else:
            return k["A.A"]
    assert inner(test_outer_trois) is None
    assert inner(test_outer_deux) is None


def test_map_swallow_return_some() -> None:
    """Checks the value returned by the map_swallow
    function to ensure that the expected value is returned
    by the wrapped function when there is no KeyError

    Parameters
    ----------

    Returns
    -------
    None
    """
    inner_eins: str = "be ever thus that men speak not of"
    inner_zwei: str = "Thee as One but as None and let"
    inner_drei: str = "them speak not of thee at all since"
    inner_vier: str = "thou art continuous."
    test_outer_un: dict = {"lorem": inner_eins,
                           "ipsum": inner_zwei,
                           "dolor": inner_drei,
                           "sit": inner_vier}
    test_outer_deux: dict = {"A.A": test_outer_un}
    test_outer_trois: dict = {"vvvVvvVvVv": test_outer_deux}

    @get.map_swallow
    def inner(k: dict) -> Optional[dict]:
        if k is test_outer_un:
            return test_outer_deux
        elif k is test_outer_deux:
            return k["A.A"]
        else:
            return k
    assert inner(test_outer_un) is test_outer_deux
    assert inner(test_outer_deux) is test_outer_un
    assert inner(test_outer_trois) is test_outer_trois


def test_map_swallow_return_error() -> None:
    """Checks the error returned by the map_swallow
    function to ensure that errors other than KeyError
    are propagated correctly from dictionary lookups
    in the inner function

    Parameters
    ----------

    Returns
    -------
    None
    """
    inner_eins: str = "be ever thus that men speak not of"
    inner_zwei: str = "Thee as One but as None and let"
    inner_drei: str = "them speak not of thee at all since"
    inner_vier: str = "thou art continuous."
    test_outer_un: dict = {"lorem": inner_eins,
                           "ipsum": inner_zwei,
                           "dolor": inner_drei,
                           "sit": inner_vier}
    test_outer_deux: dict = {"A.A": test_outer_un}
    test_outer_trois: dict = {"vvvVvvVvVv": test_outer_deux}

    @get.map_swallow
    def inner(k: dict) -> Optional[dict]:
        if 10 / 0:
            pass
        elif k is test_outer_un:
            return test_outer_deux
        elif k is test_outer_deux:
            return k["A.A"]
        else:
            return k
    with pytest.raises(ZeroDivisionError):
        assert inner(test_outer_un) is test_outer_deux
        assert inner(test_outer_deux) is test_outer_un
        assert inner(test_outer_trois) is test_outer_trois


def test_csv_meta_dims() -> None:
    """Checks that the returned Pandas DataFrame from the
    csv_meta function has the appropriate dimensions

    Parameters
    ----------

    Returns
    -------
    None
    """
    m: Optional[pd.core.frame.DataFrame] = get.csv_meta('9780711246812',
                                                        'unit_test/test.csv')
    assert len(list(m.columns)) == 11
    assert len(m) == 1


def test_csv_meta_columns() -> None:
    """Checks that the returned Pandas DataFrame from the
    csv_meta function has the appropriate columns

    Parameters
    ----------

    Returns
    -------
    None
    """
    m: Optional[pd.core.frame.DataFrame] = get.csv_meta('9780711246812',
                                                        'unit_test/test.csv')
    assert list(m.columns) == ['product_isbn',
                               'product_title',
                               'format',
                               'product_description',
                               'product_retail',
                               'publisher',
                               'product_weight',
                               'product_width',
                               'product_height',
                               'product_thickness',
                               'Author']


def test_csv_meta_bad_isbn() -> None:
    """Checks that the returned value from the
    csv_meta function is None when a lookup fails
    is an empty dataframe

    Parameters
    ----------

    Returns
    -------
    None
    """
    m: Optional[pd.core.frame.DataFrame] = get.csv_meta('9780716247812',
                                                        'unit_test/test.csv')
    assert m.empty


def test_csv_meta_error() -> None:
    """Checks that the csv_meta function propagates errors
    in an expected way

    Parameters
    ----------

    Returns
    -------
    None
    """
    with pytest.raises(TypeError):
        assert get.csv_meta(lambda x: x, 'unit_test/test.csv') is None


# def test_sqlite_meta_dims() -> None:
#     """Checks that the returned Pandas DataFrame from the
#     sqlite_meta function has the appropriate dimensions

#     Parameters
#     ----------

#     Returns
#     -------
#     None
#     """
#     m: Optional[pd.core.frame.DataFrame] = get.sqlite_meta('9780711246812')
#     assert len(list(m.columns)) == 11
#     assert len(m) == 1


# def test_sqlite_meta_columns() -> None:
#     """Checks that the returned Pandas DataFrame from the
#     sqlite_meta function has the appropriate columns

#     Parameters
#     ----------

#     Returns
#     -------
#     None
#     """
#     m: Optional[pd.core.frame.DataFrame] = get.csv_meta('9780711246812',
#                                                         'unit_test/test.csv')
#     assert list(m.columns) == ['product_isbn',
#                                'product_title',
#                                'format',
#                                'product_description',
#                                'product_retail',
#                                'publisher',
#                                'product_weight',
#                                'product_width',
#                                'product_height',
#                                'product_thickness',
#                                'Author']


# def test_sqlite_meta_bad_isbn() -> None:
#     """Checks that the returned value from the
#     sqlite_meta function is None when a lookup fails
#     is an empty dataframe

#     Parameters
#     ----------

#     Returns
#     -------
#     None
#     """
#     m: Optional[pd.core.frame.DataFrame] = get.csv_meta('9780716247812',
#                                                         'unit_test/test.csv')
#     assert m.empty


# def test_sqlite_meta_error() -> None:
#     """Checks that the csv_meta function propagates errors
#     other than KeyError in an expected way

#     Parameters
#     ----------

#     Returns
#     -------
#     None
#     """
#     with pytest.raises(TypeError):
#         assert get.csv_meta(lambda x: x, 'unit_test/test.csv') is None


# def test_mariadb_meta_dims() -> None:
#     """Checks that the returned Pandas DataFrame from the
#     mariadb_meta function has the appropriate dimensions

#     Parameters
#     ----------

#     Returns
#     -------
#     None
#     """
#     m: Optional[pd.core.frame.DataFrame] = get.csv_meta('9780711246812',
#                                                         'unit_test/test.csv')
#     assert len(list(m.columns)) == 11
#     assert len(m) == 1


# def test_mariadb_meta_columns() -> None:
#     """Checks that the returned Pandas DataFrame from the
#     mariadb_meta function has the appropriate columns

#     Parameters
#     ----------

#     Returns
#     -------
#     None
#     """
#     m: Optional[pd.core.frame.DataFrame] = get.csv_meta('9780711246812',
#                                                         'unit_test/test.csv')
#     assert list(m.columns) == ['product_isbn',
#                                'product_title',
#                                'format',
#                                'product_description',
#                                'product_retail',
#                                'publisher',
#                                'product_weight',
#                                'product_width',
#                                'product_height',
#                                'product_thickness',
#                                'Author']


# def test_mariadb_meta_bad_isbn() -> None:
#     """Checks that the returned value from the
#     mariadb_meta function is None when a lookup fails
#     is an empty dataframe

#     Parameters
#     ----------

#     Returns
#     -------
#     None
#     """
#     m: Optional[pd.core.frame.DataFrame] = get.csv_meta('9780716247812',
#                                                         'unit_test/test.csv')
#     assert m.empty


# def test_mariadb_meta_error() -> None:
#     """Checks that the mariadb_meta function propagates errors
#     other than KeyError in an expected way

#     Parameters
#     ----------

#     Returns
#     -------
#     None
#     """
#     with pytest.raises(TypeError):
#         assert get.csv_meta(lambda x: x, 'unit_test/test.csv') is None


# def test_df_meta_dims() -> None:
#     """Checks that the returned Pandas DataFrame from the
#     df_meta function has the appropriate dimensions

#     Parameters
#     ----------

#     Returns
#     -------
#     None
#     """
#     m: Optional[pd.core.frame.DataFrame] = get.csv_meta('9780711246812',
#                                                         'unit_test/test.csv')
#     assert len(list(m.columns)) == 11
#     assert len(m) == 1


# def test_df_meta_columns() -> None:
#     """Checks that the returned Pandas DataFrame from the
#     df_meta function has the appropriate columns

#     Parameters
#     ----------

#     Returns
#     -------
#     None
#     """
#     m: Optional[pd.core.frame.DataFrame] = get.csv_meta('9780711246812',
#                                                         'unit_test/test.csv')
#     assert list(m.columns) == ['product_isbn',
#                                'product_title',
#                                'format',
#                                'product_description',
#                                'product_retail',
#                                'publisher',
#                                'product_weight',
#                                'product_width',
#                                'product_height',
#                                'product_thickness',
#                                'Author']


# def test_df_meta_bad_isbn() -> None:
#     """Checks that the returned value from the
#     df_meta function is None when a lookup fails
#     is an empty dataframe

#     Parameters
#     ----------

#     Returns
#     -------
#     None
#     """
#     m: Optional[pd.core.frame.DataFrame] = get.csv_meta('9780716247812',
#                                                         'unit_test/test.csv')
#     assert m.empty


# def test_df_meta_error() -> None:
#     """Checks that the df_meta function propagates errors
#     other than KeyError in an expected way

#     Parameters
#     ----------

#     Returns
#     -------
#     None
#     """
#     with pytest.raises(TypeError):
#         assert get.csv_meta(lambda x: x, 'unit_test/test.csv') is None


def test_gvol_from_isbn_bad_isbn() -> None:
    """Checks that the returned value from the
    gvol_from_isbn function is None when it is
    passed a bogus ISBN

    Parameters
    ----------

    Returns
    -------
    None
    """
    with requests.Session() as s:
        assert get.gvol_from_isbn(isbn_gen.isbn_bogus(), s) is None


def test_gvol_from_isbn_known_isbn() -> None:
    """Checks that the returned value from the
    gvol_from_isbn function is the expected
    google volume ID when passed known valid ISBNs
    This is achieved by checking the ISBN field of
    the returned google volume ID json data, from
    the gobo_meta function, against the
    randomly generated known ISBN for an exact match and
    by then checking the link in the volumeInfo against
    the google volume ID returned from gvol_from_isbn.
    There is some circularity here, since gobo_meta calls
    gvol_from_isbn in its definition, but this at least
    ensures correspondence between the ISBN and google
    volume ID is the same as what google books reports
    through the API

    Parameters
    ----------

    Returns
    -------
    None
    """
    with requests.Session() as s:
        for i in range(5):
            isbn: str = isbn_gen.isbn_known()
            gobo: Optional[dict] = get.gobo_meta(isbn, s)
            if not gobo:
                continue
            ident: list = gobo['industryIdentifiers']
            vol: str = gobo['canonicalVolumeLink'][-12:]
            for i in ident:
                if 'ISBN_13' in i.values():
                    isbn_cloudy: str = i['identifier']
            assert isbn == isbn_cloudy
            assert get.gvol_from_isbn(isbn, s) == vol


def test_gobo_meta_bad_isbn() -> None:
    """Checks that a bogus isbn passed to the
    gobo_meta function returns None

    Parameters
    ----------

    Returns
    -------
    None
    """
    assert get.gobo_meta(isbn_gen.isbn_bogus()) is None


def test_gobo_meta_error() -> None:
    """Checks that errors other than KeyError are
    propagated correctly

    Parameters
    ----------

    Returns
    -------
    None
    """
    with pytest.raises(TypeError):
        assert get.gobo_meta(lambda x: x) is None


def test_ol_meta_bad_isbn() -> None:
    """Checks that ol_meta functions returns
    None on KeyError, for instance when
    passed a bogus isbn or the title in not
    found

    Parameters
    ----------

    Returns
    -------
    None
    """
    assert get.ol_meta(isbn_gen.isbn_bogus()) is None


def test_ol_meta_error() -> None:
    """Checks that errors other than KeyError are
    propagated correctly

    Parameters
    ----------

    Returns
    -------
    None
    """
    with pytest.raises(TypeError):
        assert get.ol_meta(lambda x: x) is None


def test_isbndb_meta_bad_isbn() -> None:
    """Checks that isbndb_meta function returns
    None on KeyError, for instance when
    passed a bogus isbn or the title in not
    found

    Parameters
    ----------

    Returns
    -------
    None
    """
    assert get.isbndb_meta(isbn_gen.isbn_bogus()) is None


def test_isbndb_meta_error() -> None:
    """Checks that errors other than KeyError are
    propagated correctly

    Parameters
    ----------

    Returns
    -------
    None
    """
    with pytest.raises(TypeError):
        assert get.isbndb_meta(lambda x: x) is None
