import itertools

import pytest
from qcware.forge.optimization import brute_force_minimize
from qcware.serialization.transforms.to_wire import (
    constraints_from_wire,
    polynomial_objective_from_wire,
    to_wire,
)
from qcware.types.optimization.predicate import Predicate
from qcware.types.optimization.problem_spec import Constraints, PolynomialObjective


def pubo_example_1(constrained: bool):
    out = {}
    p = {
        (0,): -3,
        (0, 1): 2,
        (0, 2): 2,
        (0, 3): 2,
        (1,): -3,
        (1, 2): 2,
        (1, 3): 2,
        (2,): -3,
        (2, 3): 2,
        (3,): -2,
        (0, 1, 3): -2,
        (): 7,
    }
    p = PolynomialObjective(
        polynomial=p,
        num_variables=4,
    )
    if not constrained:
        expected_minima = {"0110", "1010", "1100", "1101"}
        expected_value = 3
    else:
        nonpositive_constraint_1 = PolynomialObjective(
            {(): -1, (0,): 1, (1,): 1, (2,): 1, (3,): 1}, num_variables=4
        )
        constraints = {Predicate.NONPOSITIVE: [nonpositive_constraint_1]}
        constraints = Constraints(constraints=constraints, num_variables=4)
        out.update({"constraints": constraints})
        expected_minima = {"1000", "0100", "0010"}
        expected_value = 4

    out.update(
        {
            "pubo": p,
            "expected_value": expected_value,
            "expected_minima": expected_minima,
            "solution_exists": True,
        }
    )
    return out


def pubo_example_2(constrained: bool):
    out = {}
    p = {
        (): 123,
        (0,): -368,
        (1,): 138,
        (2,): 376,
        (0, 1): -305,
        (0, 2): 99,
        (1, 2): -397,
    }
    p = PolynomialObjective(polynomial=p, num_variables=3)

    if not constrained:
        expected_minima = {"110"}
        expected_value = -412
    else:
        constraints = {
            Predicate.NEGATIVE: [
                # a + b + c < 3 (violated iff a=b=c=1)
                PolynomialObjective(
                    {(): -3, (0,): 1, (1,): 1, (2,): 1}, num_variables=3
                ),
                # Always true
                PolynomialObjective({(): -1}, num_variables=3),
            ],
            Predicate.ZERO: [
                # (a+b+c-1)^2 == 0 (true iff exactly one variable is 1.)
                PolynomialObjective(
                    {
                        (0, 1): 2,
                        (0, 2): 2,
                        (1, 2): 2,
                        (0,): -1,
                        (1,): -1,
                        (2,): -1,
                        (): 1,
                    },
                    num_variables=3,
                ),
                # a + c = 1 (true iff a XOR c)
                PolynomialObjective({(0,): 1, (2,): 1, (): -1}, num_variables=3),
            ],
        }
        constraints = Constraints(constraints, num_variables=3)

        out.update({"constraints": constraints})
        expected_minima = {"100"}
        expected_value = -245

    out.update(
        {
            "pubo": p,
            "expected_value": expected_value,
            "expected_minima": expected_minima,
            "solution_exists": True,
        }
    )
    return out


def pubo_example_3():
    """
    p(x) = 3 x_0 x_1 _x2 x3
    """
    out = {}
    p = PolynomialObjective(
        polynomial={
            (
                0,
                1,
                2,
                3,
            ): 3
        },
        num_variables=4,
    )
    out.update(
        {
            "pubo": p,
            "expected_value": 0,
            "expected_minima": {
                "0000",
                "0001",
                "0010",
                "0011",
                "0100",
                "0101",
                "0110",
                "0111",
                "1000",
                "1001",
                "1010",
                "1011",
                "1100",
                "1101",
                "1110",
            },
            "solution_exists": True,
        }
    )
    return out


def impossible_example():
    out = {}
    p = {(0,): -3, (0, 1): 2, (0, 2): 2, (): -3}
    p = PolynomialObjective(
        polynomial=p,
        num_variables=3,
    )

    constraints = {
        Predicate.NONZERO: [PolynomialObjective({(0, 1): -3}, num_variables=3)],
        Predicate.ZERO: [PolynomialObjective({(1,): 1}, num_variables=3)],
    }
    constraints = Constraints(constraints=constraints, num_variables=3)
    out.update(
        {
            "pubo": p,
            "expected_value": None,
            "expected_minima": set(),
            "solution_exists": False,
            "constraints": constraints,
        }
    )
    return out


unconstrained_examples = (
    pubo_example_1(False),
    pubo_example_2(False),
    pubo_example_3(),
)

constrained_examples = (
    pubo_example_1(True),
    pubo_example_2(True),
    impossible_example(),
)


def test_serialize_objective():
    p = pubo_example_1(False)["pubo"]
    p2 = polynomial_objective_from_wire(to_wire(p))
    assert p.dict() == p2.dict()


def test_serialize_constraints():
    c = pubo_example_1(True)["constraints"]
    c2 = constraints_from_wire(to_wire(c))
    assert to_wire(c) == to_wire(c2)


@pytest.mark.parametrize(
    "example,backend",
    itertools.product(unconstrained_examples, ("qcware/cpu", "qcware/gpu")),
)
def test_brute_force_minimize_unconstrained(example, backend):
    print("EXAMPLE: ", example)
    p = example["pubo"]
    expected_value = example["expected_value"]
    expected_minima = example["expected_minima"]
    expected_solution_exists = example["solution_exists"]

    out = brute_force_minimize(p, backend=backend)
    actual_minima = set(out.argmin)
    actual_value = out.value

    assert actual_value == expected_value
    assert actual_minima == expected_minima
    assert out.solution_exists == expected_solution_exists


@pytest.mark.parametrize(
    "example,backend",
    itertools.product(constrained_examples, ("qcware/cpu", "qcware/gpu")),
)
def test_brute_force_minimize_constrained(example, backend):
    p = example["pubo"]
    expected_value = example["expected_value"]
    expected_minima = example["expected_minima"]
    constraints = example["constraints"]
    expected_solution_exists = example["solution_exists"]

    out = brute_force_minimize(p, constraints)
    actual_minima = set(out.argmin)
    actual_value = out.value

    assert actual_value == expected_value
    assert actual_minima == expected_minima
    assert out.solution_exists == expected_solution_exists
