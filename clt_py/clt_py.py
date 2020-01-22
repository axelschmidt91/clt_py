"""Main module."""


class NotEnoughArgumentError(Exception):
    """Exception raised when too few arguments where passed to function."""
    pass


class OverDeterminedError(Exception):
    """Raised when too many arguments where passed.
    So the system is over-determined."""
    pass


class Material:

    def __init__(self, rho, E=None, G=None, v=None):
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
        else:
            raise NotImplementedError()
        self.isotropic = True
        if isinstance(self.E, list):
            self.isotropic = False


class Ply:

    def __init__(self, matFib, matMat, fibVolRatio=0.5):
        super().__init__()
        self.matFib = matFib
        self.matMat = matMat
        self.fibVolRatio = fibVolRatio

    def set_fibWgRatio(self, fibWgRatio):
        self.fibVolRatio = (fibWgRatio * self.matMat.rho) / (fibWgRatio * self.matMat.rho + (1 - fibWgRatio) * self.matFib.rho)

    def set_fibVolRatio(self, fibVolRatio):
        self.fibVolRatio = fibVolRatio


class Laminate:

    def __init__(self):
        super().__init__()

    def addPly(self, rotation=0):
        pass

    pass
