import pydantic
from typing import Optional, List, Union

from qcware.types.optimization.utils import intlist_to_binlist

from . import utils
from qcware.types.optimization import Domain


class BruteOptimizeResult(pydantic.BaseModel):
    """Return type for brute force maximization and minimization.

    When solution_exists == False, we must have value is None and
    argmin == [].

    Arguments are specified with a list of strings that describe solutions.
    For the boolean case, this means something like ['00101', '11100'] and
    for the spin case, this means something like ['++-+-', '---++'].

    The method int_argmin can be used to obtain minima in the format
        Boolean case: [[0, 0, 1, 0, 1], [1, 1, 1, 0, 0]]
    or
        Spin case: [[1, 1, -1, 1, -1], [-1, -1, -1, 1, 1]].
    """

    domain: Domain
    value: Optional[int] = None
    argmin: List[str] = []
    solution_exists: bool = True

    @pydantic.validator("solution_exists", always=True)
    def no_solution_check(cls, sol_exists, values):
        if not sol_exists:
            if not values["value"] is None:
                raise ValueError("Value given but solution_exists=False.")
            if not values["argmin"] == []:
                raise ValueError("argmin given but solution_exists=False.")

        else:
            if values["value"] is None or values["argmin"] == []:
                raise ValueError("solution_exists=True, but no solution was specified.")
        return sol_exists

    def int_argmin(self) -> List[List[int]]:
        """Convert argmin to a list of list of ints."""

        def to_int(x: str):
            if self.domain is Domain.BOOLEAN:
                return int(x)
            else:
                if x == "+":
                    return 1
                elif x == "-":
                    return -1
                else:
                    raise ValueError(f"Unrecognized symbol {x}. Expected '+' or '-'.")

        return [[to_int(x) for x in s] for s in self.argmin]

    @property
    def num_variables(self):
        if not self.solution_exists:
            return
        return len(self.argmin[0])

    @property
    def num_minima(self):
        return len(self.argmin)

    def __repr__(self):
        if self.solution_exists:
            out = "forge.types.BruteOptimizeResult(\n"
            out += f"value={self.value}\n"
            char_estimate = self.num_variables * len(self.argmin)
            out += utils.short_list_str(self.argmin, char_estimate, "argmin")
            return out + "\n)"
        else:
            return "forge.types.BruteOptimizeResult(solution_exists=False)"

    def __str__(self):
        if not self.solution_exists:
            return "No bit string satisfies constraints."

        out = "Objective value: " + str(self.value) + "\n"
        int_argmin = self.int_argmin()
        out += f"Solution: {int_argmin[0]}"
        if self.num_minima > 1:
            out += f" (and {self.num_minima-1} other equally good solution"
            if self.num_minima == 2:
                out += ")"
            else:
                out += "s)"
        return out
