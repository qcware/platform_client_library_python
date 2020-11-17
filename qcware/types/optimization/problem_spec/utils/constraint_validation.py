import pydantic
import dataclasses
from typing import Dict, List
from qcware.types.optimization.predicate import Predicate

from qcware.types.optimization.problem_spec import PolynomialObjective


def constraint_validation(constraints: dict,
                          num_variables: int,
                          validate_types: bool = True):
    from qcware.types.optimization import Predicate

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

            for pubo_list in self.constraint_dict.values():
                for p in pubo_list:
                    if p.num_boolean_variables != self.num_vars:
                        raise RuntimeError(
                            f'Found a constraint for {p.num_boolean_variables} '
                            f'variables, but expected {self.num_vars} '
                            f'variables.')

    return _ConstraintValidation(constraint_dict=constraints,
                                 num_vars=num_variables)


if __name__ == '__main__':
    p = PUBO({}, 2)
    constraint_validation({Predicate.ZERO: [p]}, 2)
