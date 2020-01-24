#!/usr/bin/env python

"""Tests for `clt_py` package."""

import pytest


from clt_py import *
from clt_py.clt_py import *

from math import log10, floor


def round_sig(x, sig=2):
    return round(x, sig - int(floor(log10(abs(x)))))


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
    assert round(ply0.Q[1, 2], 5) == 0
    assert round(ply0.Q[0, 2], 5) == 0

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
    assert round(ply45.Q[1, 2], 5) == round(0.25 * (ply0.Q[1, 1] - ply0.Q[0, 0]), 5)
    assert round(ply45.Q[0, 2], 5) == round(0.25 * (ply0.Q[1, 1] - ply0.Q[0, 0]), 5)
    assert round(ply45.Q[2, 0], 5) == round(0.25 * (ply0.Q[1, 1] - ply0.Q[0, 0]), 5)
    assert round(ply45.Q[2, 1], 5) == round(0.25 * (ply0.Q[1, 1] - ply0.Q[0, 0]), 5)

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
    assert round(ply45.S[0, 2], 5) == round(0.5 * (ply0.S[1, 1] - ply0.S[0, 0]), 5)
    assert round(ply45.S[1, 2], 5) == round(0.5 * (ply0.S[1, 1] - ply0.S[0, 0]), 5)
    assert round(ply45.S[2, 0], 5) == round(0.5 * (ply0.S[1, 1] - ply0.S[0, 0]), 5)
    assert round(ply45.S[2, 1], 5) == round(0.5 * (ply0.S[1, 1] - ply0.S[0, 0]), 5)


def test_Ply_real_problem():
    # Carbon fiber: T300
    fiber_rho = 1.74e3
    fiber_E_para = 2.2e5
    fiber_E_ortho = 2.8e4
    fiber_G = 5e4
    fiber_v_para_ortho = 2.3e-1

    # Epoxyd matrix:
    matrix_rho = 1.32e3
    matrix_E = 3.65e3
    matrix_v = 3e-1

    mat_Epoxy = IsotropicMaterial(matrix_rho, E=matrix_E, v=matrix_v, label="Epoxy")
    mat_CFiber = AnisotropicMaterial(
        fiber_rho,
        fiber_E_para,
        fiber_E_ortho,
        fiber_G,
        fiber_v_para_ortho,
        label="C-Fiber T300",
    )

    FiberReinforcedMaterialUD.set_system("prismatic_jones")

    crp = FiberReinforcedMaterialUD(mat_CFiber, mat_Epoxy, label="CRP")
    crp.set_fibWgRatio(0.665)

    assert round_sig(crp.E_para, sig=3) == 1.337e5
    assert round_sig(crp.E_ortho, sig=3) == 7.646e3
    assert round_sig(crp.G, sig=3) == 3.375e3
    assert round_sig(crp.v_para_ortho, sig=2) == 2.58e-1
    assert round_sig(crp.v_ortho_para, sig=2) == 1.48e-2

    ply = Ply(crp, rotation=45)
    assert round_sig(ply.G, sig=3) == 7.036e3
    assert round_sig(ply.E_1, sig=3) == 9.287e3


def test_Laminate_add():
    matMat = IsotropicMaterial(rho=1, E=1, v=0.25)
    matFib = AnisotropicMaterial(rho=2, v_para_ortho=0.25, E_para=10, E_ortho=2, G=3)

    mat_FRM = FiberReinforcedMaterialUD(matFib=matFib, matMat=matMat)

    ply0 = Ply(mat_FRM)
    ply90 = Ply(mat_FRM, rotation=90)
    ply45 = Ply(mat_FRM, rotation=45)
    plyCore = Ply(matMat, thickness=5)

    laminate = Laminate()
    laminate.addPly(ply0)
    laminate.addPly(ply90)
    laminate.addPly(ply45)
    laminate.addCore(plyCore)

    assert isinstance(laminate, Laminate)


