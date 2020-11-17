from typing import List


def iterable(obj):
    """Return True iff iter(obj) works."""
    try:
        iter(obj)
    except TypeError:
        return False
    else:
        return True


def int_to_bin(x: int, num_bits: int, int_return=False):
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


def intlist_to_binlist(integers: List[int], num_bits: int):
    """Convert list of integers to list of binary strings.

    Example: if there are three bits, [3, 1] will be
    converted to ['011', '001'].
    """
    return [int_to_bin(x, num_bits) for x in integers]

