import dataclasses
import pydantic
import itertools
from qcware.types.utils import pydantic_model_abridge_validation_errors

from typing import Dict, Tuple, Set, Union


def compute_degree(polynomial: dict):
    """Compute the largest length of a term in given polynomial dict.

    If there are no terms, return -1. This choice of -1 is corrected to
    -inf after validation is complete.

    The degree here is not always the mathematically correct degree, even
    for nontrivial polynomials. For
    example, the polynomial specified by {(1,): 12, (0, 1): 0} has
    mathematical degree 1 but this function will return 2.
    """
    if polynomial == {}:
        return -1
    return max(len(term) for term in polynomial)


def polynomial_validation(
    polynomial: dict, num_variables: int, validate_types: bool = True
):
    """

    Args:
        polynomial:

        num_variables:

        validate_types: If the polynomial has many terms, validating
            all types can take a while. There is no reason to repeat
            such a validation if it has already been done elsewhere.
            By setting validate_types to False, the system will trust
            the user to provide a polynomial with the correct structure.

    Returns:

    """
    # By sneakily changing from a pydantic.dataclass to a vanilla dataclass,
    # we are able to turn off type checking while still using __post_init__.
    # This is admittedly somewhat hacky.
    if validate_types:
        dataclass_selection = pydantic.dataclasses.dataclass
        # int_type = pydantic.StrictInt
        int_type = int  # I disabled strict validation due to numpy issues.
    else:
        dataclass_selection = dataclasses.dataclass
        int_type = int

    @dataclass_selection
    class _PolynomialValidation:
        poly: Dict[Tuple[int_type, ...], int_type]
        num_vars: int_type
        deg: int = None
        variables: Set[int] = None

        def __post_init__(self):
            # These are computed fields so they should start as None.
            assert self.deg is None
            assert self.variables is None
            self.deg = compute_degree(self.poly)
            self.variables = set(itertools.chain.from_iterable(self.poly.keys()))
            if not self.variables.issubset(range(self.num_vars)):
                raise ValueError(
                    f"Specified number of variables {self.num_vars} is inconsistent with "
                    f"the variables in the polynomial.\nExpected variables "
                    f"to be ints in the range {{0,...,{self.num_vars - 1}}} "
                    f"but found variables between {min(self.variables)} and "
                    f"{max(self.variables)} inclusive."
                )

    return pydantic_model_abridge_validation_errors(
        model=_PolynomialValidation,
        max_num_errors=10,
        poly=polynomial,
        num_vars=num_variables,
    )
