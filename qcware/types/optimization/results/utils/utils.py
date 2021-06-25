import math
from qcware.types.optimization import utils


def short_list_str(lst, expected_characters, name=None):
    if name is None:
        out = ""
    else:
        out = name + "="
    if expected_characters <= 200 or len(lst) < 6:
        out += str(lst)
    else:
        out += str(lst[:3])[:-1]
        out += " ..., " + str(lst[-3:])[1:]

    return out


def short_string(string: str, name=None):
    if len(string) <= 80:
        out = string
    else:
        out = string[:10]
        out += f"... [{len(string)-20} characters hidden] ..."
        out += string[-10:]

    if name is None:
        return out
    else:
        return name + "=" + out


def format_feasible_set(feasible_set: str, num_feasible: int = None):
    """Get the feasible set as a list of binary strings.

    This format is less compressed than the feasible_set attribute
    which is a string of length 2^n.
    """
    if feasible_set is None:
        if num_feasible == 0:
            return []
        raise RuntimeError("No feasible set is stored.")

    num_values = len(feasible_set)
    num_variables = round(math.log2(num_values))
    if 2 ** num_variables != num_values:
        raise ValueError("feasible_set must be a string of length 2^n.")

    index_list = [i for i in range(len(feasible_set)) if feasible_set[i] == "1"]
    return utils.intlist_to_binlist(index_list, num_variables)
