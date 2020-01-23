#!/usr/bin/env python

"""Tests for `clt_py` package."""

import pytest


from clt_py import *
from clt_py.clt_py import *


def test_IsotropicMaterial_NotEnoughArgumentError():
    with pytest.raises(NotEnoughArgumentError):
        assert IsotropicMaterial(rho=1, E=1)
    with pytest.raises(NotEnoughArgumentError):
        assert IsotropicMaterial(rho=1, v=1)
    with pytest.raises(NotEnoughArgumentError):
        assert IsotropicMaterial(rho=1, G=1)
    with pytest.raises(NotEnoughArgumentError):
        assert IsotropicMaterial(rho=1)


def test_IsotropicMaterial_OverDeterminedError():
    with pytest.raises(OverDeterminedError):
        assert IsotropicMaterial(rho=1, G=1, E=1, v=1)


def test_IsotropicMaterial():
    mat_iso = IsotropicMaterial(rho=1, E=10, v=0.25)
    assert mat_iso.G == 4
    mat_iso = IsotropicMaterial(rho=1, E=10, G=4)
    assert mat_iso.v == 0.25
    mat_iso = IsotropicMaterial(rho=1, G=4, v=0.25)
    assert mat_iso.E == 10


def test_AnisotropicMaterial():
    mat_aniso = AnisotropicMaterial(rho=1, v=0.25, E_para=10, E_ortho=2, G=3)
    assert isinstance(mat_aniso, AnisotropicMaterial)


def test_Ply():
    matMat = IsotropicMaterial(rho=1, E=1, v=0.25)
    matFib = AnisotropicMaterial(rho=2, v=0.25, E_para=10, E_ortho=2, G=3)

    ply = Ply(matFib=matFib, matMat=matMat)

    ply.set_fibVolRatio(0.2)
    assert ply.fibVolRatio == 0.2
    ply.set_fibWgRatio(0.4)
    assert ply.fibVolRatio == 0.25


def test_Ply_prismatic_jones_model():
    matMat = IsotropicMaterial(rho=1, E=1, v=0.25)
    matFib = AnisotropicMaterial(rho=2, v=0.25, E_para=10, E_ortho=2, G=3)

    ply = Ply(matFib=matFib, matMat=matMat)
    ply.system = "prismatic_jones"
    ply.update()
    assert ply.E_para == 5.5
    assert round(ply.E_ortho, 3) == 1.333
    assert round(ply.G, 3) == 0.706
    assert ply.v_para_ortho == 0.25
    pass


def test_Ply_hsb_model():
    matMat = IsotropicMaterial(rho=1, E=1, v=0.25)
    matFib = AnisotropicMaterial(rho=2, v=0.25, E_para=10, E_ortho=2, G=3)

    ply = Ply(matFib=matFib, matMat=matMat, kapa=[0.8, 0.8, 0.8])
    Ply.system = "hsb"
    ply.update()
    assert round(ply.E_para, 3) == 4.4
    assert round(ply.E_ortho, 3) == 1.105
    assert round(ply.G, 3) == 0.678
    assert round(ply.v_para_ortho, 3) == 0.25
    assert round(ply.v_ortho_para, 3) == 0.063
    assert round(ply.rho, 3) == 1.5
    pass
