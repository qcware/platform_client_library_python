from hypothesis.strategies import (
    lists,
    composite,
    integers,
    dictionaries,
    sampled_from,
    none,
    just,
    text,
    iterables,
)
import itertools
import string
import cProfile

from qcware.types.optimization import (
    BinaryProblem,
    Constraints,
    Domain,
    PolynomialObjective,
    Predicate,
)

from qcware.types.optimization.results.results_types import Sample, BinaryResults

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


@composite
def samples(draw, problem):
    if problem.domain == Domain.BOOLEAN:
        bitstring = draw(
            lists(
                sampled_from([0, 1]),
                min_size=problem.num_variables,
                max_size=problem.num_variables,
            )
        )
    elif problem.domain == Domain.SPIN:
        bitstring = draw(
            lists(
                sampled_from([-1, 1]),
                min_size=problem.num_variables,
                max_size=problem.num_variables,
            )
        )
    value = problem.objective.compute_value(
        {index: v for index, v in enumerate(bitstring)}
    )
    # could change this too
    occurrences = 1
    return Sample(bitstring=bitstring, value=value, occurrences=occurrences)


@composite
def sample_sequences(draw, problem, num_samples):
    return draw(iterables(samples(problem), min_size=num_samples, max_size=num_samples))


@composite
def binary_results(draw, problem, num_samples):
    these_samples = draw(sample_sequences(problem, num_samples))
    return BinaryResults.from_unsorted_samples(samples, original_problem)
