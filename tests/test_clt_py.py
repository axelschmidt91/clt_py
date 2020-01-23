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
    assert mat_iso.v_para_ortho == 0.25
    mat_iso = IsotropicMaterial(rho=1, G=4, v=0.25)
    assert mat_iso.E_para == 10


def test_AnisotropicMaterial():
    mat_aniso = AnisotropicMaterial(rho=1, v_para_ortho=0.25, E_para=10, E_ortho=2, G=3)
    assert isinstance(mat_aniso, AnisotropicMaterial)


def test_FiberReinforcedMaterialUD():
    matMat = IsotropicMaterial(rho=1, E=1, v=0.25)
    matFib = AnisotropicMaterial(rho=2, v_para_ortho=0.25, E_para=10, E_ortho=2, G=3)

    mat_FRM = FiberReinforcedMaterialUD(matFib=matFib, matMat=matMat)

    mat_FRM.set_fibVolRatio(0.2)
    assert mat_FRM.fibVolRatio == 0.2
    mat_FRM.set_fibWgRatio(0.4)
    assert mat_FRM.fibVolRatio == 0.25

    mat_FRM.set_fibVolRatio(0)
    assert mat_FRM.rho == 1
    mat_FRM.set_fibVolRatio(1)
    assert mat_FRM.rho == 2


def test_FiberReinforcedMaterialUD_prismatic_jones_model():
    matMat = IsotropicMaterial(rho=1, E=1, v=0.25)
    matFib = AnisotropicMaterial(rho=2, v_para_ortho=0.25, E_para=10, E_ortho=2, G=3)

    mat_FRM = FiberReinforcedMaterialUD(matFib=matFib, matMat=matMat)
    mat_FRM.set_system("prismatic_jones")
    assert mat_FRM.E_para == 5.5
    assert round(mat_FRM.E_ortho, 3) == 1.333
    assert round(mat_FRM.G, 3) == 0.706
    assert mat_FRM.v_para_ortho == 0.25
    pass


def test_FiberReinforcedMaterialUD_hsb_model():
    matMat = IsotropicMaterial(rho=1, E=1, v=0.25)
    matFib = AnisotropicMaterial(rho=2, v_para_ortho=0.25, E_para=10, E_ortho=2, G=3)

    mat_FRM = FiberReinforcedMaterialUD(
        matFib=matFib, matMat=matMat, kapa=[0.8, 0.8, 0.8]
    )
    FiberReinforcedMaterialUD.set_system("hsb")
    assert round(mat_FRM.E_para, 3) == 4.4
    assert round(mat_FRM.E_ortho, 3) == 1.105
    assert round(mat_FRM.G, 3) == 0.678
    assert round(mat_FRM.v_para_ortho, 3) == 0.25
    assert round(mat_FRM.v_ortho_para, 3) == 0.063
    assert round(mat_FRM.rho, 3) == 1.5
    pass


def test_FiberReinforcedMaterialUD_nonValid_model():
    matMat = IsotropicMaterial(rho=1, E=1, v=0.25)
    matFib = AnisotropicMaterial(rho=2, v_para_ortho=0.25, E_para=10, E_ortho=2, G=3)

    mat_FRM = FiberReinforcedMaterialUD(
        matFib=matFib, matMat=matMat, kapa=[0.8, 0.8, 0.8]
    )

    with pytest.raises(ValueError):
        assert mat_FRM.set_system("test")


def test_FiberReinforcedMaterialUD_set_matMat():
    matMat = IsotropicMaterial(rho=1, E=1, v=0.25)
    matMat2 = IsotropicMaterial(rho=1, E=1, v=0.25)
    matMat3 = AnisotropicMaterial(rho=2, v_para_ortho=0.25, E_para=10, E_ortho=2, G=3)
    matFib = AnisotropicMaterial(rho=2, v_para_ortho=0.25, E_para=10, E_ortho=2, G=3)

    mat_FRM = FiberReinforcedMaterialUD(
        matFib=matFib, matMat=matMat, kapa=[0.8, 0.8, 0.8]
    )

    mat_FRM.set_matMat(matMat2)
    assert round(mat_FRM.E_para, 3) == 4.4

    with pytest.raises(Material2D.NotIsotropicError):
        assert mat_FRM.set_matMat(matMat3)


def test_FiberReinforcedMaterialUD_set_matFib():
    matMat = IsotropicMaterial(rho=1, E=1, v=0.25)
    matFib = AnisotropicMaterial(rho=2, v_para_ortho=0.25, E_para=10, E_ortho=2, G=3)
    matFib2 = AnisotropicMaterial(rho=2, v_para_ortho=0.25, E_para=10, E_ortho=2, G=3)
    matFib3 = IsotropicMaterial(rho=1, E=1, v=0.25)

    mat_FRM = FiberReinforcedMaterialUD(
        matFib=matFib, matMat=matMat, kapa=[0.8, 0.8, 0.8]
    )

    mat_FRM.set_matFib(matFib2)
    assert round(mat_FRM.E_para, 3) == 4.4

    with pytest.raises(Material2D.NotAnisotropicError):
        assert mat_FRM.set_matFib(matFib3)


