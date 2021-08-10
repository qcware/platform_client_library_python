import pydantic
import dataclasses
from typing import Dict, List, Optional, Union

from qcware.types.utils import pydantic_model_abridge_validation_errors

from qcware.types.optimization.predicate import Predicate
from qcware.types.optimization.variable_types import Domain
from qcware.types.optimization.problem_spec import PolynomialObjective


def constraint_validation(
    constraints: dict,
    num_variables: int,
    validate_types: bool = True,
    domain: Optional[Union[Domain, str]] = None,
    variable_name_mapping: Optional[Dict[int, str]] = None,
):
    if domain is not None:
        domain = Domain(domain.lower())
    for p_list in constraints.values():
        for i, p in enumerate(p_list):
            if not isinstance(p, PolynomialObjective):
                if domain is None:
                    domain = Domain.BOOLEAN
                p_list[i] = PolynomialObjective(
                    polynomial=p,
                    num_variables=num_variables,
                    domain=domain,
                    variable_name_mapping=variable_name_mapping,
                    validate_types=validate_types,
                )

    # By changing from a pydantic.dataclass to a vanilla dataclass,
    # we are able to turn off type checking while still using __post_init__.
    if validate_types:
        dataclass_selection = pydantic.dataclasses.dataclass
        int_type = pydantic.StrictInt
    else:
        dataclass_selection = dataclasses.dataclass
        int_type = int

    @dataclass_selection
    class _ConstraintValidation:
        constraint_dict: Dict[Predicate, List[PolynomialObjective]]
        num_vars: int_type

        def __post_init__(self):
            fixed_key_dict = {}
            for k, v in self.constraint_dict.items():
                fixed_key_dict.update({Predicate(k.lower()): v})
            self.constraint_dict = fixed_key_dict

            removals = set()
            for predicate, pubo_list in self.constraint_dict.items():
                if len(pubo_list) == 0:
                    removals.add(predicate)
                for p in pubo_list:
                    if p.num_variables != self.num_vars:
                        raise RuntimeError(
                            f"Found a constraint for {p.num_variables} "
                            f"variables, but expected {self.num_vars} "
                            f"variables."
                        )

            for pred in removals:
                self.constraint_dict.pop(pred)

    return pydantic_model_abridge_validation_errors(
        model=_ConstraintValidation,
        max_num_errors=10,
        constraint_dict=constraints,
        num_vars=num_variables,
    )
