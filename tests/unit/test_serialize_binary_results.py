from qcware.types.optimization import BinaryProblem, BinaryResults
import qubovert as qv
import json
from qcware.types.optimization import PolynomialObjective
from qcware.serialization.transforms.helpers import (to_wire, binary_problem_from_wire)

def create_binary_problem():
    Q = {(0, 0): 1, (1, 1): 1, (0, 1): -2, (2, 2): -2, (3, 3): -4, (3, 2): -6}
    qubo = PolynomialObjective(
        polynomial=Q,
        num_variables=4,
        domain='boolean'
    )
    problem = BinaryProblem(Q_dict=qubo)
    return problem


def test_serialize_problem():
    problem = create_binary_problem()
    pdict = to_wire(problem)
    json_string = json.dumps(pdict)
    pdict2 = json.loads(json_string)
    problem2 = binary_problem_from_wire(pdict2)
    # now try converting down again
    pdict3 = to_wire(problem2)
    json_string2 = json.dumps(pdict3)

    assert json_string2 == json_string
