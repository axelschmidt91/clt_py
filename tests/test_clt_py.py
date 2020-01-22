#!/usr/bin/env python

"""Tests for `clt_py` package."""

import pytest


from clt_py import clt_py


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    import requests
    return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_add():
    assert clt_py.add(1, 2) == 3
