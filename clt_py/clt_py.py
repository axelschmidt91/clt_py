"""Main module."""

import math
import numpy as np


class NotEnoughArgumentError(Exception):
    """Exception raised when too few arguments where passed to function."""

    pass


class OverDeterminedError(Exception):
    """Raised when too many arguments where passed.
    So the system is over-determined."""

    pass


class Material2D:
    class NotAnisotropicError(Exception):
        pass

    class NotIsotropicError(Exception):
        pass

    def __init__(self, rho, E_para, E_ortho, G, v_para_ortho, label="material"):
        super().__init__()
        self.rho = rho
        self.label = label
        self.E_para = E_para
        self.E_ortho = E_ortho
        self.G = G
        self.v_para_ortho = v_para_ortho

    def calc_poissonRatio_ortho_pata(self):
        self.v_ortho_para = self.v_para_ortho * self.E_ortho / self.E_para

    def calc_stiffness_compliance_matrices(self):
        s_para = 1 / self.E_para
        s_ortho = 1 / self.E_ortho
        s_para_ortho = -self.v_para_ortho / self.E_para
        s_shear = 1 / self.G

        self.complianceMatrix = np.array(
            [[s_para, s_para_ortho, 0], [s_para_ortho, s_para, 0], [0, 0, s_shear]]
        )
        self.stiffnessMatrix = np.invert(self.complianceMatrix)


class IsotropicMaterial(Material2D):
    def __init__(self, rho, label="material", E=None, G=None, v=None):
        if (G is not None) and (v is not None) and (E is not None):
            raise OverDeterminedError()
        elif (
            ((G is None) and (v is None))
            or ((G is None) and (E is None))
            or ((E is None) and (v is None))
        ):
            raise NotEnoughArgumentError()
        elif G is None:
            G = E / (2 * (1 + v))
        elif E is None:
            E = 2 * G * (1 + v)
        elif v is None:
            v = E / (2 * G) - 1
        super().__init__(
            self, rho=rho, E_para=E, E_ortho=E, G=G, v_para_ortho=v, label=label
        )


class AnisotropicMaterial(Material2D):
    def __init__(self, rho, E_para, E_ortho, G, v_para_ortho, label="material"):
        super().__init__(rho, label=label)
        self.E_para = E_para
        self.E_ortho = E_ortho
        self.G = G
        self.v_para_ortho = v_para_ortho


class FiberReinforcedMaterialUD(Material2D):

    system = "hsb"  # "prismatic_jones" or "hsb"

    def __init__(
        self, matFib, matMat, fibVolRatio=0.5, kapa=[1, 1, 1], label="FRM_material"
    ):
        self.check_matFib(matFib)
        self.matFib = matFib
        self.check_matMat(matMat)
        self.matMat = matMat
        self.fibVolRatio = fibVolRatio
        self.kapa = kapa
        self.update()
        super().__init__(self.rho, label)

    def set_fibWgRatio(self, fibWgRatio):
        self.fibVolRatio = (fibWgRatio * self.matMat.rho) / (
            fibWgRatio * self.matMat.rho + (1 - fibWgRatio) * self.matFib.rho
        )
        self.update()

    def set_fibVolRatio(self, fibVolRatio):
        self.fibVolRatio = fibVolRatio
        self.update()

    def set_matFib(self, matFib):
        self.check_matFib(matFib)
        self.matFib = matFib
        self.update()

    def set_matMat(self, matMat):
        self.check_matMat(matMat)
        self.matMat = matMat
        self.update()

    def check_matFib(self, matFib):
        if not isinstance(matFib, AnisotropicMaterial):
            raise Material2D.NotAnisotropicError()

    def check_matMat(self, matMat):
        if not isinstance(matMat, IsotropicMaterial):
            raise Material2D.NotIsotropicError()

    def update(self):
        if self.system == "prismatic_jones":
            self.prismatic_jones_model()
        elif self.system == "hsb":
            self.hsb_model()
        else:
            raise ValueError
        self.calc_stiffness_compliance_matrices()

    def prismatic_jones_model(self):
        self.E_para = self.matFib.E_para * self.fibVolRatio + self.matMat.E * (
            1 - self.fibVolRatio
        )
        self.E_ortho = (self.matFib.E_ortho * self.matMat.E) / (
            self.matMat.E * self.fibVolRatio
            + self.matFib.E_ortho * (1 - self.fibVolRatio)
        )
        self.G = (self.matFib.G * self.matMat.G) / (
            self.matMat.G * self.fibVolRatio + self.matFib.G * (1 - self.fibVolRatio)
        )
        self.v_para_ortho = (
            self.fibVolRatio * self.matFib.v + (1 - self.fibVolRatio) * self.matMat.v
        )
        self.calc_poissonRatio_ortho_pata()
        self.calc_density()

    def hsb_model(self):
        # helping variables
        v = math.sqrt(self.fibVolRatio / math.pi)
        e = 1 - self.matMat.E / self.matFib.E_ortho
        g = 1 - self.matMat.G / self.matFib.G
        q_G = (1 + 2 * g * v) / (1 - 2 * g * v)
        q_E = (1 + 2 * e * v) / (1 - 2 * e * v)

        self.E_para = self.kapa[0] * (
            self.matFib.E_para * self.fibVolRatio
            + self.matMat.E * (1 - self.fibVolRatio)
        )
        self.E_ortho = (
            self.kapa[1]
            * self.matMat.E
            * (
                1
                - 2 * v
                - math.pi / (2 * e)
                + (
                    (2 * math.atan(math.sqrt(q_E)))
                    / (e * math.sqrt(1 - math.pow(2 * e * v, 2)))
                )
            )
        )
        self.G = (
            self.kapa[2]
            * self.matMat.G
            * (
                1
                - 2 * v
                - math.pi / (2 * g)
                + (
                    (2 * math.atan(math.sqrt(q_G)))
                    / (g * math.sqrt(1 - math.pow(2 * g * v, 2)))
                )
            )
        )
        self.v_para_ortho = self.matFib.v * self.fibVolRatio + self.matMat.v * (
            1 - self.fibVolRatio
        )
        self.calc_poissonRatio_ortho_pata()
        self.calc_density()

    def calc_density(self):
        self.rho = (
            self.fibVolRatio
            + self.matMat.rho / self.matFib.rho * (1 - self.fibVolRatio)
        ) * self.matFib.rho


class Ply:
    def __init__(self, reinforcedMat, thickness, rotation=0):
        super().__init__()
        self.mat = reinforcedMat


class Laminate:
    def __init__(self):
        super().__init__()
        self.stack = []

    def addPly(self, rotation=0):
        pass
