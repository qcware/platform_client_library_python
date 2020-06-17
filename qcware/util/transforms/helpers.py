import numpy as np
import base64
from typing import Dict
import lz4.frame


def ndarray_to_dict(x: np.ndarray):
    # from https://stackoverflow.com/questions/30698004/how-can-i-serialize-a-numpy-array-while-preserving-matrix-dimensions
    if x is None:
        return None
    else:
        if isinstance(x, list) or isinstance(x, tuple):
            x = np.array(x)
        b = x.tobytes()
        Compression_threshold = 1024
        if len(b) > Compression_threshold:
            b = lz4.frame.compress(b)
            compression = 'lz4'
        else:
            compression = 'none'
        return dict(ndarray=base64.b64encode(b).decode('utf-8'),
                    compression=compression,
                    dtype=x.dtype.str,
                    shape=x.shape)


def dict_to_ndarray(d: dict):
    if d is None:
        return None
    else:
        b = base64.b64decode(d['ndarray'])
        if d['compression'] == 'lz4':
            b = lz4.frame.decompress(b)
        return np.frombuffer(
            b,
            dtype=np.dtype(d['dtype']),
        ).reshape(d['shape'])


def scalar_to_dict(v) -> Dict:
    """
    Hack for individual numerical scalars to serializable form.
    This is done by casting them to complex128, which is byte-wasteful
    in some ways, and into an array, which is byte-wasteful in other
    ways, but at least preserves accuracy to a degree
    """
    return ndarray_to_dict(np.array([v], dtype=np.complex128))


def dict_to_scalar(d: Dict):
    return dict_to_ndarray(d)[0]


def remap_q_indices_from_strings(q_old: dict) -> dict:
    q_new = {eval(k): v for k, v in q_old.items()}
    return q_new


def remap_q_indices_to_strings(Q: dict) -> dict:
    return {str(k): v for k, v in Q.items()}


def complex_dtype_to_string(t: type):
    if t is None:
        return None
    else:
        result = t.__name__
        if result not in ['complex64', 'complex128']:
            raise NotImplementedError(
                'dtypes not of complex64 or complex128 not currently supported'
            )
        return result


def string_to_complex_dtype(s: str):
    if s is None:
        return None
    elif s == 'complex64':
        return np.complex64
    elif s == 'complex128':
        return np.complex128
    else:
        raise NotImplementedError(
            'dtypes not of complex64 or complex128 not currently supported')
