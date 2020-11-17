from typing import Dict, Tuple, Set, Union, Optional
import qubovert as qv
from qcware.types.optimization.problem_spec.utils import \
    polynomial_validation as validator


class PolynomialObjective:
    """Integer-valued polynomial of boolean variables with int coefficients.

    Objects of this class specify polynomials of some number of
    boolean variables with integer coefficients. When we use the term
    "boolean", we mean that variables take on the values 0 and 1. These
    are pseudo-boolean functions.

    Objects of this class are meant to be treated as objective functions
    for optimization. They do not know about constraints. Constraints
    can be specified separately using a Constraints object.

    Polynomials are specified with a dict that specifies the coefficients
    for the polynomial. For example, suppose that we are interested
    in the polynomial of three boolean variables defined by

    p(x, y, z) = 12 x - 2 y z + x y z - 50

    The three variables should be associated with the integers 0, 1, and 2.
    We choose the association x ~ 0, y ~ 1, and z ~ 2.

    There are four terms in p. Consider the term -2yz. We can specify this
    term by matching the tuple (1, 2), which represents yz, with the
    coefficient -2. This can be encoded with an entry in a dict (1, 2): -2.
    Overall, p can be defined by
        {
        (): -50,
        (0,): 12,
        (1, 2): -2,
        (0, 1, 2): -50
        }
    .

    Note that this object does not automatically simplify a given
    PolynomialObjective. For example, {(0, 1): 2, (1, 0): 3} is the same
    thing as {(0, 1): 5}. However, we do provide a `simplified` method
    returns a version of the same polynomial with simplifications performed.

    The number of variables must be specified explicitly, even if it seems
    obvious how many variables there are. The reason for this is to allow
    for the possibility that there are more variables than appear explicitly
    in the polynomial. For example, the polynomial p(a, b) = 12 b might be
    mistaken for q(b) = 12 b.

    Attributes:
        polynomial: The polynomial is specified by a dict in the standard way.
            We only use tuples of int as keys and the range of ints must
            be from 0 to `num_boolean_variables - 1`. Values for the dict must be
            type int. This is because we are only treating integer-coefficient
            polynomials.

        variables: Set of ints representing variables.

        num_boolean_variables: The number of variables for the polynomial. This number
            can be larger than the actual number of variables that appear
            in pubo.

        degree: The degree of the polynomial. This is not the mathematically
            correct degree. It is instead the length of the longest key in
            the pubo dict or -inf in the case when the pubo dict is {}.
            For example, the PolynomialObjective {(1,): 12, (0, 1): 0} has
            mathematical degree 1 but the attribute `degree` is 2.
    """
    polynomial: Dict[Tuple[int, ...], int]
    variables: Set[int]
    num_boolean_variables: int
    degree: Union[int, float]

    def __init__(self,
                 polynomial: Dict[Tuple[int, ...], int],
                 num_boolean_variables: int,
                 variable_name_mapping: Optional[Dict[int, str]] = None,
                 validate_types: bool = True):
        self.num_boolean_variables = num_boolean_variables

        parsed_polynomial = validator.polynomial_validation(
            polynomial=polynomial,
            num_variables=num_boolean_variables,
            validate_types=validate_types)
        self.polynomial = parsed_polynomial.poly
        self.variables = parsed_polynomial.variables
        self.degree = parsed_polynomial.deg

        self.variable_name_mapping = variable_name_mapping
        if variable_name_mapping is None:
            self.variable_name_mapping = {
                i: f'x_{i}'
                for i in range(num_boolean_variables)
            }

    def to_wire(self) -> Dict:
        result = self.dict()

        def remap_q_indices_to_strings(Q: dict) -> dict:
            return {str(k): v for k, v in Q.items()}

        result['polynomial'] = remap_q_indices_to_strings(result['polynomial'])
        return result

    @classmethod
    def from_wire(cls, d: Dict):
        # I copy this so that changes don't affect the original,
        # not that it matters much here
        remapped_dict = d.copy()

        def string_to_int_tuple(s: str):
            term_strings = s.split(',')
            if term_strings[-1] == '':
                term_strings = term_strings[:-1]
            return tuple(map(int, term_strings))

        def remap_q_indices_from_strings(q_old: dict) -> dict:
            q_new = {
                string_to_int_tuple(k[1:-1].strip(", ")): v
                for k, v in q_old.items()
            }
            return q_new

        remapped_dict['polynomial'] = remap_q_indices_from_strings(
            d['polynomial'])
        return cls(**remapped_dict)

    def keys(self):
        return self.polynomial.keys()

    def values(self):
        return self.polynomial.values()

    def items(self):
        return self.polynomial.items()

    def __iter__(self):
        return self.polynomial.__iter__()

    def __repr__(self):
        out = 'PolynomialObjective(\n'
        out += '    polynomial=' + self.polynomial.__repr__() + '\n'
        out += '    num_boolean_variables=' + str(self.num_boolean_variables)
        out += '\n)'
        return out

    def __str__(self):
        return self.pretty_str()

    def __getitem__(self, item):
        return self.polynomial.__getitem__(item)

    def clone(self):
        """Make a copy of this PolynomialObjective."""
        return PolynomialObjective(
            polynomial=self.polynomial,
            num_boolean_variables=self.num_boolean_variables,
            validate_types=False)

    def simplified(self, preserve_num_variables=True) -> 'PolynomialObjective':
        """Get a simplified copy of the PolynomialObjective.

        Args:
            preserve_num_variables: If True, the resulting PolynomialObjective will
            have the same number of variables stored as the original PolynomialObjective.
            Otherwise, num_boolean_variables will match the actual number of variables
            that appear in the polynomial with nonzero coefficients.
        """
        simplified_qv = qv.utils.PUBOMatrix(self.polynomial)
        num_vars = simplified_qv.num_binary_variables
        if preserve_num_variables:
            num_vars = self.num_boolean_variables

        return PolynomialObjective(polynomial=simplified_qv,
                                   num_boolean_variables=num_vars,
                                   validate_types=False)

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_type

    @classmethod
    def validate_type(cls, v):
        """
        This validator only confirms that we are dealing with an object
        of the expected type. This does not validate internal consistency
        of attributes for the Objective function because that is done
        by __init__.

        """
        if not isinstance(v, PolynomialObjective):
            raise TypeError(
                'Expected an object of class PolynomialObjective, but found '
                f'{type(v)}.')
        return v

    def pretty_str(self):
        """Make a string that presents the polynomial algebraically.

        The names of variables can be controlled with the attribute
        variable_name_mapping.

        Adapted from qubovert--thanks to Joseph T. Iosue.
        """
        if self.polynomial == {}:
            return ''

        res = f"Boolean Variables: "
        res += f"{list(self.variable_name_mapping.values())}\n"
        first = True
        for term, coef in self.items():
            if coef >= 0 and (coef != 1 or not term):
                res += f'{coef} '
            elif coef < 0:
                if coef == -1:
                    if first:
                        res += "-" if term else "-1 "
                    else:
                        res = res[:-2] + ('- ' if term else "- 1 ")
                else:
                    if first:
                        res += f'{coef} '
                    else:
                        res = res[:-2] + f'- {abs(coef)} '

            for x in term:

                res += self.variable_name_mapping[x] + ' '
            res += "+ "
            first = False
        return res[:-2].strip()

    def dict(self):
        return {
            'polynomial': self.polynomial,
            'num_boolean_variables': self.num_boolean_variables,
        }


if __name__ == '__main__':
    pass
