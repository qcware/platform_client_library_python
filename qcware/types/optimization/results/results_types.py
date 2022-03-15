from collections import OrderedDict
from itertools import tee, takewhile
from typing import Iterator, List, Optional, Tuple, Union, Iterable

import numpy as np
import pydantic
from qcware.types.optimization import Domain
from qcware.types.optimization.problem_spec import BinaryProblem
from qcware.types.optimization.results import utils
from qcware.types.optimization.variable_types import domain_bit_values


class Sample(pydantic.BaseModel):
    bitstring: Tuple[int, ...]
    value: int
    occurrences: int = 1

    @pydantic.validator("occurrences")
    def positive_occurrences(cls, v):
        if v <= 0:
            raise ValueError(
                "Sample occurrences must be positive. If there are no samples "
                "for this bitstring, then the sample should not be included "
                "in a BinaryResults construction."
                ""
            )
        return v

    def str_bitstring(self, domain: Domain):
        """Write the sample bitstring in a format like '011' or '+--'."""
        return binary_ints_to_binstring(bl=self.bitstring, domain=domain)

    def convert(self, mapping: dict[int, int]) -> "Sample":
        return Sample(
            bitstring=tuple(mapping[i] for i in self.bitstring),
            value=self.value,
            occurrences=self.occurrences,
        )

    def __add__(self, other: "Sample"):
        if other.bitstring != self.bitstring:
            raise ValueError("Cannot combine samples with different bitstring.")
        if other.value != self.value:
            raise ValueError("Cannot combine samples with different value.")
        return Sample(
            bitstring=self.bitstring,
            occurrences=self.occurrences + other.occurrences,
            value=self.value,
        )


def bool_sample_to_spin_sample(s: Sample):
    """Convert a Sample with boolean variables to spin variables.

    Does not change sample occurrences or value.
    """
    conversion = {0: 1, 1: -1}
    try:
        return s.convert(conversion)
    except KeyError:
        raise ValueError(f"Expected sample to have boolean domain.\nFound: {s}")


def spin_sample_to_bool_sample(s: Sample):
    """Convert a Sample with spin variables to boolean variables.

    Does not change sample occurrences or value.
    """
    conversion = {1: 0, -1: 1}
    try:
        return s.convert(conversion)
    except KeyError:
        raise ValueError(f"Expected sample to have spin domain.\nFound: {s}")


