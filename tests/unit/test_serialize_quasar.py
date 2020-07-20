import inspect
from random import uniform
from quasar import Circuit, CompositeGate, ControlledGate, Gate
from qcware.util.serialize_quasar import (quasar_to_sequence,
                                          sequence_to_quasar, base_gate_name,
                                          num_adjoints, make_gate,
                                          quasar_to_string,
                                          string_to_quasar,
                                          Canonical_gate_names)
from scipy.stats import unitary_group


def test_serialize_quasar_1_and_2():
    q = Circuit()
    q.H(0).CX(0, 1).CX(1, 2).ST(0)
    s = list(quasar_to_sequence(q))
    q2 = sequence_to_quasar(s)
    s2 = list(quasar_to_sequence(q2))

    assert s == s2
    assert Circuit.test_equivalence(q, q2)


def test_serialize_parmgates():
    q = Circuit()
    q.Rx(0, 0.5)
    s = list(quasar_to_sequence(q))
    q2 = sequence_to_quasar(s)
    s2 = list(quasar_to_sequence(q2))

    assert s == s2
    assert Circuit.test_equivalence(q, q2)


def test_serialize_compositegates():
    cg = CompositeGate(
        Circuit().CF(0, 1, theta=0.42).CX(1, 0),
        name='PS',
        ascii_symbols=['P', 'S'],
    )
    q = Circuit()
    q.add_gate(cg, (0, 1))
    s = list(quasar_to_sequence(q))
    q2 = sequence_to_quasar(s)
    s2 = list(quasar_to_sequence(q2))

    assert s == s2
    assert Circuit.test_equivalence(q, q2)


def test_serialize_controlledgate():
    cX = ControlledGate(Gate.X)
    q = Circuit()
    q.add_gate(cX, (0, 1))
    s = list(quasar_to_sequence(q))
    q2 = sequence_to_quasar(s)
    s2 = list(quasar_to_sequence(q2))

    assert s == s2
    assert Circuit.test_equivalence(q, q2)


def test_adjoint_regexes():
    s = 'S'
    st = 'S^+'
    stt = 'S^+^+'

    assert base_gate_name(s) == 'S'
    assert num_adjoints(s) == 0
    assert base_gate_name(st) == 'S'
    assert num_adjoints(st) == 1
    assert base_gate_name(stt) == 'S'
    assert num_adjoints(stt) == 2


def test_create_adjoint():
    st = make_gate('S^+', {})
    assert st == Gate.ST

    stt = make_gate("S^+^+", {})
    assert stt == Gate.S


def test_all_canonical_gates():
    # make a circuit with all the gates.  It may not make
    # sense--that's OK.  It's just to ensure the serialization
    # works
    q = Circuit()
    for gate_name in Canonical_gate_names:
        g = getattr(Gate, gate_name)
        # print(f"Gate {g} (callable: {callable(g)})")
        if callable(g):
            if gate_name == 'U1':
                g = Gate.U1(unitary_group.rvs(2))
            elif gate_name == 'U2':
                g = Gate.U2(unitary_group.rvs(4))
            else:
                # this is a function-style gate; instantiate it
                # with random parameters
                argnames = inspect.getfullargspec(g).args
                args = dict(
                    zip(argnames,
                        [uniform(0, 3.14) for x in range(len(argnames))]))
                # print(f"Instantiating {gate_name}")
                g = g(**args)
        try:
            bits = tuple(range(g.nqubit))
            q.add_gate(g, bits)
        except Exception as e:
            # print(f"With gate {gate_name} ({g})")
            raise e

    s = list(quasar_to_sequence(q))
    q2 = sequence_to_quasar(s)
    s2 = list(quasar_to_sequence(q2))
    assert Circuit.test_equivalence(q, q2)
    assert (s == s2)

    s2 = quasar_to_string(q)
    # print(s2)
    q3 = string_to_quasar(s2)
    assert Circuit.test_equivalence(q, q3)
