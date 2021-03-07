from typing import Dict, Tuple, Set, Union, Optional
import qubovert as qv
from qcware.types.optimization.problem_spec.utils import \
    polynomial_validation as validator
from qcware.types.optimization.variable_types import Domain


class PolynomialObjective:
    """Integer-valued polynomial of binary variables with int coefficients.

    Objects of this class specify polynomials of some number of
    binary variables with integer coefficients. "Binary variables" can either
    mean variables taking on the values 0 and 1 or variables taking on the
    values 1 and -1. The former a referred to as boolean variables and the
    latter are referred to as spin variables

    Objects of this class are meant to be treated as objective functions
    for optimization. They do not know about constraints. Constraints
    can be specified separately using a Constraints object.

    Polynomials are specified with a dict that specifies the coefficients
    for the polynomial. For example, suppose that we are interested
    in the polynomial of three boolean variables defined by::

        p(x, y, z) = 12 x - 2 y z + x y z - 50

    The three variables should be associated with the integers 0, 1, and 2.
    We choose the association x ~ 0, y ~ 1, and z ~ 2.

    There are four terms in p. Consider the term -2yz. We can specify this
    term by matching the tuple (1, 2), which represents yz, with the
    coefficient -2. This can be encoded with an entry in a dict (1, 2): -2.
    Overall, p can be defined by::

        {
            (): -50,
            (0,): 12,
            (1, 2): -2,
            (0, 1, 2): -50
        }

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
        polynomial: The polynomial is specified by a dict as described above.
            We only use tuples of int as keys and the range of ints must
            be from 0 to `num_variables - 1`. Values for the dict must be
            type int. This is because we are only treating integer-coefficient
            polynomials.

        variables: Set of ints representing the variables.

        num_variables: The number of variables for the polynomial. This number
            can be larger than the actual number of variables that appear
            in `polynomial` but it cannot be smaller.

        degree: The degree of the polynomial. This is not the mathematically
            correct degree. It is instead the length of the longest key in
            the polynomial dict or -inf in the case when the dict is {}.
            For example, the boolean PolynomialObjective {(1,): 12, (0, 1): 0}
            has mathematical degree 1 but the attribute `degree` is 2.

        domain: Specifies if variables take on boolean (0, 1) or spin (1, -1)
            values.
    """
    polynomial: Dict[Tuple[int, ...], int]
    variables: Set[int]
    num_variables: int
    degree: Union[int, float]
    domain: Domain

    def __init__(self,
                 polynomial: Dict[Tuple[int, ...], int],
                 num_variables: int,
                 domain: Union[Domain, str] = Domain.BOOLEAN,
                 variable_name_mapping: Optional[Dict[int, str]] = None,
                 validate_types: bool = True):
        self.num_variables = num_variables
        self.domain = Domain(domain.lower())

        parsed_polynomial = validator.polynomial_validation(
            polynomial=polynomial,
            num_variables=num_variables,
            validate_types=validate_types)

        self.polynomial = parsed_polynomial.poly
        self.variables = parsed_polynomial.variables
        self.degree = parsed_polynomial.deg
        if self.degree < 0:
            self.degree = float('-inf')

        self.variable_name_mapping = variable_name_mapping

        def default_symbol(variable_type: Domain):
            if variable_type is Domain.BOOLEAN:
                return 'x'
            elif variable_type is Domain.SPIN:
                return 'z'

        if variable_name_mapping is None:
            symbol = default_symbol(self.domain)
            self.variable_name_mapping = {
                i: f'{symbol}_{i}'
                for i in range(num_variables)
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
        out += '    num_variables=' + str(self.num_variables) + '\n'
        out += '    domain=' + repr(self.domain)
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
            num_variables=self.num_variables,
            domain=self.domain,
            validate_types=False)

    def qubovert(self, use_variable_names: bool = False):
        """Get a qubovert model describing this polynomial.

        This method will return a qubovert PUBO or PUSO depending on
        the domain of the variables.

        Args:
            use_variable_names: When True, the variables in the qubovert
                object will use the same string names as appear in
                the attribute variable_name_mapping.
        """
        if use_variable_names:
            polynomial = dict()
            for k, v in self.polynomial.items():
                new_key = tuple(self.variable_name_mapping[i] for i in k)
                polynomial[new_key] = v
        else:
            polynomial = self.polynomial

        if self.domain is Domain.BOOLEAN:
            model = qv.PUBO(polynomial)
        elif self.domain is Domain.SPIN:
            model = qv.PUSO(polynomial)
        else:
            raise RuntimeError('Domain is not valid.')
        if use_variable_names:
            model.set_reverse_mapping(self.variable_name_mapping)
        return model

    def simplified(self, preserve_num_variables=True
                   ) -> Tuple['PolynomialObjective', dict]:
        """Get a simplified copy of the PolynomialObjective.

        Args:
            preserve_num_variables: If True, the resulting PolynomialObjective will
            have the same number of variables stored as the original PolynomialObjective.
            Otherwise, num_variables will match the actual number of variables
            that appear in the polynomial with nonzero coefficients.

        """
        if preserve_num_variables:
            num_vars = self.num_variables
            mapping = {i: i for i in range(num_vars)}
            if self.domain is Domain.BOOLEAN:
                simplified_qv = qv.utils.PUBOMatrix(self.polynomial)
            elif self.domain is Domain.SPIN:
                simplified_qv = qv.utils.PUSOMatrix(self.polynomial)
            else:
                raise RuntimeError(f"Domain {self.domain} seems invalid.")

            return (
                PolynomialObjective(polynomial=simplified_qv,
                                    num_variables=num_vars,
                                    domain=self.domain,
                                    validate_types=False,
                                    variable_name_mapping=self.variable_name_mapping
                                    ),
                mapping
            )

        # This annoying block fixes a bug that arises when there are trivial
        # zero terms in the polynomial... we may end up deleting zero terms
        # upon initialization because of this.
        raw_polynomial = self.polynomial.copy()
        for term, coef in self.polynomial.items():
            if coef == 0:
                del raw_polynomial[term]

        if self.domain is Domain.BOOLEAN:
            qv_form = qv.PUBO(raw_polynomial)
        elif self.domain is Domain.SPIN:
            qv_form = qv.PUSO(raw_polynomial)
        else:
            raise RuntimeError(f"Domain {self.domain} seems invalid.")

        simplified_qv = qv_form.to_enumerated()
        mapping = qv_form.mapping
        num_vars = simplified_qv.num_binary_variables

        return (
            PolynomialObjective(polynomial=simplified_qv,
                                num_variables=num_vars,
                                domain=self.domain,
                                validate_types=False),
            mapping
        )

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

        if self.domain is Domain.BOOLEAN:
            res = f"Boolean Variables: "
        elif self.domain is Domain.SPIN:
            res = f"Spin Variables: "
        else:
            raise RuntimeError("Variable domain type seems to be invalid.")

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
            'num_variables': self.num_variables,
            'domain': self.domain.lower()
        }


if __name__ == '__main__':
    pass