class BinaryResults(pydantic.BaseModel):
    sample_ordered_dict: OrderedDict
    original_problem: BinaryProblem
    task_metadata: Optional[dict] = None
    result_metadata: Optional[dict] = None
    _sample_list: Optional[List[Sample]] = pydantic.PrivateAttr(None)

    @classmethod
    def from_unsorted_samples(
        cls,
        samples: Iterator[Sample],
        original_problem: BinaryProblem,
        task_metadata: Optional[dict] = None,
        result_metadata: Optional[dict] = None,
    ):
        # accumulator indexed by bitstring:
        accumulator = {}

        for s in samples:
            bitstring = s.str_bitstring(domain=original_problem.domain)
            if bitstring in accumulator:
                accumulator[bitstring].occurrences += s.occurrences
                if accumulator[bitstring].value != s.value:
                    raise ValueError(
                        "Encountered samples with identical bitstring but "
                        "distinct objective values."
                    )
            else:
                accumulator[bitstring] = s
                if len(bitstring) != original_problem.num_variables:
                    raise ValueError(
                        f"Encountered bitstring with {len(s.bitstring)} "
                        f"variables. Expected "
                        f"{original_problem.num_variables}."
                    )

        sample_ordered_dict = (
            (k, v) for (k, v) in sorted(accumulator.items(), key=lambda x: x[1].value)
        )
        sample_ordered_dict = OrderedDict(sample_ordered_dict)
        return cls(
            sample_ordered_dict=sample_ordered_dict,
            original_problem=original_problem,
            task_metadata=task_metadata,
            result_metadata=result_metadata,
        )

    def __eq__(self, value):
        return (
            self.sample_ordered_dict == value.sample_ordered_dict
            and self.original_problem == value.original_problem
            and self.task_metadata == value.task_metadata
            and self.result_metadata == value.result_metadata
        )

    def __getitem__(self, bitstring: Union[str, Iterable[int]]) -> Sample:
        """Get sample data for given bitstring.

        Bitstrings can be specified in a few ways:
            - Iterable[int] as in [0, 1, 0, 1]
            - str as in '0101' (or '+-+-' in the spin case)

        Returns:
            Sample with occurrences set to the total number of occurrences
            for this particular bitstring.
        """
        if not isinstance(bitstring, str):
            bitstring = binary_ints_to_binstring(bitstring, domain=self.domain)

        try:
            return self.sample_ordered_dict[bitstring]
        except KeyError:
            raise KeyError(f"There is no sample matching {bitstring}.")

    def num_occurrences(self, bitstring: Union[str, Iterable[int]]) -> int:
        """Get the number of occurrences for a given binary string.

        If the specified bitstring does has no samples, 0 is returned.
        """
        try:
            return self[bitstring].occurrences
        except KeyError:
            return 0

    def keys(self):
        """Iterate through str representations of samples.

        The keys are binary strings like '0101'. The order of the iteration
        goes from lowest values of the objective function to highest.
        """
        return self.sample_ordered_dict.keys()

    def items(self):
        """Iterate through the sample data.

        The order of iteration goes from lowest values of the objective
        function to the highest.
        """
        return self.sample_ordered_dict.items()

    @property
    def domain(self) -> Domain:
        """The domain (boolean or spin) of the variables."""
        return self.original_problem.domain

    @property
    def num_variables(self) -> int:
        """The number of binary variables for the objective function."""
        return self.original_problem.num_variables

    @property
    def samples(self):
        return self.sample_ordered_dict.values()

    @property
    def sample_list(self) -> List[Sample]:
        """List of all samples ordered by objective value."""
        if self._sample_list is None:
            self._sample_list = list(self.sample_ordered_dict.values())
        return self._sample_list

    @property
    def num_distinct_bitstrings(self) -> int:
        return len(self.sample_ordered_dict)

    @property
    def total_num_occurrences(self) -> int:
        """The total number of occurrences of any bitstring.

        Includes in the count multiple occurrences of the same strings.
        """
        return sum(s.occurrences for s in self.sample_list)

    @property
    def lowest_value(self) -> int:
        """Lowest observed value of the objective function."""
        first_sample = next(iter(self.samples))
        return first_sample.value

    @property
    def lowest_value_bitstring(self) -> Tuple[int, ...]:
        """A Bitstring with the lowest value of the objective function.

        This property only provides one example of a bitstring with the
        lowest value. To get all bitstrings with lowest value, use
        lowest_value_sample_list.
        """
        first_sample = next(iter(self.samples))
        return first_sample.bitstring

    @property
    def lowest_value_sample_list(self) -> List[Sample]:
        """List of samples with lowest observed objective value."""
        lowest_value = self.lowest_value
        samples = takewhile(lambda s: s.value == lowest_value, self.samples)
        return list(samples)

    @property
    def num_occurrences_lowest_value(self) -> int:
        """The number of observed occurrences of the lowest value."""
        return self.num_occurrences_under(val=self.lowest_value + 1)

    def num_occurrences_under(self, val: int) -> int:
        """The number of occurrences below a given objective value."""
        samples = takewhile(lambda s: s.value < val, self.samples)
        return sum(s.occurrences for s in samples)

    @property
    def num_bitstrings_lowest_value(self) -> int:
        """The number of observed bitstrings of the lowest value."""
        return self.num_bitstrings_under(val=self.lowest_value + 1)

    def num_bitstrings_under(self, val: int) -> int:
        """The number of distinct bitstrings below a given objective value."""
        samples = takewhile(lambda s: s.value < val, self.samples)
        return sum(1 for _ in samples)

    def __eq__(self, other: "BinaryResults"):
        conditions = (
            self.sample_ordered_dict == other.sample_ordered_dict,
            self.original_problem == other.original_problem,
            self.task_metadata == other.task_metadata,
            self.result_metadata == other.result_metadata,
        )
        return all(conditions)

    def __str__(self) -> str:
        if self.num_distinct_bitstrings == 0:
            return "No solutions sampled."
        out = "Objective value: "

        out += str(self.lowest_value) + "\n"
        out += "Solution: "
        out += str(self.lowest_value_bitstring)

        if self.num_occurrences_lowest_value > 1:
            out += (
                f" (and {self.num_bitstrings_lowest_value-1} "
                f"other equally good solution"
            )
            if self.num_bitstrings_lowest_value == 2:
                out += ")"
            else:
                out += "s)"
        return out


def samples_to_array(samples: Iterator[Sample], domain: Domain, num_variables: int):
    """Convert a sequence of Samples to a NumPy array.

    Performs optional validation if domain and num_variables are specified.
    """
    try:
        bitstrings = np.array(list(s.bitstring for s in samples), dtype=int)
    except ValueError:
        raise ValueError("Samples provided appear to have inconsistent string length.")

    if bitstrings.shape[-1] != num_variables:
        raise ValueError(
            f"Sample bitstrings have {bitstrings.shape[-1]} variables, "
            f"but the original problem instance has {num_variables}."
        )

    valid_bits = domain_bit_values(domain)
    if not np.isin(bitstrings, valid_bits).all():
        raise ValueError(
            f"Bitstrings are expected to have domain {domain} but "
            f"found entries outside of {valid_bits}."
        )
    return bitstrings


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


def binary_ints_to_binstring(bl: Iterable[int], domain: Domain = Domain.BOOLEAN):
    """Convert a binary object like [0, 1, 1] to a string like '011'."""
    if domain is Domain.BOOLEAN:

        def conv(bit):
            if bit not in {0, 1}:
                raise ValueError(f"Expected 0 or 1, found {bit}")
            return str(bit)

        return "".join(map(conv, bl))
    elif domain is Domain.SPIN:

        def conv(bit):
            if bit == 1:
                return "+"
            elif bit == -1:
                return "-"
            else:
                raise ValueError(f"Expected 1 or -1, found {bit}")

        return "".join(map(conv, bl))
    else:
        raise TypeError(f"Expected Domain, found {type(domain)}")
