from typing import List, Optional, Tuple, Union
from qcware.types.optimization import Domain


def iterable(obj):
    """Return True iff iter(obj) works."""
    try:
        iter(obj)
    except TypeError:
        return False
    else:
        return True


def int_to_bin(
        x: int, num_bits: int,
        int_return=False,
):
    if x >= 2 ** num_bits:
        raise ValueError(f'Insufficient bits to store integer {x}.')
    if x < 0:
        raise ValueError(f'Integer should be nonnegative but found {x}.')

    bin_format = str(bin(x))[2:]
    padding_size = num_bits - len(bin_format)
    bin_format = padding_size * '0' + bin_format
    if not int_return:
        return bin_format
    else:
        return [int(x) for x in bin_format]


def intlist_to_binlist(
        integers: List[int],
        num_bits: int,
        symbols: Union[Tuple[str, str], Domain, None] = None
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
        symbols = ('0', '1')
    if symbols is Domain.SPIN:
        symbols = ('+', '-')

    bin_list = [int_to_bin(x, num_bits)for x in integers]
    if symbols is None:
        return bin_list
    else:
        def bin_to_symbols(x):
            if x == '0':
                return symbols[0]
            elif x == '1':
                return symbols[1]
            else:
                raise RuntimeError(
                    f'Encountered {x} but expected \'0\' or \'1\'.')

        return [''.join(map(bin_to_symbols, s)) for s in bin_list]



