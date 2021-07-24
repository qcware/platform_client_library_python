from pydantic import BaseModel
from typing import Dict, Tuple, Optional

from .. import Predicate, Domain

from . import PolynomialObjective
from . import Constraints


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
    def domain(self):
        """The domain (boolean or spin) for the problem instance."""
        return self.objective.domain

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
