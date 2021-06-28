import itertools
import json
import string

import pytest
import qubovert as qv
from hypothesis import assume, given, note
from hypothesis.strategies import (
    composite,
    dictionaries,
    floats,
    integers,
    just,
    lists,
    none,
    sampled_from,
    text,
)
from qcware.serialization.transforms.helpers import (
    binary_problem_from_wire,
    constraints_from_wire,
    polynomial_objective_from_wire,
    to_wire,
)
from qcware.types.optimization import (
    BinaryProblem,
    BinaryResults,
    Constraints,
    Domain,
    PolynomialObjective,
    Predicate,
)


# the following are some strategies meant solely to create data to test serialization;
# they make no bones about being reasonable problems
def keys(min_var: int = 0, max_var: int = 4):
    return lists(
        integers(min_var, max_var), min_size=1, max_size=(max_var - min_var)
    ).map(tuple)


def qdicts(min_var: int = 0, max_var: int = 4, min_size: int = 1, max_size: int = 3):
    return dictionaries(keys(), integers(1, 5), min_size=1, max_size=3)


@composite
def polynomial_objectives(draw, num_vars):
    objective = draw(qdicts(max_var=num_vars - 1))
    variables = set(itertools.chain.from_iterable(objective.keys()))
    num_variables = num_vars
    domain = draw(sampled_from(Domain))
    varmap = draw(none() | just({k: str(k) for k in variables}))
    return PolynomialObjective(
        objective,
        num_variables=num_variables,
        domain=domain,
        variable_name_mapping=varmap,
    )


@composite
def constraints(draw, num_vars):
    domain = draw(sampled_from(Domain))
    constraint_dict = draw(
        dictionaries(
            sampled_from(Predicate),
            lists(polynomial_objectives(num_vars), min_size=1),
            min_size=1,
        )
    )
    # we force all constraints here to have the same number of variables
    for constraint, polys in constraint_dict.items():
        for p in polys:
            p.domain = domain
            p.num_variables = num_vars
    return Constraints(constraint_dict, num_vars)


@composite
def binary_problems(draw, num_vars):
    objective = draw(polynomial_objectives(num_vars))
    _constraints = draw(constraints(num_vars=objective.num_variables))
    name = draw(text(string.ascii_lowercase + string.ascii_uppercase))
    return BinaryProblem(objective=objective, constraints=_constraints, name=name)


def create_binary_problem():
    Q = {(0, 0): 1, (1, 1): 1, (0, 1): -2, (2, 2): -2, (3, 3): -4, (3, 2): -6}
    qubo = PolynomialObjective(polynomial=Q, num_variables=4, domain="boolean")
    problem = BinaryProblem(objective=qubo)
    return problem


def create_binary_problem_from_dict():
    Q = {(0, 0): 1, (1, 1): 1, (0, 1): -2, (2, 2): -2, (3, 3): -4, (3, 2): -6}
    problem = BinaryProblem.from_dict(Q)
    return problem


def reflexive_serialize(v, from_wire_func):
    """Pushes the given object through serialization to JSON and back.

    Requires the "from_wire_func" to be provided manually.
    """
    d = to_wire(v)
    note(v)
    note(d)
    json_str = json.dumps(d)
    d2 = json.loads(json_str)
    result = from_wire_func(d2)
    return result


def assert_polynomial_objectives_equal(pobj, pobj2):
    assert pobj.polynomial == pobj2.polynomial
    assert pobj.num_variables == pobj2.num_variables
    assert pobj.domain == pobj2.domain
    assert pobj.degree == pobj2.degree
    assert pobj.variable_name_mapping == pobj2.variable_name_mapping


@given(polynomial_objectives(5))
def test_serialize_polynomial_objectives(pobj):
    pobj2 = reflexive_serialize(pobj, polynomial_objective_from_wire)
    assert_polynomial_objectives_equal(pobj, pobj2)


def assert_constraints_equal(constraints, constraints2):
    assert constraints.num_variables == constraints2.num_variables
    assert constraints.predicates == constraints2.predicates
    assert constraints.degree_dict == constraints2.degree_dict
    assert constraints.degree_set == constraints2.degree_set
    for key in constraints.constraint_dict:
        assert key in constraints2
        assert len(constraints2[key]) == len(constraints[key])
        for p1, p2 in zip(constraints[key], constraints2[key]):
            assert p1.polynomial == p2.polynomial
            assert p1.num_variables == p2.num_variables
            assert p1.domain == p2.domain
            assert p1.degree == p2.degree
            assert p1.variable_name_mapping == p2.variable_name_mapping


@given(constraints(5))
def test_serialize_constraints(constraints):
    constraints2 = reflexive_serialize(constraints, constraints_from_wire)
    # comparing nested dicts can get dicey, so we cheat and compare the
    # generated JSON
    assert_constraints_equal(constraints, constraints2)


@given(binary_problems(5))
def test_serialize_binary_problems(problem):
    problem2 = reflexive_serialize(problem, binary_problem_from_wire)
    assert_polynomial_objectives_equal(problem.objective, problem2.objective)
    if problem.constraints is None:
        assert problem2.constraints is None
    else:
        assert_constraints_equal(problem.constraints, problem2.constraints)
    assert problem.name == problem2.name


@pytest.mark.parametrize(
    ["problem"], [[create_binary_problem()], [create_binary_problem_from_dict()]]
)
def test_serialize_problem(problem):
    problem = create_binary_problem()
    pdict = to_wire(problem)
    json_string = json.dumps(pdict)
    pdict2 = json.loads(json_string)
    problem2 = binary_problem_from_wire(pdict2)
    # now try converting down again
    pdict3 = to_wire(problem2)
    json_string2 = json.dumps(pdict3)

    assert json_string2 == json_string
