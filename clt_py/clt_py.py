"""Main module."""


def add(a, b):
    return a + b


class NotEnoughArgumentError(Exception):
    """Exception raised when too few arguments where passed to function."""
    pass


class OverDeterminedError(Exception):
    """Raised when too many arguments where passed. 
    So the system is over-determined."""


class Material:

    def __init__(self, E=None, rho, G=None, v=None):
        self.rho = rho
        if G is not None & v is not None & E is not None:
            OverDeterminedError()
        elif G is None & v is None | G is None & E is None | E is None & v is None:
            NotEnoughArgumentError()
        elif G is None:
            self.E = E
            self.v = v
            self.G = E / (2 * (1 + v))
        elif E is None:
            self.G = G
            self.v = v
            self.E = 2 * G * (1 + v)
        elif v is None:
            self.E = E
            self.G = G
            self.v = E / (2 * G) - 1
            if isinstance(self.v, list()):
                if len(self.v) == self.v.count(self.v[0]):
                    self.v = self.v[0]
                else:
                    OverDeterminedError()
        self.isotropic = True
        if isinstance(self.E, list()):
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
