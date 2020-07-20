# helper routines to serialize to/from quasar circuits
import re
from quasar.circuit import Circuit, CompositeGate, ControlledGate, Gate
from quasar.pauli import PauliString, Pauli
from quasar.measurement import ProbabilityHistogram
from .transforms.helpers import ndarray_to_dict, dict_to_ndarray, scalar_to_dict, dict_to_scalar
import numpy as np
from typing import Sequence, List, Tuple, Dict, Mapping
import json
import lz4
import base64
from sortedcontainers import SortedSet, SortedDict


def q_instruction_to_s(k, v):
    """
    Trivial serialization: taking a gate from a quasar
    circuit, gets the name, a dict of the parameters for
    instantiating the gate, and the list of bits
    to apply the gate
    (gatename, parameters, bits); returns a dict
    of the form { "gate": str, 
                  "parameters": (dict(parmname: parmval)),
                  "bits": tuple(int),
                  "times": tuple(int) }
    """
    if isinstance(v, CompositeGate):
        return dict(gate="CompositeGate",
                    parameters=dict(name=v.name,
                                    circuit=list(quasar_to_sequence(
                                        v.circuit)),
                                    ascii_symbols=v.ascii_symbols),
                    bits=k[1],
                    times=k[0])
    elif isinstance(v, ControlledGate):
        return dict(gate="ControlledGate",
                    parameters=dict(gate=q_instruction_to_s([None, None],
                                                            v.gate),
                                    controls=v.controls),
                    bits=k[1],
                    times=k[0])
    # for the U1 and U2 unitary gates, Quasar doesn't store the parameter U,
    # so we must call the operator function to extract it
    elif v.name in ['U1', 'U2']:
        newparms = dict(U=ndarray_to_dict(v.operator_function(None)))
        return dict(gate=v.name, parameters=newparms, bits=k[1], times=k[0])
    elif base_gate_name(v.name) not in Canonical_gate_names:
        raise GateSerializationNotImplementedError(v.name)
    else:
        return dict(gate=v.name,
                    parameters=dict(v.parameters),
                    bits=k[1],
                    times=k[0])


def wrap_gate(fn):
    """
    Gets a gate creation function and passes arguments if they
    exist
    """
    return lambda parms: fn(**parms) if len(parms) > 0 else fn


def wrap_composite_gate(parms):
    cg_circuit = sequence_to_quasar(parms['circuit'])
    gate = CompositeGate(cg_circuit, parms['name'], parms['ascii_symbols'])
    # make the bit list into a tuple since this is needed in hashland
    # see quasar add_gate method
    return gate


def wrap_controlled_gate(parms):
    gate = make_gate(parms['gate']['gate'], parms['gate']['parameters'])
    result = ControlledGate(gate, parms['controls'])
    return result


# this is just copied/pasted from 'dir (Gate)' in Python and taking
# the list of gate names from that.  It will need to be updated if

adjoint_re = re.compile(r"\^\+")
gate_re = re.compile(r"([\w]*)(\^\+)*")
adjoint_str = "^+"


def base_gate_name(gate_name: str) -> str:
    "Return the base gate name (without adjoint markers)"
    # return gate_re.search(gate_name).group(1)
    adjoint_index = gate_name.find(adjoint_str)
    return gate_name if adjoint_index == -1 else gate_name[0:adjoint_index]


def num_adjoints(gate_name: str) -> str:
    "the number of adjoint markers in this gate name"
    # return len(adjoint_re.findall(gate_name))
    return gate_name.count(adjoint_str)


# more gates are added to the base Gate class and there's not a way
# to programatically get it (eg from a SimpleNamespace)
Canonical_gate_names = [
    'CCX', 'CF', 'CS', 'CST', 'CSWAP', 'CX', 'CY', 'CZ', 'H', 'I', 'R_ion',
    'Rx', 'Rx2', 'Rx2T', 'Rx_ion', 'Ry', 'Ry_ion', 'Rz', 'Rz_ion', 'S', 'SO4',
    'SO42', 'ST', 'SWAP', 'T', 'TT', 'U1', 'U2', 'X', 'XX_ion', 'Y', 'Z', 'u1',
    'u2', 'u3'
]

Name_to_gatefn = {
    'CCX': wrap_gate(Gate.CCX),
    'CF': wrap_gate(Gate.CF),
    'CS': wrap_gate(Gate.CS),
    'CST': wrap_gate(Gate.CST),
    'CSWAP': wrap_gate(Gate.CSWAP),
    'CX': wrap_gate(Gate.CX),
    'CY': wrap_gate(Gate.CY),
    'CZ': wrap_gate(Gate.CZ),
    'H': wrap_gate(Gate.H),
    'I': wrap_gate(Gate.I),
    'R_ion': wrap_gate(Gate.R_ion),
    'Rx': wrap_gate(Gate.Rx),
    'Rx2': wrap_gate(Gate.Rx2),
    'Rx2T': wrap_gate(Gate.Rx2T),
    'Rx_ion': wrap_gate(Gate.Rx_ion),
    'Ry': wrap_gate(Gate.Ry),
    'Ry_ion': wrap_gate(Gate.Ry_ion),
    'Rz': wrap_gate(Gate.Rz),
    'Rz_ion': wrap_gate(Gate.Rz_ion),
    'S': wrap_gate(Gate.S),
    'SO4': wrap_gate(Gate.SO4),
    'SO42': wrap_gate(Gate.SO42),
    'ST': wrap_gate(Gate.ST),
    'SWAP': wrap_gate(Gate.SWAP),
    'T': wrap_gate(Gate.T),
    'U1': wrap_gate(Gate.U1),
    'U2': wrap_gate(Gate.U2),
    'X': wrap_gate(Gate.X),
    'XX_ion': wrap_gate(Gate.XX_ion),
    'Y': wrap_gate(Gate.Y),
    'Z': wrap_gate(Gate.Z),
    "CompositeGate": wrap_composite_gate,
    "ControlledGate": wrap_controlled_gate,
    'u1': wrap_gate(Gate.u1),
    'u2': wrap_gate(Gate.u2),
    'u3': wrap_gate(Gate.u3)
}


