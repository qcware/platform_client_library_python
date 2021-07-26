from typing import List, Optional, Tuple, Union
from qcware.types.optimization import Domain
import numpy as np


def iterable(obj):
    """Return True iff iter(obj) works."""
    try:
        iter(obj)
    except TypeError:
        return False
    else:
        return True


def int_to_bin(
    x: int,
    num_bits: int,
    int_return=False,
):
    if x >= 2 ** num_bits:
        raise ValueError(f"Insufficient bits to store integer {x}.")
    if x < 0:
        raise ValueError(f"Integer should be nonnegative but found {x}.")

    bin_format = str(bin(x))[2:]
    padding_size = num_bits - len(bin_format)
    bin_format = padding_size * "0" + bin_format
    if not int_return:
        return bin_format
    else:
        return [int(x) for x in bin_format]


def intlist_to_binlist(
    integers: List[int],
    num_bits: int,
    symbols: Union[Tuple[str, str], Domain, None] = None,
):
    """Convert list of integers to list of binary strings.

    Example: if there are three bits, [3, 1] will be
    converted to ['011', '001'].

    If `symbols` is given then strings other than '0' or '1' can be used.
    For example, if symbols=('a', 'b'), then [3, 1] will be
    converted to ['abb', 'aab'] assuming that num_bits=3.

    Since the most common symbol choices are "boolean" and "spin" where we use
    ('0', '1') and ('+', '-') respectively, symbols can also be specified
    by a Domain.
    """
    if symbols is Domain.BOOLEAN:
        symbols = ("0", "1")
    if symbols is Domain.SPIN:
        symbols = ("+", "-")

    bin_list = [int_to_bin(x, num_bits) for x in integers]
    if symbols is None:
        return bin_list
    else:

        def bin_to_symbols(x):
            if x == "0":
                return symbols[0]
            elif x == "1":
                return symbols[1]
            else:
                raise RuntimeError(f"Encountered {x} but expected '0' or '1'.")

        return ["".join(map(bin_to_symbols, s)) for s in bin_list]


def bitarray_to_int(bitstrings: np.ndarray, domain: Domain):
    """Convert an array of binary strings to corresponding ints.

    For example, if `bitstrings` is
        np.array(
            [[0, 1, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0]]
        )
    then this function returns []
    """
    if domain is Domain.SPIN:
        bitstrings = (1 - bitstrings) // 2

    num_variables = bitstrings.shape[-1]
    powers = np.array([2 ** n for n in reversed(range(num_variables))])
    return (powers * bitstrings).sum(axis=-1)


def bitstring_to_intlist(binstring, domain: Domain):
    if domain is Domain.BOOLEAN:
        return [int(i) for i in binstring]
    elif domain is Domain.SPIN:

        def conversion(i):
            if i == "+":
                return 1
            elif i == "-":
                return -1
            else:
                raise ValueError(
                    "For spin domain, if binstring is an str, bits must be"
                    f"'+' or '-'. Encountered {i}."
                )

        return [conversion(i) for i in binstring]
    else:
        raise TypeError(f"Expected Domain, encountered {type(domain)}.")


def bin_to_int(bin_spec, domain: Domain, num_variables: Optional[int] = None):
    """Convert a binary specification of a number to an int.

    If `bin_spec` is already an int, it is returned as is.

    Args:
        bin_spec: Binary specification of a number. Valid specifications are:
            - List[int] as in [0, 1, 0, 1]
            - str as in '0101' (or '+-+-' in the spin case)
            - int as in 5. In this case, 5 is returned.
        domain: Domain for the variables (boolean or spin).
        num_variables: When specified, checks that the number of variables is
            consistent with `spec`. Note that if `spec` is an `int`, then
            this validation can only confirm that `spec` is not too large.

    Returns: Integer corresponding to the given binary string.
    """
    if isinstance(bin_spec, int):
        if bin_spec < 0:
            raise ValueError(f"Integer bin_spec must be positive, found {bin_spec}.")
        if num_variables is not None:
            if bin_spec >= 2 ** num_variables:
                raise ValueError(
                    f"{bin_spec} is too large for {num_variables} " f"binary variables."
                )
        return bin_spec
    if num_variables is not None:
        if len(bin_spec) != num_variables:
            raise ValueError(
                f"Expected a binary string with {num_variables} variables, "
                f"but got {bin_spec} which has {len(bin_spec)} variables."
            )
    if isinstance(bin_spec, str):
        return bin_to_int(
            bin_spec=bitstring_to_intlist(binstring=bin_spec, domain=domain),
            domain=domain,
        )
    else:
        bin_spec = bitarray_to_int(np.array(bin_spec), domain=domain)
        return int(bin_spec)
