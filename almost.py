import math

class Approximate(object):
    def __init__(self, expected, prec=3):
        self.expected = expected
        self.prec = prec

    def normalize(self, value):
        return value

    def _compare(self, a, b):
        if hasattr(a, 'mu') and hasattr(a, 'sigma'):
            a = (a.mu, a.sigma)
        if hasattr(b, 'mu') and hasattr(b, 'sigma'):
            b = (b.mu, b.sigma)
        if isinstance(a, float) or isinstance(a, int):
            if isinstance(a, float) and isinstance(b, float):
                if math.isnan(a) and math.isnan(b):
                    return True
            tolerance = 10 ** (-self.prec)
            return abs(a - b) <= tolerance
        elif isinstance(a, (list, tuple)):
            if len(a) != len(b):
                return False
            return all(self._compare(x, y) for x, y in zip(a, b))
        elif isinstance(a, dict):
            if set(a.keys()) != set(b.keys()):
                return False
            return all(self._compare(a[k], b[k]) for k in a)
        else:
            return a == b

    def __eq__(self, other):
        return self._compare(self.normalize(other), self.normalize(self.expected))

    def __ne__(self, other):
        return not self.__eq__(other)

    @classmethod
    def wrap(cls, f, *args, **kwargs):
        def wrapper(*a, **k):
            return cls(f(*a, **k), *args, **kwargs)
        return wrapper
