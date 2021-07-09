from pydantic import BaseModel, conint, ValidationError, validator
from typing import List, Union, Dict, Tuple, Any, Optional
import qubovert as qv
import numpy as np
from . import Predicate, Domain

from ...types.optimization import PolynomialObjective
from .problem_spec import Constraints


class BinaryProblem(BaseModel):
    objective: PolynomialObjective
    constraints: Optional[Constraints] = None
    name: str = "my_qcware_binary_problem"

    class Config:
        validate_assignment = True
        allow_mutation = False
        arbitrary_types_allowed = True

    def __str__(self) -> str:
        header0 = "* Name: {0} *\n".format(self.name)
        header1 = "* Variable type: {0} *\n".format(self.objective.domain)
        line = "**********************\n"
        header2 = "Objective function: {0} \n".format(self.objective.polynomial)

        string_out = line + header0 + header1 + line + header2
        if self.constraints is not None:
            string_out += self.constraints.__repr__()
        return string_out

    @classmethod
    def from_dict(
        cls, objective: Dict[Tuple[int, ...], int], domain: Domain = Domain.BOOLEAN
    ):
        """
        Creates the BinaryProblem from a dict specifying a boolean polynomial.
        """

        def count_variables(polynomial: dict):
            var_names = set()
            for k in polynomial.keys():
                var_names.update(k)
            return len(var_names)

        objective = PolynomialObjective(
            polynomial=objective,
            num_variables=count_variables(objective),
            domain=domain,
        )

        return cls(objective=objective)

    def dwave_dict(self):
        """Returns a dict valid for D-Wave problem specification."""
        q_start = self.objective.polynomial
        q_final = {}
        for elm in q_start.keys():
            if elm == ():
                pass
            elif len(elm) == 1:
                q_final[(elm[0], elm[0])] = q_start[(elm[0],)]
            else:
                q_final[elm] = q_start[elm]

        return q_final

    @property
    def num_variables(self):
        """The number of variables for the objective function."""
        return self.objective.num_variables

    @property
    def constraint_dict(self):
        """Constraints in a dict format."""
        return self.constraints.constraint_dict

    def num_constraints(self, predicate: Optional[Predicate] = None):
        """Return the number of constraints.

        If a predicate is specified, only return the number of constraints
        for that predicate.
        """
        return self.constraints.num_constraints(predicate)

    @property
    def constrained(self):
        """True if this problem instance is constrained."""
        return self.constraints is not None


class BinarySample(BaseModel):
    bitstring: List[int]
    energy: int = None
    num_occurrences: int

    @validator("bitstring")
    def bitstring_must_be_01(cls, v):
        for elm in v:
            if elm != 0 and elm != 1:
                raise ValueError("Bitstring values must be 0 or 1")
        return v

    class Config:
        validate_assignment = True
        allow_mutation = False

    def __str__(self) -> str:
        """Print the problem in a nice way"""
        header0 = "* Bitstring: {0} *\n".format(self.bitstring)
        header1 = "* Energy: {0} *\n".format(self.energy)
        header2 = "* Number of ocurrences: {0} *\n".format(self.num_occurrences)

        string_out = header0 + header1 + header2  # + '\n'

        return string_out

    def set_energy(self, energy: float) -> None:
        """Sets the energy of the sample
        Args:
            energy: The energy of the sample.
        """
        return self.copy(deep=True, update=dict(energy=energy))