def test_Laminate_stiffnessMatrix_classic_orthotrop():
    matMat = IsotropicMaterial(rho=1, E=1, v=0.25)
    matFib = AnisotropicMaterial(rho=2, v_para_ortho=0.25, E_para=10, E_ortho=2, G=3)

    mat_FRM = FiberReinforcedMaterialUD(matFib=matFib, matMat=matMat)

    ply0 = Ply(mat_FRM, rotation=0, thickness=1)
    ply90 = Ply(mat_FRM, rotation=90, thickness=1)

    laminate = Laminate()
    laminate.addPly(ply0)
    laminate.addPly(ply90)
    laminate.addPly(ply0)

    # assert preprocessing
    np.set_printoptions(precision=3, suppress=True)
    print(laminate.get_stiffnessMatrix())

    compare_matrix = np.zeros((6, 6))
    compare_matrix[0:2, 0:2] = 1
    compare_matrix[2:3, 2:3] = 1
    compare_matrix[3:5, 3:5] = 1
    compare_matrix[5:6, 5:6] = 1
    print(compare_matrix)

    (bx, by) = np.nonzero(np.round(laminate.get_stiffnessMatrix(), 3))
    lam_matrix = np.zeros(laminate.get_stiffnessMatrix().shape)
    for x, y in zip(bx, by):
        lam_matrix[x, y] = 1

    assert np.array_equal(lam_matrix, compare_matrix)


def test_Laminate_stiffnessMatrix_general_anisotrop():
    matMat = IsotropicMaterial(rho=1, E=1, v=0.25)
    matFib = AnisotropicMaterial(rho=2, v_para_ortho=0.25, E_para=10, E_ortho=2, G=3)

    mat_FRM = FiberReinforcedMaterialUD(matFib=matFib, matMat=matMat)

    plyP45 = Ply(mat_FRM, rotation=45, thickness=1)
    plyN45 = Ply(mat_FRM, rotation=-45, thickness=1)

    laminate = Laminate()
    laminate.addPly(plyP45)
    laminate.addPly(plyN45)
    laminate.addPly(plyP45)

    # assert preprocessing
    np.set_printoptions(precision=3, suppress=True)
    print(laminate.get_stiffnessMatrix())

    compare_matrix = np.zeros((6, 6))
    compare_matrix[0:3, 0:3] = 1
    compare_matrix[3:6, 3:6] = 1
    print(compare_matrix)

    (bx, by) = np.nonzero(np.round(laminate.get_stiffnessMatrix(), 3))
    lam_matrix = np.zeros(laminate.get_stiffnessMatrix().shape)
    for x, y in zip(bx, by):
        lam_matrix[x, y] = 1

    assert np.array_equal(lam_matrix, compare_matrix)


def test_Laminate_stiffnessMatrix_orthotrop_as_disc():
    matMat = IsotropicMaterial(rho=1, E=1, v=0.25)
    matFib = AnisotropicMaterial(rho=2, v_para_ortho=0.25, E_para=10, E_ortho=2, G=3)

    mat_FRM = FiberReinforcedMaterialUD(matFib=matFib, matMat=matMat)

    plyP45 = Ply(mat_FRM, rotation=45, thickness=1)
    plyN45 = Ply(mat_FRM, rotation=-45, thickness=2)

    laminate = Laminate()
    laminate.addPly(plyP45)
    laminate.addPly(plyN45)
    laminate.addPly(plyP45)

    # assert preprocessing
    np.set_printoptions(precision=3, suppress=True)
    print(laminate.get_stiffnessMatrix())

    compare_matrix = np.zeros((6, 6))
    compare_matrix[0:2, 0:2] = 1
    compare_matrix[2:3, 2:3] = 1
    compare_matrix[3:6, 3:6] = 1
    print(compare_matrix)

    (bx, by) = np.nonzero(np.round(laminate.get_stiffnessMatrix(), 3))
    lam_matrix = np.zeros(laminate.get_stiffnessMatrix().shape)
    for x, y in zip(bx, by):
        lam_matrix[x, y] = 1

    assert np.array_equal(lam_matrix, compare_matrix)


