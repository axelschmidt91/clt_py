"""Main module."""


class NotEnoughArgumentError(Exception):
    """Exception raised when too few arguments where passed to function."""
    pass


class OverDeterminedError(Exception):
    """Raised when too many arguments where passed.
    So the system is over-determined."""
    pass


class Material:

    class NotAnisotropicError(Exception):
        pass

    class NotIsotropicError(Exception):
        pass

    # TODO: Subclasses for Anisitropic Material and isotropic Material. --> Independend material properties are different

    def __init__(self, rho, E=None, G=None, v=None):
        super().__init__()
        self.rho = rho
        if (G is not None) and (v is not None) and (E is not None):
            raise OverDeterminedError()
        elif (((G is None) and (v is None)) or ((G is None) and (E is None)) or ((E is None) and (v is None))):
            raise NotEnoughArgumentError()
        elif G is None:
            self.E = E
            self.v = v
            if isinstance(E, list):
                self.G = [x / (2 * (1 + v)) for x in E]
            else:
                self.G = E / (2 * (1 + v))
        elif E is None:
            self.G = G
            self.v = v
            if isinstance(G, list):
                self.E = [2 * x * (1 + v) for x in G]
            else:
                self.E = 2 * G * (1 + v)
        elif v is None:
            self.E = E
            self.G = G
            if isinstance(E, list) or isinstance(G, list):
                self.v = [x / (2 * y) - 1 for x, y in zip(E, G)]
            else:
                self.v = E / (2 * G) - 1
            if isinstance(self.v, list):
                if len(self.v) == self.v.count(self.v[0]):
                    self.v = self.v[0]
                else:
                    raise OverDeterminedError()

        self.isotropic = True
        if isinstance(self.E, list):
            self.isotropic = False


class Ply:

    system = "simplified"  # "simplified" or "hsb"

    def __init__(self, matFib, matMat, fibVolRatio=0.5):
        super().__init__()
        self.set_matFib(matFib)
        self.set_matMat(matMat)
        self.set_fibVolRatio(fibVolRatio)

    def set_fibWgRatio(self, fibWgRatio):
        self.fibVolRatio = (fibWgRatio * self.matMat.rho) / (fibWgRatio * self.matMat.rho + (1 - fibWgRatio) * self.matFib.rho)
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
        # TODO: check for isinstance of Anisotropic class
        if isinstance(matFib, list):
            if len(matFib) <= 1:
                raise Material.NotAnisotropicError()
        else:
            raise Material.NotAnisotropicError()

    def check_matMat(self, matMat):
        # TODO: check for isinstance of Isotropic class
        if isinstance(matMat, list):
            raise Material.NotIsotropicError()

    def update(self):
        if system is "simplified":
            self.prismatic_jones_model()
        elif system is "hsb":
            self.hsb_model()
        else:
            raise ValueError

    def prismatic_jones_model(self):
        raise NotImplementedError()
        E_para = self.matFib.E[0] * self.fibVolRatio + self.matMat.E * (1 - self.fibVolRatio)
        E_orto = (self.matFib.E[1] * self.matMat.E) / (self.matMat.E * self.fibVolRatio + self.matFib.E[1] * (1 - self.fibVolRatio))
        self.E = [E_para, E_orto]
        self.G = (self.matFib.G) / ()
        # self.v =
        # self.rho =

    def hsb_model(self):
        # TODO: Implementation
        raise NotImplementedError()
        self.E = 0
        self.G = 0
        self.rho = 0


class Laminate:

    def __init__(self):
        super().__init__()

    def addPly(self, rotation=0):
        pass
