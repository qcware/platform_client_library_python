from typing import Dict, Tuple, Set, Union, Optional
import qubovert as qv
from icontract import require
from qcware.types.optimization.problem_spec.utils import (
    polynomial_validation as validator,
)
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
    variable_name_mapping: Dict[int, str]

    #    @require(lambda polynomial: len(polynomial) > 0)
    def __init__(
        self,
        polynomial: Dict[Tuple[int, ...], int],
        num_variables: int,
        domain: Union[Domain, str] = Domain.BOOLEAN,
        variable_name_mapping: Optional[Dict[int, str]] = None,
        validate_types: bool = True,
    ):
        # TODO: introduce mapping structure to guarantee consistent variable
        #   reduction. This is also critical because we don't want
        #   reduction to annoyingly re-order variables when it's not necessary.
        self.num_variables = num_variables
        self.domain = Domain(domain.lower())
        polynomial = simplify_polynomial(polynomial, self.domain)

        parsed_polynomial = validator.polynomial_validation(
            polynomial=polynomial,
            num_variables=num_variables,
            validate_types=validate_types,
        )

        self.polynomial = parsed_polynomial.poly
        self.active_variables = parsed_polynomial.variables
        self.num_active_variables = len(self.active_variables)
        self.degree = parsed_polynomial.deg
        if self.degree < 0:
            self.degree = float("-inf")

        self.variable_name_mapping = variable_name_mapping

        def default_symbol(variable_type: Domain):
            if variable_type is Domain.BOOLEAN:
                return "x"
            elif variable_type is Domain.SPIN:
                return "z"

        if variable_name_mapping is None:
            symbol = default_symbol(self.domain)
            self.variable_name_mapping = {
                i: f"{symbol}_{i}" for i in range(num_variables)
            }

        # We use qubovert to compute function values. Since we don't want
        # to reconstruct a qubovert object every time we use it, we keep
        # these private attributes around to use as a cache.
        self._qv_polynomial = None
        self._qv_polynomial_named = None

    def keys(self):
        return self.polynomial.keys()

    def values(self):
        return self.polynomial.values()

    def items(self):
        return self.polynomial.items()

    def __iter__(self):
        return self.polynomial.__iter__()

    def __repr__(self):
        out = "PolynomialObjective(\n"
        out += "    polynomial=" + self.polynomial.__repr__() + "\n"
        out += "    num_variables=" + str(self.num_variables) + "\n"
        out += "    domain=" + repr(self.domain) + "\n"
        out += "    variable_mapping=" + repr(self.variable_name_mapping)
        out += "\n)"
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
            variable_name_mapping=self.variable_name_mapping.copy(),
            validate_types=False,
        )

    def qubovert(self, use_variable_names: bool = False):
        """Get a qubovert model describing this polynomial.

        This method will return a qubovert PUBO or PUSO depending on
        the domain of the variables.

        This method creates a cached qubovert object once it is called.
        TODO: This fact makes it particularly important that
            PolynomialObjective is immutable. We should try to enforce this.

        Args:
            use_variable_names: When True, the variables in the qubovert
                object will use the same string names as appear in
                the attribute variable_name_mapping.
        """
        if not use_variable_names:
            if self._qv_polynomial is None:
                self._qv_polynomial = self._qubovert(use_variable_names=False)
            return self._qv_polynomial

        else:
            if self._qv_polynomial_named is None:
                self._qv_polynomial_named = self._qubovert(use_variable_names=True)
            return self._qv_polynomial_named

    def _qubovert(self, use_variable_names: bool = False):
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
            raise RuntimeError("Domain is not valid.")
        if use_variable_names:
            model.set_reverse_mapping(self.variable_name_mapping)
        return model

    def qubovert_boolean(self):
        """Get a boolean qubovert model equivalent to this polynomial.

        This produces a PUBOMatrix which is qubovert's enumerated form of a
        PUBO (polynomial unconstrained boolean optimization). This
        transformation may change the variable ordering and for that
        reason we also return a mapping that can be used to recover
        the original variable identifiers.
        """
        qv_model = self.qubovert(use_variable_names=False)
        return {"polynomial": qv_model.to_pubo(), "mapping": qv_model.mapping}

    def qubovert_spin(self):
        """Get a spin qubovert model equivalent to this polynomial.

        This produces a PUSOMatrix which is qubovert's enumerated form of a
        PUSO (polynomial unconstrained spin optimization). This transformation
        may change the variable ordering and for that
        reason we also return a mapping that can be used to recover
        the original variable identifiers.
        """
        qv_model = self.qubovert(use_variable_names=False)
        return {"polynomial": qv_model.to_puso(), "mapping": qv_model.mapping}

    def reduce_variables(self):
        """Return a PolynomialObjective with trivial variables removed.

        As an example, suppose that we have a PolynomialObjective defined by

        PolynomialObjective(
            polynomial={(1,): 1},
            num_variables=3
        )

        which essentially means the polynomial p defined by p(x, y, z) = y.
        This has two variables that p doesn't actually depend on. In this
        case, the method `reduce_variables` will return a polynomial of one
        variable along with a mapping to identify variables appropriately.
        Specifically, in this case the return would be

        {
            'polynomial': PolynomialObjective(polynomial={(0,): 1},
                                              num_variables=1
                                              )
            'mapping': {1: 0}
        }.
        """
        qv_form = self.qubovert(use_variable_names=False)
        reduced_qv = qv_form.to_enumerated()
        mapping = qv_form.mapping
        num_vars = reduced_qv.num_binary_variables

        return {
            "polynomial": PolynomialObjective(
                polynomial=reduced_qv,
                num_variables=num_vars,
                domain=self.domain,
                variable_name_mapping=None,
                validate_types=False,
            ),
            "mapping": mapping,
        }

    def compute_value(self, variable_values: dict, use_variable_names: bool = False):
        """Compute the value of this polynomial at a specified input."""
        qv_polynomial = self.qubovert(use_variable_names=use_variable_names)
        return qv_polynomial.value(variable_values)

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
                "Expected an object of class PolynomialObjective, but found "
                f"{type(v)}."
            )
        return v

    def pretty_str(self, include_domain: bool = True):
        """Make a string that presents the polynomial algebraically.

        The names of variables can be controlled with the attribute
        variable_name_mapping.

        Adapted from qubovert--thanks to Joseph T. Iosue.
        """
        if self.domain is Domain.BOOLEAN:
            domain_label = f"({self.num_variables} boolean variables)"
        elif self.domain is Domain.SPIN:
            domain_label = f"({self.num_variables} spin variables)"
        else:
            raise RuntimeError("Variable domain type seems to be invalid.")

        if self.polynomial == {}:
            if include_domain:
                return "0  " + domain_label
            else:
                return "0"

        res = ""
        first = True
        for term, coef in self.items():
            if coef >= 0 and (coef != 1 or not term):
                res += f"{coef} "
            elif coef < 0:
                if coef == -1:
                    if first:
                        res += "-" if term else "-1 "
                    else:
                        res = res[:-2] + ("- " if term else "- 1 ")
                else:
                    if first:
                        res += f"{coef} "
                    else:
                        res = res[:-2] + f"- {abs(coef)} "

            for x in term:

                res += self.variable_name_mapping[x] + " "
            res += "+ "
            first = False
        res = res[:-2].strip()

        if include_domain:
            return res + "  " + domain_label
        else:
            return res

    def dict(self):
        return {
            "polynomial": self.polynomial,
            "num_variables": self.num_variables,
            "domain": self.domain.lower(),
            "variable_name_mapping": self.variable_name_mapping,
        }


def simplify_polynomial(polynomial: dict, domain: Domain) -> dict:
    """Simplify given polynomial dict."""
    domain = Domain(domain.lower())
    if domain is Domain.BOOLEAN:
        simplified_qv = qv.utils.PUBOMatrix(polynomial)
    elif domain is Domain.SPIN:
        simplified_qv = qv.utils.PUSOMatrix(polynomial)
    else:
        raise TypeError(f"Expected a Domain but found {type(domain)}.")

    return dict(simplified_qv)
