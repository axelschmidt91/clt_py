#!/usr/bin/env python

"""Tests for `clt_py` package."""

import pytest


from clt_py import clt_py
from clt_py.clt_py import *


def test_Material_NotEnoughArgumentError():
    with pytest.raises(NotEnoughArgumentError):
        assert Material(rho=1, E=1)
    with pytest.raises(NotEnoughArgumentError):
        assert Material(rho=1, v=1)
    with pytest.raises(NotEnoughArgumentError):
        assert Material(rho=1, G=1)
    with pytest.raises(NotEnoughArgumentError):
        assert Material(rho=1)


def test_Material_OverDeterminedError():
    with pytest.raises(OverDeterminedError):
        assert Material(rho=1, G=1, E=1, v=1)
    with pytest.raises(OverDeterminedError):
        assert Material(rho=1, G=[4, 1], E=[10, 2])


def test_Material_isotropic():
    mat_iso = Material(rho=1, E=10, v=0.25)
    assert mat_iso.G == 4
    mat_iso = Material(rho=1, E=10, G=4)
    assert mat_iso.v == 0.25
    mat_iso = Material(rho=1, G=4, v=0.25)
    assert mat_iso.E == 10


def test_Material_anisotropic():
    mat_aniso = Material(rho=1, v=0.25, E=[10, 2])
    assert mat_aniso.G == [4, 0.8]
    mat_aniso = Material(rho=1, v=0.25, G=[4, 0.8])
    assert mat_aniso.E == [10, 2]
    mat_aniso = Material(rho=1, G=[4, 0.8], E=[10, 2])
    assert mat_aniso.v == 0.25


def test_Ply():
    matMat = Material(rho=1, E=1, v=0.25)
    matFib = Material(rho=2, E=10, v=0.25)

    ply = Ply(matFib=matFib, matMat=matMat)

    ply.set_fibVolRatio(0.2)
    assert ply.fibVolRatio == 0.2
    ply.set_fibWgRatio(0.4)
    assert ply.fibVolRatio == 0.25