def test_Laminate_stiffnessMatrix_exzentric_orthotrop():
    matMat = IsotropicMaterial(rho=1, E=1, v=0.25)
    matFib = AnisotropicMaterial(rho=2, v_para_ortho=0.25, E_para=10, E_ortho=2, G=3)

    mat_FRM = FiberReinforcedMaterialUD(matFib=matFib, matMat=matMat)

    ply0 = Ply(mat_FRM, rotation=0, thickness=1)
    ply90 = Ply(mat_FRM, rotation=90, thickness=2)

    laminate = Laminate()
    laminate.addPly(ply0)
    laminate.addPly(ply90)

    print(ply0.Q)
    print(ply90.Q)
    # assert preprocessing
    np.set_printoptions(precision=3, suppress=True)
    print(laminate.get_stiffnessMatrix())

    compare_matrix = np.zeros((6, 6))
    compare_matrix[0:2, 0:2] = 1
    compare_matrix[2:3, 2:3] = 1
    compare_matrix[3:5, 3:5] = 1
    compare_matrix[5:6, 5:6] = 1

    compare_matrix[0:2, 3:5] = 1
    compare_matrix[2:3, 5:6] = 1
    compare_matrix[3:5, 0:2] = 1
    compare_matrix[5:6, 2:3] = 1

    print(compare_matrix)

    (bx, by) = np.nonzero(np.round(laminate.get_stiffnessMatrix(), 3))
    lam_matrix = np.zeros(laminate.get_stiffnessMatrix().shape)
    for x, y in zip(bx, by):
        lam_matrix[x, y] = 1

    assert np.array_equal(lam_matrix, compare_matrix)


def test_Laminate_stiffnessMatrix_exzentric_orthotrop_same_thickness():
    matMat = IsotropicMaterial(rho=1, E=1, v=0.25)
    matFib = AnisotropicMaterial(rho=2, v_para_ortho=0.25, E_para=10, E_ortho=2, G=3)

    mat_FRM = FiberReinforcedMaterialUD(matFib=matFib, matMat=matMat)

    ply0 = Ply(mat_FRM, rotation=0, thickness=1)
    ply90 = Ply(mat_FRM, rotation=90, thickness=1)

    laminate = Laminate()
    laminate.addPly(ply0)
    laminate.addPly(ply90)

    # assert preprocessing
    np.set_printoptions(precision=3, suppress=True)
    print(laminate.get_stiffnessMatrix())

    compare_matrix = np.zeros((6, 6))
    compare_matrix[0:2, 0:2] = 1
    compare_matrix[2:3, 2:3] = 1
    compare_matrix[3:5, 3:5] = 1
    compare_matrix[5:6, 5:6] = 1

    compare_matrix[0:1, 3:4] = 1
    compare_matrix[1:2, 4:5] = 1
    compare_matrix[3:4, 0:1] = 1
    compare_matrix[4:5, 1:2] = 1
    print(compare_matrix)

    (bx, by) = np.nonzero(np.round(laminate.get_stiffnessMatrix(), 3))
    lam_matrix = np.zeros(laminate.get_stiffnessMatrix().shape)
    for x, y in zip(bx, by):
        lam_matrix[x, y] = 1

    assert np.array_equal(lam_matrix, compare_matrix)


def test_Laminate_stiffnessMatrix_antimetric_middle_layer():
    matMat = IsotropicMaterial(rho=1, E=1, v=0.25)
    matFib = AnisotropicMaterial(rho=2, v_para_ortho=0.25, E_para=10, E_ortho=2, G=3)

    mat_FRM = FiberReinforcedMaterialUD(matFib=matFib, matMat=matMat)

    ply0 = Ply(mat_FRM, rotation=0, thickness=1)
    plyP45 = Ply(mat_FRM, rotation=45, thickness=1)
    plyN45 = Ply(mat_FRM, rotation=-45, thickness=1)

    laminate = Laminate()
    laminate.addPly(plyP45)
    laminate.addPly(ply0)
    laminate.addPly(plyN45)

    # assert preprocessing
    np.set_printoptions(precision=3, suppress=True)
    print(laminate.get_stiffnessMatrix())

    compare_matrix = np.zeros((6, 6))
    compare_matrix[0:2, 0:2] = 1
    compare_matrix[2:5, 2:5] = 1
    compare_matrix[5:6, 5:6] = 1
    compare_matrix[0:2, 5:6] = 1
    compare_matrix[5:6, 0:2] = 1
    print(compare_matrix)

    (bx, by) = np.nonzero(np.round(laminate.get_stiffnessMatrix(), 3))
    lam_matrix = np.zeros(laminate.get_stiffnessMatrix().shape)
    for x, y in zip(bx, by):
        lam_matrix[x, y] = 1

    assert np.array_equal(lam_matrix, compare_matrix)
