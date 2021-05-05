from pydantic import BaseModel, conint, ValidationError, validator
from typing import List, Union, Dict, Tuple, Any
import qubovert as qv
import numpy as np
from ...types.optimization import PolynomialObjective
from .problem_spec import Constraints
from ...types.optimization.predicate import Predicate

from ...types.optimization.variable_types import Domain

BinaryProblemTerms = Union[PolynomialObjective]
BinaryConstraintTerms = Union[Constraints]


class BinaryProblem(BaseModel):
    Q_dict: BinaryProblemTerms

    constraints: Any = None

    name: str = 'my_qcware_binary_problem'

    class Config:
        validate_assignment = True
        allow_mutation = False

    def __str__(self) -> str:
        '''Print the problem in a nice way'''

        header0 = '* Name: {0} *\n'.format(self.name)
        header1 = '* Variable type: {0} *\n'.format(self.Q_dict.domain)
        line = '**********************\n'
        header2 = 'Objective function: {0} \n'.format(self.Q_dict.polynomial)

        string_out = line + header0 + header1 + line + header2

        if self.constraints != None:

            string_out += self.constraints.__repr__()

        return string_out

    @classmethod
    def from_q(cls, Q: Dict[Tuple[int, ...], float]):
        """
        Creates the BinaryProblem from an old-style Q-matrix
        """
        num_var = qv.QUBO(Q).num_binary_variables
        qubo = PolynomialObjective(polynomial=Q,
                                   num_variables=num_var,
                                   domain='boolean')

        return cls(Q_dict=qubo)

    def set_name(self, name: str) -> None:
        """Sets the name of the quadratic program.
        Args:
            name: The name of the quadratic program.
        """

        return self.copy(deep=True, update=dict(name=name))

    def dwave_Q(self):
        """Returns a dict valid for D-Wave problems
        """
        Q_start = self.Q_dict.polynomial

        Q_final = {}
        for elm in Q_start.keys():
            if elm == ():
                pass
            elif len(elm) == 1:
                Q_final[(elm[0], elm[0])] = Q_start[(elm[0], )]
            else:
                Q_final[elm] = Q_start[elm]

        return Q_final


class BinarySample(BaseModel):
    bitstring: List[int]
    energy: float = None
    num_occurrences: int

    @validator('bitstring')
    def bitstring_must_be_01(cls, v):
        for elm in v:
            if elm != 0 and elm != 1:
                raise ValueError('Bitstring values must be 0 or 1')
        return v

    class Config:
        validate_assignment = True
        allow_mutation = False

    def __str__(self) -> str:
        '''Print the problem in a nice way'''
        header0 = '* Bitstring: {0} *\n'.format(self.bitstring)
        header1 = '* Energy: {0} *\n'.format(self.energy)
        header2 = '* Number of ocurrences: {0} *\n'.format(
            self.num_occurrences)

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
    """
    original_problem: BinaryProblem

    backend_data_start: Dict[str, Union[str, int, float, Dict, List, None]]

    backend_data_finish: Dict[str, Union[str, int, float, Dict, List,
                                         None]] = {}

    results: List[BinarySample] = []

    class Config:
        validate_assignment = True
        allow_mutation = False

    def __str__(self) -> str:
        '''Print the problem in a nice way'''
        title = 'Name: {0} \n'.format('results_of_' +
                                      self.original_problem.name)
        header0 = 'Lowest energy sample:\n'
        if len(self.results) == 0:
            header1 = 'Empty'

            return title + header0 + header1
        else:
            lowest_energy = self.results[0].energy

            header1 = str(self.results[0])

            for elm in self.results[1:]:
                if elm.energy == lowest_energy:
                    header1 += str(elm)
                else:
                    break

            num_occurrences_results = [
                elm.num_occurrences for elm in self.results
            ]
            header2 = 'Number of Samples: {0} \n'.format(
                sum(num_occurrences_results))
            header3 = 'Number of Unique Samples: {0} \n'.format(
                len(self.results))

            string_out = title + header0 + header1 + header2 + header3

            return string_out

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

            return self.original_problem.Q_dict.qubovert().value(x)

        def sort_bin(b):
            'Orders bitstrings'
            b_view = np.ascontiguousarray(b).view(
                np.dtype((np.void, b.dtype.itemsize * b.shape[1])))
            return np.argsort(b_view.ravel())

        sample_bitstring = sample.bitstring

        # First assert that the solution is the same length as the problem
        assert len(
            sample_bitstring) == self.original_problem.Q_dict.num_variables

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
                    new_sample = BinarySample(bitstring=sample.bitstring,
                                              energy=new_results[elm].energy,
                                              num_occurrences=new_frequency)
                    # Remove the old sample
                    new_results.remove(new_results[elm])
                    # Add new sample
                    new_results.append(new_sample)
                    break
        else:
            # If bitstring not there just add
            # But first calculate energy
            sample = sample.set_energy(
                calculate_energy(bitstring=sample_bitstring))
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
        """Returns lowest energy
        """
        return self.results[0].energy

    def lowest_energy_bitstrings(self) -> List:
        """Returns all the bitstrings with the lowest energy
        """
        # these are sorted, so result[0] has the lowest energy
        result = [
            elm for elm in self.results if elm.energy == self.results[0].energy
        ]
        return result

    def variable_mapping(self) -> Dict:
        """Returns variable mapping
        """
        return self.original_problem.qubovert.mapping

    def reverse_mapping(self) -> Dict:
        """Returns reverse variable mapping
        """
        return self.original_problem.qubovert.reverse_mapping

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
        """Plots histogram
        """
        results_ori = []

        for elm in self.results:
            bitstring_sample = elm.bitstring
            original_mapping = self.original_problem.qubovert.mapping
            dict_sample = {}
            for dict_elm in original_mapping:
                dict_sample[dict_elm] = bitstring_sample[
                    original_mapping[dict_elm]]

            results_ori.append(dict_sample)

        return results_ori

    def name(self) -> str:
        """Returns the name of the quadratic program.
        """
        return 'results_of_' + self.original_problem.name

    def set_output_data(self, output_data: Dict) -> None:
        """Sets the output data of the quadratic program.
        Args:
            output_data: The output data of the quadratic program.
        """
        return self.copy(deep=True,
                         update=dict(backend_data_finish=output_data))

    def has_result_with_energy(self, bitstring: List[int],
                               energy: float) -> bool:
        """
        Returns whether or not there exists in the list of results a bitstring
        with the given energy.
        """
        results = [
            x for x in self.results
            if x.bitstring == bitstring and x.energy == energy
        ]
        return len(results) > 0

    @classmethod
    def from_wire(cls, d: Dict):
        remapped_dict = d.copy()
        remapped_dict['original_problem'] = BinaryProblem.from_wire(
            d['original_problem'])
        return cls(**remapped_dict)
