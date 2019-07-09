from . import params_pb2
from google.protobuf import descriptor
import numpy as np


def convert(params, endpoint_type):
    param_dict = params_pb2.params()
    if endpoint_type != "solve_binary":
        param_dict = params_pb2.params_vqe()
    if endpoint_type == "qml":
        param_dict = params_pb2.params_qml()
    valid_keys = [f.name for f in param_dict.DESCRIPTOR.fields]
    for k, v in params.items():
        if k in valid_keys:
            python_to_proto(param_dict, k, v)
    return param_dict


def isInt(a):
    return isinstance(a, (int, np.integer))


def python_to_proto(param_dict, k, v):
    if k == "Q":
        getattr(param_dict, k).CopyFrom(dict_to_protodict(v, isTensor=True))
    elif k == "constraints_linear_A":
        getattr(param_dict, k).CopyFrom(dict_to_protodict(mat_to_dict(v)))
    elif k == "constraints_linear_b":
        getattr(param_dict, k).CopyFrom(vec_to_protovec(v))
    elif k == "constraints_equality_R" or k == "constraints_inequality_S":
        getattr(param_dict, k).extend(mat_array_to_protodict_array(v))
    elif k == "constraints_equality_c" or k == "constraints_inequality_d":
        getattr(param_dict, k).CopyFrom(vec_to_protovec(v))
    elif k == "dwave_anneal_offsets":
        param_dict.dwave_anneal_offsets.extend(v)
    elif k == "dwave_flux_biases":
        param_dict.dwave_flux_biases.extend(v)
    elif k == "dwave_anneal_schedule":
        getattr(param_dict, k).CopyFrom(array_to_anneal_schedule(v))
    elif k == "dwave_initial_state":
        getattr(param_dict, k).CopyFrom(array_to_initial_state(v))
    elif k == "dwave_chains":
        for arr in v:
            pb_obj = params_pb2.params.DWaveChain()
            pb_obj.qubits.extend(arr)
            param_dict.dwave_chains.extend([pb_obj])
    elif k == "dwave_beta_range":
        getattr(param_dict, k).CopyFrom(array_to_beta_range(v))
    elif k == "dwave_precision_ancillas_tuples":
        for arr in v:
            tup = array_to_precision_ancillas_tuple(arr)
            param_dict.dwave_precision_ancillas_tuples.extend([tup])
    elif k == "google_arguments_optimizer":
        getattr(param_dict, k).CopyFrom(dict_to_google_arguments_optimizer(v))
    elif k == "molecule":
        getattr(param_dict, k).CopyFrom(array_to_molecule_vqe(v))
    elif k == "guess_amplitudes":
        getattr(param_dict, k).CopyFrom(array_to_amplitudes_vqe(v))
    elif k == "X":
        getattr(param_dict, k).CopyFrom(array_to_data(v))
    elif k == "y":
        getattr(param_dict, k).CopyFrom(array_to_target_vector(v))
    elif k == "T":
        getattr(param_dict, k).CopyFrom(array_to_data(v))
    elif k == "clf_params":
        # jank, but it'll do
        pb_obj = params_pb2.params_qml(clf_params=v)
        getattr(param_dict, k).MergeFrom(pb_obj.clf_params)
    elif k == "initial_solution":
        # jank, but it'll do
        pb_obj = params_pb2.params(initial_solution=v)
        getattr(param_dict, k).MergeFrom(pb_obj.initial_solution)
    else:
        # Must be a 'primitive' of some type
        setattr(param_dict, k, v)


def mat_to_dict(mat, symmetrize=False):
    the_dict = {}
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            the_dict[(i, j)] = mat[i][j]
    if symmetrize:
        new_dict = {}
        for it in the_dict.keys():
            val = the_dict[it]
            if (it[1], it[0]) in the_dict.keys() and it[1] != it[0] and it[1] > it[0]:
                val += the_dict[(it[1], it[0])]
                new_dict[it] = val
            elif it[1] == it[0]:
                new_dict[it] = the_dict[it]
        return new_dict
    else:
        return the_dict


def dict_to_protodict(pydict, isTensor=False):
    pb_obj = params_pb2.params.Tensor() if isTensor else params_pb2.params.Matrix()
    for k, v in pydict.items():
        entry = pb_obj.entries.add()
        if isTensor:
            entry.indices.extend(k)
        else:
            entry.i = k[0]
            entry.j = k[1]
        if isInt(v):
            entry.int_val = v
        else:
            entry.float_val = v
    return pb_obj


def array_to_anneal_schedule(arr):
    pb_obj = params_pb2.params.DWaveAnnealSchedule()
    for pair in arr:
        entry = pb_obj.entries.add()
        entry.time = pair[0]
        entry.current = pair[1]
    return pb_obj


def array_to_initial_state(arr):
    pb_obj = params_pb2.params.DWaveInitialState()
    for pair in arr:
        entry = pb_obj.entries.add()
        entry.qubit = pair[0]
        entry.state = pair[1]
    return pb_obj


def array_to_beta_range(arr):
    pb_obj = params_pb2.params.DWaveBetaRange()
    pb_obj.start = arr[0]
    pb_obj.end = arr[1]
    return pb_obj


def array_to_precision_ancillas_tuple(arr):
    pb_obj = params_pb2.params.DWavePrecisionAncillasTuple()
    pb_obj.first = arr[0]
    pb_obj.second = arr[1]
    return pb_obj


def array_to_molecule_vqe(arr):
    pb_obj = params_pb2.params_vqe.Molecule()
    for atom in arr:
        entry = pb_obj.entries.add()
        entry.atom = atom[0]
        for pos in atom[1]:
            coord = entry.coord.add()
            if isInt(pos):
                coord.x_int = pos
            else:
                coord.x_float = pos
    return pb_obj


def array_to_amplitudes_vqe(arr):
    pb_obj = params_pb2.params_vqe.Vector2()
    for amplitude in arr:
        entry = pb_obj.entries.add()
        if isInt(amplitude):
            entry.int_val = amplitude
        else:
            entry.float_val = amplitude
    return pb_obj


def array_to_target_vector(arr):
    pb_obj = params_pb2.params_qml.TargetVector()
    for val in arr:
        pb_obj.targets.append(val)
    return pb_obj


def array_to_data(arr):
    pb_obj = params_pb2.params_qml.Data()
    for sample in arr:
        row = pb_obj.rows.add()
        for val in sample:
            row.values.append(val)
    return pb_obj


def mat_array_to_protodict_array(mat_array):
    pb_matrices = []
    for mat in mat_array:
        pbmat = dict_to_protodict(mat_to_dict(mat))
        pb_matrices.append(pbmat)
    return pb_matrices


def vec_to_protovec(vec):
    pb_vec = params_pb2.params.Vector()
    for el in vec:
        entry = pb_vec.entries.add()
        if isInt(el):
            entry.int_val = el
        else:
            entry.float_val = el
    return pb_vec


def vec_array_to_protovec_array(vec_array):
    pb_vecs = []
    for vec in vec_array:
        pb_vec = vec_to_protovec(vec)
        pb_vecs.append(pb_vec)
    return pb_vecs


def dict_to_google_arguments_optimizer(pydict):
    pb_obj = params_pb2.params.CirqArgumentsOptimizer()
    if 'init_point' in pydict:
        pb_obj.init_point = pydict['init_point']
    if 'number_iter' in pydict:
        pb_obj.number_iter = pydict['number_iter']
    if 'kappa' in pydict:
        pb_obj.kappa = pydict['kappa']
    return pb_obj