class GateSerializationNotImplementedError(NotImplementedError):
    pass


def quasar_to_dict(q: Circuit) -> Dict:
    """
    Returns a serializable dict object suitable for conversion to JSON
    or other simple format, with format
      { "instructions": sequence of dicts in form q_instruction_to_s,
        "qubits": sequence of ints from circuit.qubits,
        "times": sequence of ints from circuit.times }
    This is for the intent of faster serialization by constructing the 
    base objects of Circuit (SortedDict, SortedSet) more directly, 
    providing them sorted sequences which should be quickly iterable
    by timsort on construction
    """
    return dict(instructions=quasar_to_list(q),
                qubits=list(q.qubits),
                times=list(q.times),
                times_and_qubits=list(q.times_and_qubits))


def dict_to_quasar(d: Mapping) -> Circuit:
    """
    Takes a serialized mapping dict as in quasar_to_dict and returns
    a rebuilt circuit from the elements therein
    """
    gate_generator = (((tuple(instruction['times']),
                        tuple(instruction['bits'])),
                       make_gate(instruction['gate'],
                                 instruction['parameters']))
                      for instruction in d['instructions'])
    gates = SortedDict(gate_generator)
    qubits = SortedSet(d['qubits'])
    times = SortedSet(d['times'])
    times_and_qubits = SortedSet([tuple(x) for x in d['times_and_qubits']])
    result = Circuit.__new__(Circuit)
    result.gates = gates
    result.qubits = qubits
    result.times = times
    result.times_and_qubits = times_and_qubits
    return result


def quasar_to_sequence(q: Circuit) -> Sequence:
    return (q_instruction_to_s(k, v) for k, v in q.gates.items())


def quasar_to_list(q: Circuit) -> List:
    return list(quasar_to_sequence(q))


def quasar_to_string(q: Circuit) -> str:
    b = json.dumps(quasar_to_dict(q)).encode('utf-8')
    cb = lz4.frame.compress(b)
    return base64.b64encode(cb).decode('utf-8')


def make_gate(gate_name: str, original_parameters: dict):
    # U1 and U2 have translated ndarrays, so we must convert them
    parameters = original_parameters.copy()
    if gate_name in ['U1', 'U2']:
        parameters['U'] = dict_to_ndarray(parameters['U'])
    base = base_gate_name(gate_name)
    n_adj = num_adjoints(gate_name)
    f = Name_to_gatefn.get(base, None)
    if f is None:
        raise GateSerializationNotImplementedError(gate_name)
    else:
        gate = f(parameters)
        for i in range(n_adj):
            gate = gate.adjoint()
    return gate


def sequence_to_quasar(s: Sequence) -> Circuit:
    # make a sequence of tuples (gate, qubits, times) and manually
    # add to circuit, no need for copy
    instructions = [(make_gate(instruction['gate'], instruction['parameters']),
                     tuple(instruction['bits']), tuple(instruction['times']))
                    for instruction in s]
    gate_dict = SortedDict({(x[2], x[1]): x[0] for x in instructions}.items())
    qubit_set = SortedSet
    result = Circuit()
    for instruction in s:
        gate = make_gate(instruction['gate'], instruction['parameters'])
        # add_gate is quite fussy about taking tuples
        result.add_gate(gate,
                        tuple(instruction['bits']),
                        times=tuple(instruction['times']))
    return result


def string_to_quasar(s: str) -> Circuit:
    cb = base64.b64decode(s)
    b = lz4.frame.decompress(cb)
    qdict = json.loads(b.decode('utf-8'))
    return dict_to_quasar(qdict)


def probability_histogram_to_dict(hist: ProbabilityHistogram):
    return dict(nqubit=hist.nqubit,
                histogram=hist.histogram,
                nmeasurement=hist.nmeasurement)


def dict_to_probability_histogram(d: dict):
    d2 = d.copy()
    if 'histogram' in d2:
        d2['histogram'] = {int(k): v for k, v in d2['histogram'].items()}
    return ProbabilityHistogram(d2['nqubit'], d2['histogram'],
                                d2['nmeasurement'])


def pauli_item_to_tuple(k: PauliString, v: object) -> Tuple[str, Dict]:
    return tuple((str(k), scalar_to_dict(v)))


def tuple_to_pauli_item(t: Tuple[str, Dict]) -> Tuple:
    return tuple((PauliString.from_string(t[0]), dict_to_scalar(t[1])))


def pauli_to_list(p: Pauli) -> List[Tuple[str, Dict]]:
    """
    Transforms a pauli object into a list of tuples
    of the form str, float float, representing 
    (PauliString, Dict) where the Dict is an encoded
    numpy array
    """
    return [pauli_item_to_tuple(k, v) for k, v in p.items()]


def list_to_pauli(pl: List) -> Pauli:
    """
    Transforms a list of pauli tuples (see above) to
    a pauli object
    """
    return Pauli([tuple_to_pauli_item(t) for t in pl])