def test_Ply_init():
    matMat = IsotropicMaterial(rho=1, E=1, v=0.25)
    matFib = AnisotropicMaterial(rho=2, v_para_ortho=0.25, E_para=10, E_ortho=2, G=3)

    mat_FRM = FiberReinforcedMaterialUD(matFib=matFib, matMat=matMat)

    with pytest.raises(TypeError):
        assert Ply(matFib)

    ply = Ply(mat_FRM)


def test_Ply_rotationStressMatrix():
    matMat = IsotropicMaterial(rho=1, E=1, v=0.25)
    matFib = AnisotropicMaterial(rho=2, v_para_ortho=0.25, E_para=10, E_ortho=2, G=3)

    mat_FRM = FiberReinforcedMaterialUD(matFib=matFib, matMat=matMat)

    ply0 = Ply(mat_FRM)
    ply90 = Ply(mat_FRM, rotation=90)
    ply45 = Ply(mat_FRM, rotation=45)

    # 90° rotation:
    assert round(ply0.Q[0, 0], 5) == round(ply90.Q[1, 1], 5)
    assert round(ply0.Q[1, 1], 5) == round(ply90.Q[0, 0], 5)
    assert round(ply0.Q[2, 2], 5) == round(ply90.Q[2, 2], 5)
    assert round(ply0.Q[0, 1], 5) == round(ply90.Q[0, 1], 5)
    assert round(ply0.Q[1, 0], 5) == round(ply90.Q[1, 0], 5)

    assert round(ply0.S[0, 0], 5) == round(ply90.S[1, 1], 5)
    assert round(ply0.S[1, 1], 5) == round(ply90.S[0, 0], 5)
    assert round(ply0.S[2, 2], 5) == round(ply90.S[2, 2], 5)
    assert round(ply0.S[0, 1], 5) == round(ply90.S[0, 1], 5)
    assert round(ply0.S[1, 0], 5) == round(ply90.S[1, 0], 5)

    # 45° rotation:
    assert round(ply45.Q[0, 0], 5) == round(
        (0.25 * (ply0.Q[0, 0] + ply0.Q[1, 1]) + 0.5 * ply0.Q[0, 1] + ply0.Q[2, 2]), 5
    )
    assert round(ply45.Q[1, 1], 5) == round(
        (0.25 * (ply0.Q[0, 0] + ply0.Q[1, 1]) + 0.5 * ply0.Q[0, 1] + ply0.Q[2, 2]), 5
    )
    assert round(ply45.Q[0, 1], 5) == round(
        (0.25 * (ply0.Q[0, 0] + ply0.Q[1, 1]) + 0.5 * ply0.Q[0, 1] - ply0.Q[2, 2]), 5
    )
    assert round(ply45.Q[2, 2], 5) == round(
        (0.25 * (ply0.Q[0, 0] + ply0.Q[1, 1]) - 0.5 * ply0.Q[0, 1]), 5
    )
    assert round(ply45.Q[0, 2], 5) == 0
    assert round(ply45.Q[1, 2], 5) == 0
    assert round(ply45.Q[2, 0], 5) == 0
    assert round(ply45.Q[2, 1], 5) == 0

    assert round(ply45.S[0, 0], 5) == round(
        (
            0.25 * (ply0.S[0, 0] + ply0.S[1, 1])
            + 0.5 * ply0.S[0, 1]
            + 0.25 * ply0.S[2, 2]
        ),
        5,
    )
    assert round(ply45.S[1, 1], 5) == round(
        (
            0.25 * (ply0.S[0, 0] + ply0.S[1, 1])
            + 0.5 * ply0.S[0, 1]
            + 0.25 * ply0.S[2, 2]
        ),
        5,
    )
    assert round(ply45.S[0, 1], 5) == round(
        (0.5 * ply0.S[0, 1] + 0.25 * (ply0.S[0, 0] + ply0.S[1, 1] - ply0.S[2, 2])), 5
    )
    assert round(ply45.S[2, 2], 5) == round(
        ((ply0.S[0, 0] + ply0.S[1, 1]) - 2 * ply0.S[0, 1]), 5
    )
    assert round(ply45.S[0, 2], 5) == 0
    assert round(ply45.S[1, 2], 5) == 0
    assert round(ply45.S[2, 0], 5) == 0
    assert round(ply45.S[2, 1], 5) == 0
