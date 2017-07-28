import params_pb2
from google.protobuf import descriptor
import numpy as np

def convert(params):
    print(params)
    param_dict = params_pb2.params()
    valid_keys = [f.name for f in param_dict.DESCRIPTOR.fields]
    for k,v in params.items():
        print(k, v)
        if k in valid_keys:
            python_to_proto(param_dict, k, v)
    print(param_dict)
    return param_dict

def mat_to_dict(mat, symmetrize=False):
    the_dict = {}
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            the_dict[(i,j)] = mat[i][j]
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

def python_to_proto(param_dict, k, v):
    if k == "Q":
        getattr(param_dict, k).extend(dict_to_protodict(v))
    elif k == "constraints_linear_A":
        getattr(param_dict, k).extend(dict_to_protodict(mat_to_dict(v)))
    elif k == "constraints_equality_R" or k == "constraints_inequality_S":
        getattr(param_dict, k).extend(mat_array_to_protodict_array(v))
    elif k == "constraints_equality_c" or k == "constraints_inequality_d":
        getattr(param_dict, k).extend(vec_array_to_protovec_array(v))
    elif k == "constraints_linear_b":
        getattr(param_dict, k).extend(v)
    else:
        #Must be a 'primitive' of some type
        setattr(param_dict, k, v)

def dict_to_protodict(pydict):
    mapentries = []
    for k,v in pydict.items():
        print("k:",k,"v:",type(v))
        mapentry = params_pb2.params.MatrixMapEntry()
        mapentry.i = k[0]
        mapentry.j = k[1]
        if isinstance(v, (int, np.integer)):
            mapentry.int_val = v
        else:
            mapentry.float_val = v
        mapentries.append(mapentry)
    return mapentries

def mat_array_to_protodict_array(mat_array):
    pb_matrices = []
    for mat in mat_array:
        pbmat = params_pb2.params.Matrix()
        pbmat.el.extend(dict_to_protodict(mat_to_dict(mat)))
        pb_matrices.append(pbmat)
    return pb_matrices

def vec_array_to_protovec_array(vec_array):
    pb_vecs = []
    for vec in vec_array:
        pbvec = params_pb2.params.Vector()
        pbvec.el.extend(vec)
        pb_vecs.append(pbvec)
    return pb_vecs
