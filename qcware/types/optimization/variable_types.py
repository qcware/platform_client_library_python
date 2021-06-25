import enum


class Domain(str, enum.Enum):
    """Possible types of variables for binary polynomials."""

    BOOLEAN = "boolean"
    SPIN = "spin"

    def __repr__(self):
        return str(self).__str__()
