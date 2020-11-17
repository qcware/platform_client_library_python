import pydantic
from typing import Optional, List
from . import utils


class BruteOptimizeResult(pydantic.BaseModel):
    """Return type for brute force maximization and minimization.

    When solution_exists == False, we must have value is None and
    arguments == [].
    """
    value: Optional[int] = None
    arguments: List[str] = []
    solution_exists: bool = True

    @pydantic.validator('solution_exists', always=True)
    def no_solution_check(cls, sol_exists, values):
        if not sol_exists:
            if not values['value'] is None:
                raise ValueError('Value given but solution_exists=False.')
            if not values['arguments'] == []:
                raise ValueError('arguments given but solution_exists=False.')

        else:
            if values['value'] is None or values['arguments'] == []:
                raise ValueError(
                    'solution_exists=True, but no solution was specified.'
                )
        return sol_exists

    def int_argument(self) -> List[List[int]]:
        """Convert arguments to a list of list of ints."""
        return [[int(x) for x in s] for s in self.arguments]

    @property
    def num_variables(self):
        if not self.solution_exists:
            return
        return len(self.arguments[0])

    def __repr__(self):
        if self.solution_exists:
            out = 'forge.return_types.BruteOptimizeResult(\n'
            out += f'value={self.value}\n'
            char_estimate = self.num_variables * len(self.arguments)
            out += utils.short_list_str(
                self.arguments, char_estimate, 'arguments'
            )
            return out + '\n)'
        else:
            return (
                'forge.return_types.BruteOptimizeResult(solution_exists=False)')
