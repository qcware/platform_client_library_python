import textwrap
from typing import Dict, List, Union, Iterable, Optional

import tabulate
from qcware.types.optimization.predicate import Predicate
from qcware.types.optimization.variable_types import Domain
from qcware.types.optimization import utils
from qcware.types.optimization.problem_spec import PolynomialObjective
from qcware.types.optimization.problem_spec.utils import \
    constraint_validation as validator


class Constraints:
    """Specification of constraints on binary variables.

    An object of class Constraints does not have information about the
    objective function on which the constraints are applied. It is simply a
    collection of constraints which can then be imposed on something.

    To specify constraints, we use a "constraint dict". The format
    of this dict is::
      
        {type of constraint: list of constraints of that type}.

    The "type of constraint" means a `Predicate` object. The list of
    constraints of a given `Predicate` are a list of `PolynomialObjective` s.

    This can be understood fairly easily by example. Suppose that f is an
    PolynomialObjective with 3 boolean variables. We take::

        f(x, y, z) = (x + y + z - 1)^2

    which is minimized when exactly one of the three variables is 1.

    If we want to impose the condition that either x or z is zero,
    we can roughly use the constraint dict::

        {Predicate.ZERO: [p]}

    where p is the PolynomialObjective representing the function::

        p(x, y, z) = OR(x, z) = x + z - x z

    (To build this, see the documentation for PolynomialObjective.) If we
    additionally want to add the constraint that the sum of the three variables
    is at least 2, we can make our dict::

        {Predicate.ZERO: [p], Predicate.POSITIVE: [q]}

    where q is a PolynomialObjective representing `q(x, y, z) = x + y + z - 1`. The
    reason that we are using [p] and [q] instead of just p and q is that we can
    add additional constraints of those types in this fashion by adding
    more entries to the lists.
    """
    constraint_dict: Dict[Predicate, List[PolynomialObjective]]
    domain: Domain

    def __init__(self,
                 constraints: Dict[Predicate, List[PolynomialObjective]],
                 num_variables: int,
                 validate_types: bool = True):
        """
        Args:
            constraints: Constraints are specified with a dict from
                Predicate objects to lists of PolynomialObjective objects. All
                PolynomialObjective objects in the lists must have the same
                number of variables as this Constraints object has.

                Keys to the dict are Predicate objects that specify the
                type of constraint. The values of the dict are lists of
                PolynomialObjective objects. Here's an example:
                    {
                    Predicate.NEGATIVE: [p, q],
                    Predicate.ZERO: [r]
                    }
                    is a specification for three constraints. p, q, and r are
                    all objects of type PolynomialObjective. The constraints are

                    p(x) < 0, q(x) < 0, r(x) = 0  <==> x is feasible.

                The meaning of different Predicates are:
                    NONNEGATIVE   --   polynomial >= 0
                    POSITIVE      --   polynomial > 0
                    NONPOSITIVE   --   polynomial <= 0
                    NEGATIVE      --   polynomial < 0
                    ZERO          --   polynomial = 0
                    NONZERO       --   polynomial != 0

            num_variables: The number of binary variables that the
                constraints constrain.
        """
        parsed_constraints = validator.constraint_validation(
            constraints, num_variables, validate_types)
        del constraints
        self.constraint_dict = parsed_constraints.constraint_dict
        self.num_variables = num_variables
        self.predicates = set(self.constraint_dict)
        self.degree_dict = {rel: [] for rel in self.predicates}
        self.degree_set = set()
        self._total_num_constraints = 0
        self._num_constraints_dict = {rel: 0 for rel in self.predicates}

        selected_domain = None
        for predicate in self.predicates:
            for c in self.constraint_dict[predicate]:
                self.degree_dict[predicate].append(c.degree)
                self.degree_set.add(c.degree)
                self._total_num_constraints += 1
                self._num_constraints_dict[predicate] += 1
                if selected_domain is None:
                    selected_domain = c.domain
                elif selected_domain is not c.domain:
                    raise ValueError(
                        'Encountered constraints with both boolean and spin '
                        'variable domains.')

        self.domain = selected_domain
        self.max_degree_dict = {
            predicate: max(degs)
            for predicate, degs in self.degree_dict.items()
        }
        if self.constraint_dict == {}:
            self.max_degree = None
        else:
            self.max_degree = max(self.max_degree_dict.values())

    def to_wire(self) -> Dict:
        result = self.dict().copy()
        result['constraints'] = {
            k: [x.to_wire() for x in v]
            for k, v in self.dict()['constraints'].items()
        }
        print(result)
        return result

    @classmethod
    def from_wire(cls, d: Dict):
        remapped_dict = d.copy()
        remapped_dict['constraints'] = {
            k: [PolynomialObjective.from_wire(x) for x in v]
            for k, v in d['constraints'].items()
        }

        print('remapped:')
        print(remapped_dict)
        return cls(**remapped_dict)

    def get_constraint_group(self,
                             predicate: Predicate,
                             order: Union[int, Iterable[int], None] = None):
        """Iterate over constraints with specified predicate and order.

        If order is not specified, all orders are generated.
        """
        if order is None:
            order = range(self.max_degree_dict[predicate] + 1)
        elif isinstance(order, int):
            order = range(order, order + 1)
        if not utils.iterable(order):
            raise TypeError(f'Expected `order` to be int or iterable '
                            f'of int but got type {type(order)}.')

        for i, constraint in enumerate(self[predicate]):
            if constraint.degree in order:
                yield i, constraint

    def constraint_exists(self,
                          order: Union[int, Iterable[int], None] = None,
                          predicate: Optional[Predicate] = None):
        """Return True iff a constraint exists with given order or predicate.

        `order` can be an int or an iterable of ints. `predicate` is a
        Predicate object.

        If order and predicate are both None, this function returns True iff
        any constraint exists.
        """
        if order is None and predicate is None:
            return self.num_constraints() > 0
        if order is not None:
            if isinstance(order, int):
                if order < 0:
                    raise ValueError("Order must be non-negative.")
                order = range(order, order + 1)

        if order is None:
            # True iff constraint with given predicate exists.
            return self.num_constraints(predicate) > 0
        else:
            if predicate is None:
                degree_collection = self.degree_set
            else:
                try:
                    degree_collection = self.degree_dict[predicate]
                except KeyError:
                    return False
            for deg in degree_collection:
                if deg in order:
                    return True
            else:
                return False

    def num_constraints(self, predicate: Optional[Predicate] = None):
        """Return the number of constraints.

        If a predicate is specified, only return the number of constraints
        for that predicate.
        """
        if predicate is None:
            return self._total_num_constraints
        try:
            return self._num_constraints_dict[predicate]
        except KeyError:
            if isinstance(predicate, Predicate):
                return 0
            else:
                raise TypeError(f'Expected Predicate, found {type(predicate)}')

    def __len__(self):
        """Get the total number of constraints"""
        return self.num_constraints()

    def __iter__(self):
        return self.constraint_dict.__iter__()

    def __getitem__(self, item):
        return self.constraint_dict.__getitem__(item)

    def __repr__(self):
        out = f'Number of variables: {self.num_variables}\n'
        out += f'Total number of constraints: {self.num_constraints()}\n\n'
        header = ['Predicate', 'Number of Constraints', 'Highest Degree']
        data = [[
            rel.upper(),
            self.num_constraints(rel), self.max_degree_dict[rel]
        ] for rel in self.predicates]

        out += tabulate.tabulate(data, header)

        out = textwrap.indent(out, '    ', predicate=None)
        out = 'Constraints:\n' + out
        return out

    def dict(self):
        return {
            'constraints': self.constraint_dict,
            'num_variables': self.num_variables
        }


