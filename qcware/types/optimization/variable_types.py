import enum


class Domain(str, enum.Enum):
    """Possible types of variables for binary polynomials."""

    BOOLEAN = "boolean"
    SPIN = "spin"

    def __repr__(self):
        return str(self).__str__()


def domain_bit_values(domain: Domain):
    """Get values of bits that are intended to be associated with a Domain."""
    if domain is Domain.BOOLEAN:
        return [0, 1]
    elif domain is Domain.SPIN:
        return [1, -1]
    else:
        raise TypeError(f"Expected Domain, found {type(domain)}.")
