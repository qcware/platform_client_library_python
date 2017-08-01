import params_pb2
from google.protobuf import descriptor
import numpy as np


def convert(params):
    param_dict = params_pb2.params()
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
        getattr(param_dict, k).extend(vec_array_to_protovec_array(v))
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
