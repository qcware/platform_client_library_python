import enum


class Predicate(str, enum.Enum):
    """Relations for constraint specification."""

    NONNEGATIVE = "nonnegative"
    POSITIVE = "positive"
    NONPOSITIVE = "nonpositive"
    NEGATIVE = "negative"
    ZERO = "zero"
    NONZERO = "nonzero"

    def __repr__(self):
        return str(self).__str__()