if __name__ == '__main__':

    def std_constraints_3vars(feasible):
        """Generate a standard constraint-specifying dict for three variables.

        If feasible is True, then this function generates four constraints
        for which there are two feasible points. If false, there is one
        more constraint that eliminates the feasible points.


        Summary of constraints:

            infeasible case:
            Number of binary variables: 3
            Total number of constraints: 6
            Predicate      Number of Constraints    Highest Degree
            ----------  -----------------------  ----------------
            NONZERO                           1                 3
            ZERO                              2                 2
            NEGATIVE                          2                 1
            POSITIVE                          1                 0

            feasible case:
            Number of binary variables: 3
            Total number of constraints: 5
            Predicate      Number of Constraints    Highest Degree
            ----------  -----------------------  ----------------
            EQ                                2                 2
            LT                                2                 1
            GT                                1                 0

        """
        neg_constraints = [
            # a + b + c < 3 (violated iff a=b=c=1)
            PolynomialObjective(polynomial={
                (): -3,
                (0, ): 1,
                (1, ): 1,
                (2, ): 1
            },
                              num_variables=3),
            # Always true
            PolynomialObjective(polynomial={(): -1}, num_variables=3),
        ]
        zero_constraints = [
            # (a+b+c-1)^2 == 0 (true iff exactly one variable is 1.)
            PolynomialObjective(polynomial={
                (0, 1): 2,
                (0, 2): 2,
                (1, 2): 2,
                (0, ): -1,
                (1, ): -1,
                (2, ): -1,
                (): 1
            },
                              num_variables=3),
            # a + c = 1 (true iff a XOR c)
            PolynomialObjective(polynomial={
                (0, ): 1,
                (2, ): 1,
                (): -1
            },
                              num_variables=3),
        ]
        pos_constraints = [
            # Always true
            PolynomialObjective(polynomial={(): 7}, num_variables=3),
        ]

        constraints = {
            Predicate.NEGATIVE: neg_constraints,
            Predicate.ZERO: zero_constraints,
            Predicate.POSITIVE: pos_constraints
        }

        if not feasible:
            constraints.update({
                Predicate.NONZERO: [
                    PolynomialObjective(polynomial={(0, 1, 2): 1},
                                        num_variables=3)
                ]
            })

        return Constraints(constraints, 3)

    con = std_constraints_3vars(True)