class BinaryResults(BaseModel):
    """A data class for Binary problem results.

    Members:
      original_problem: The original problem submitted
      backend_data_start: A dictionary of data submitted to the backend
      backend_data_finish: A dictionary of data retrieved from the backend
        often containing run information
      results: a list of BinarySample objects
      variable_mapping: Optional specification of how variables in the original
        problem instance map to variables appearing in binary samples.
    """

    original_problem: BinaryProblem

    backend_data_start: Dict[str, Union[str, int, float, Dict, List, None]]

    backend_data_finish: Dict[str, Union[str, int, float, Dict, List, None]] = {}

    results: List[BinarySample] = []

    class Config:
        validate_assignment = True
        allow_mutation = False

    def __str__(self) -> str:
        if len(self.results) == 0:
            return "No solutions sampled."
        out = "Objective value: "
        lowest_value = self.results[0].energy
        out += str(lowest_value) + "\n"
        out += "Solution: "
        out += str(self.results[0].bitstring)
        num_solutions = 1
        for elm in self.results[1:]:
            if elm.energy == lowest_value:
                num_solutions += 1
            else:
                break

        if num_solutions > 1:
            out += f" (and {num_solutions-1} other equally good solution"
            if num_solutions == 2:
                out += ")"
            else:
                out += "s)"
        return out

    def add_sample(self, sample: BinarySample) -> None:
        """Adds a provided sample to results.
        Args:
            sample: The objective function of the quadratic program.
        """

        def calculate_energy(bitstring: List) -> float:
            """Calculates the energy of a bitstring
            Args:
                bitstring: The bistring
            """
            x = {}
            for elm in range(len(bitstring)):
                x[elm] = bitstring[elm]

            return self.original_problem.objective.qubovert().value(x)

        def sort_bin(b):
            "Orders bitstrings"
            b_view = np.ascontiguousarray(b).view(
                np.dtype((np.void, b.dtype.itemsize * b.shape[1]))
            )
            return np.argsort(b_view.ravel())

        sample_bitstring = sample.bitstring

        # First assert that the solution is the same length as the problem
        assert len(sample_bitstring) == self.original_problem.objective.num_variables

        # Obtain existing results

        new_results = self.results

        # Obtain existing bitstrings

        existing_bitstrings = [elm.bitstring for elm in new_results]

        if sample_bitstring in existing_bitstrings:

            for elm in range(len(new_results)):
                if new_results[elm].bitstring == sample_bitstring:
                    # assert new_results[elm].energy == sample.energy
                    # Find the old num_occurrences
                    old_frequency = new_results[elm].num_occurrences
                    # Modify by new one
                    new_frequency = old_frequency + sample.num_occurrences
                    new_sample = BinarySample(
                        bitstring=sample.bitstring,
                        energy=new_results[elm].energy,
                        num_occurrences=new_frequency,
                    )
                    # Remove the old sample
                    new_results.remove(new_results[elm])
                    # Add new sample
                    new_results.append(new_sample)
                    break
        else:
            # If bitstring not there just add
            # But first calculate energy
            sample = sample.set_energy(calculate_energy(bitstring=sample_bitstring))
            new_results.append(sample)

        bitstrings = [elm.bitstring for elm in new_results]
        order_bitstrings = sort_bin(np.array(bitstrings))

        zip_values = list(zip(new_results, order_bitstrings))

        zip_values.sort(key=lambda x: (x[0].energy, x[1]))

        new_results = [elm[0] for elm in zip_values]

        return self.copy(deep=True, update=dict(results=new_results))

    def return_results(self, spin=False) -> List:
        sample_list = self.results
        result_list = []
        for elm in sample_list:
            result_list.append((elm.num_occurrences, elm.bitstring))

        if spin:
            result_spin_list = []
            for elm in result_list:
                sample_list = []
                for elm2 in elm[1]:
                    if elm2 == 0:
                        sample_list.append(1)
                    elif elm2 == 1:
                        sample_list.append(-1)
                result_spin_list.append((elm[0], sample_list))
            return result_spin_list
        else:
            return result_list

    def lowest_energy(self) -> float:
        """Returns lowest energy"""
        return self.results[0].energy

    def lowest_energy_bitstrings(self) -> List:
        """Returns all the bitstrings with the lowest energy"""
        # these are sorted, so result[0] has the lowest energy
        result = [elm for elm in self.results if elm.energy == self.results[0].energy]
        return result

    # def plot_histogram(self) -> None:
    #     """Plots histogram
    #     """
    #     import matplotlib.pyplot as plt
    #     histo_data = []

    #     for sample in self.results:
    #         histo_data += [
    #             sample.energy,
    #         ] * sample.num_occurrences

    #     plt.style.use('ggplot')
    #     plt.hist(histo_data, bins=len(self.results))

    #     plt.title('Results histogram')
    #     plt.xlabel('Energy')
    #     plt.ylabel('Frequency')

    #     plt.show()

    def results_original_notation(self) -> List[Dict]:
        """Plots histogram"""
        results_ori = []

        for elm in self.results:
            bitstring_sample = elm.bitstring
            original_mapping = self.original_problem.qubovert.mapping
            dict_sample = {}
            for dict_elm in original_mapping:
                dict_sample[dict_elm] = bitstring_sample[original_mapping[dict_elm]]

            results_ori.append(dict_sample)

        return results_ori

    def name(self) -> str:
        """Returns the name of the quadratic program."""
        return "results_of_" + self.original_problem.name

    def set_output_data(self, output_data: Dict) -> None:
        """Sets the output data of the quadratic program.
        Args:
            output_data: The output data of the quadratic program.
        """
        return self.copy(deep=True, update=dict(backend_data_finish=output_data))

    def has_result_with_energy(self, bitstring: List[int], energy: float) -> bool:
        """
        Returns whether or not there exists in the list of results a bitstring
        with the given energy.
        """
        results = [
            x for x in self.results if x.bitstring == bitstring and x.energy == energy
        ]
        return len(results) > 0

    @classmethod
    def from_wire(cls, d: Dict):
        remapped_dict = d.copy()
        remapped_dict["original_problem"] = BinaryProblem.from_wire(
            d["original_problem"]
        )
        return cls(**remapped_dict)
