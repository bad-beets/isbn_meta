#!/usr/bin/env python3

import pytest
import hypothesis
from isbn_meta import isbn_gen


def test_isbn_gen_len() -> None:
    """Checks the length of the value provided by the isbn_gen
    function for the correct length of 13, the only valid length
    for an ISBN-13 according to the specification

    Parameters
    ----------

    Returns
    -------
    None
    """
    assert len(isbn_gen.isbn_gen()) == 13


def test_isbn_gen_ret_type() -> None:
    """Checks the type of the value provided by the isbn_gen
    function for the correct str return type

    Parameters
    ----------

    Returns
    -------
    None
    """
    assert type(isbn_gen.isbn_gen()) == str


def test_isbn_gen_prefix() -> None:
    """Checks the value provided by the isbn_gen
    function for the correct prefix section
    As of 2022, only the prefixes 978- and 979-
    have been assigned

    Parameters
    ----------

    Returns
    -------
    None
    """
    assert isbn_gen.isbn_gen()[0:3] == "978" or "979"


def test_isbn_gen_digits() -> None:
    """Checks the value provided by the isbn_gen
    function to ensure each character in the returned
    string is a digit

    Parameters
    ----------

    Returns
    -------
    None
    """
    for c in isbn_gen.isbn_gen():
        assert c.isdigit


def test_isbn_gen_check_digit() -> None:
    """Checks the last character of the value provided by
    the isbn_gen function (this is called the check digit
    of an ISBN-13) for correctness according to the
    specification. The last digit is calculated based
    on the other fields in the ISBN using a simple
    modular arithmetic formula

    Parameters
    ----------

    Returns
    -------
    None
    """
    res: str = isbn_gen.isbn_gen()
    dutzend: str = res[:-1]
    check: int  = int(res[-1])
    total: int = 0
    for i in range(len(dutzend)):
        if i % 2 == 0:
            total += int(dutzend[i])
        else:
            total += (int(dutzend[i]) * 3)
    total = 10 - (total % 10) if 10 - (total % 10) < 10 else 0
    assert check == total


def test_isbn_mc_len() -> None:
    """Checks the length of the value provided by the isbn_mc
    function for the correct length of 13, the only valid length
    for an ISBN-13 according to the specification

    Parameters
    ----------

    Returns
    -------
    None
    """
    assert len(isbn_gen.isbn_mc()) == 13


def test_isbn_mc_ret_type() -> None:
    """Checks the type of the value provided by the isbn_mc
    function for the correct str return type

    Parameters
    ----------

    Returns
    -------
    None
    """
    assert type(isbn_gen.isbn_mc()) == str


def test_isbn_mc_prefix() -> None:
    """Checks the value provided by the isbn_mc
    function for the correct prefix section
    As of 2022, only the prefixes 978- and 979-
    have been assigned

    Parameters
    ----------

    Returns
    -------
    None
    """
    assert isbn_gen.isbn_mc()[0:3] == "978" or "979"


def test_isbn_mc_digits() -> None:
    """Checks the value provided by the isbn_mc
    function to ensure each character in the returned
    string is a digit

    Parameters
    ----------

    Returns
    -------
    None
    """
    for c in isbn_gen.isbn_mc():
        assert c.isdigit


def test_isbn_mc_check_digit() -> None:
    """Checks the last character of the value provided by
    the isbn_mc function (this is called the check digit
    of an ISBN-13) for correctness according to the
    specification. The last digit is calculated based
    on the other fields in the ISBN using a simple
    modular arithmetic formula

    Parameters
    ----------

    Returns
    -------
    None
    """
    res: str = isbn_gen.isbn_mc()
    dutzend: str = res[:-1]
    check: int = int(res[-1])
    total: int = 0
    for i in range(len(dutzend)):
        if i % 2 == 0:
            total += int(dutzend[i])
        else:
            total += (int(dutzend[i]) * 3)
    total = 10 - (total % 10) if 10 - (total % 10) < 10 else 0
    assert check == total


def test_isbn_known_len() -> None:
    """Checks the length of the value provided by the isbn_known
    function for the correct length of 13, the only valid length
    for an ISBN-13 according to the specification

    Parameters
    ----------

    Returns
    -------
    None
    """
    assert len(isbn_gen.isbn_known()) == 13


def test_isbn_known_ret_type() -> None:
    """Checks the type of the value provided by the isbn_known
    function for the correct str return type

    Parameters
    ----------

    Returns
    -------
    None
    """
    assert type(isbn_gen.isbn_known()) == str


def test_isbn_known_prefix() -> None:
    """Checks the value provided by the isbn_known
    function for the correct prefix section
    As of 2022, only the prefixes 978- and 979-
    have been assigned

    Parameters
    ----------

    Returns
    -------
    None
    """
    assert isbn_gen.isbn_known()[0:3] == "978" or "979"


def test_isbn_known_digits() -> None:
    """Checks the value provided by the isbn_known
    function to ensure each character in the returned
    string is a digit

    Parameters
    ----------

    Returns
    -------
    None
    """
    for c in isbn_gen.isbn_known():
        assert c.isdigit


def test_isbn_known_check_digit() -> None:
    """Checks the last character of the value provided by
    the isbn_known function (this is called the check digit
    of an ISBN-13) for correctness according to the
    specification. The last digit is calculated based
    on the other fields in the ISBN using a simple
    modular arithmetic formula

    Parameters
    ----------

    Returns
    -------
    None
    """
    res: str = isbn_gen.isbn_known()
    dutzend: str = res[:-1]
    check: int = int(res[-1])
    total: int = 0
    for i in range(len(dutzend)):
        if i % 2 == 0:
            total += int(dutzend[i])
        else:
            total += (int(dutzend[i]) * 3)
    total = 10 - (total % 10) if 10 - (total % 10) < 10 else 0
    assert check == total


def test_isbn_bogus_len() -> None:
    """Checks the length of the value provided by the isbn_bogus
    function for the correct length of 13, the only valid length
    for an ISBN-13 according to the specification

    Parameters
    ----------

    Returns
    -------
    None
    """
    assert len(isbn_gen.isbn_bogus()) == 13


def test_isbn_bogus_ret_type() -> None:
    """Checks the type of the value provided by the isbn_bogus
    function for the correct str return type

    Parameters
    ----------

    Returns
    -------
    None
    """
    assert type(isbn_gen.isbn_bogus()) == str


def test_isbn_bogus_prefix() -> None:
    """Checks the value provided by the isbn_bogus
    function for the correct prefix section
    As of 2022, only the prefixes 978- and 979-
    have been assigned

    Parameters
    ----------

    Returns
    -------
    None
    """
    assert isbn_gen.isbn_bogus()[0:3] == "978" or "979"


def test_isbn_bogus_digits() -> None:
    """Checks the value provided by the isbn_bogus
    function to ensure each character in the returned
    string is a digit or "O"

    Parameters
    ----------

    Returns
    -------
    None
    """
    for c in isbn_gen.isbn_bogus():
        assert c.isdigit or c == "O"
