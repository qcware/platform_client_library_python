import numpy
from . import request
from qcware.wrappers import print_errors, print_api_mismatch


@print_api_mismatch
@print_errors
def fit_and_predict(
        key,
        X=[],
        y=[],
        T=[],
        backend="simulator",
        clf_type="nearest_centroids",
        clf_params={},
        solver="dwave_hybrid",
        host="https://platform.qcware.com"):
    r"""Classifies test data according to input training data and a selected backend and classifier type

    It is strongly recommended to wrap a call to :obj:`fit_and_predict` in a try/catch block since it is possible for the
    platform or the client library to raise an exception.

    Args:
        key (:obj:`str`): An API key for the platform.  Keys can be allocated and managed from the Forge web portal
            website.

        X (:obj:`[[float]]`): Training data array of dimension m by n, where m equals the number of samples 
            and n the number of features. Both m and n are assumed to be powers of two.

        y (:obj:`[int]`): Target values array of dimension 1 by m, where m is the number of rows in X 
            (i.e the number of samples in X). For clf_type = "nearest_clusters", it is assumed that each target value
            has at least two occurences in y.

        T (:obj:`[[float]]`): Test data array of dimension d by n, where d is any positive integer
            and n equals the number of columns in X  (i.e the number of features in X).

        backend (:obj:`string`): Selects the specific backend used to run the computation.

            * "simulator": Runs the algorithms on a software simulator
            * "hardware": Runs on physical hardware

            Defaults to "simulator".

        clf_type (:obj:`string`): Selects the classifier used to run the computation. Options include
            "nearest_centroids", "nearest_clusters", and "nearest_neighbors".

            Defaults to "nearest_centroids".

        clf_params (:obj:`dict`): You can put parameters specific to each classifier here.
            
            The structure of clf_params depends on clf_type and is the following:
                
                For clf_type = "nearest_centroids", clf_params is {"mode": s} is either the string "exact" or the string "sample".
                    If mode="sample", then the classifier samples a centroid with probability propotional to the closeness to the test point. 
                    If mode="exact", then multiple samples are taken in order to choose the nearest centroid with high probability. 
                
                For clf_type = "nearest_clusters", clf_params is the empty dictionary.

                For clf_type = "nearest_neighbors", clf_params is the dictionary {"k": n_neighbors} 
                    where n_neighbors is the (positive integer) number of nearest neighbours to be computed for each point.
    Returns:
        JSON object: A JSON object, possibly containing the fields:
            * 'labels' (:obj:`list`): A Python list representing the classification labels.

    """

    params = {
        "key": key,
        "X": X if not isinstance(X, numpy.ndarray) else X.tolist(),
        "y": y if not isinstance(y, numpy.ndarray) else y.tolist(),
        "T": T if not isinstance(T, numpy.ndarray) else T.tolist(),
        "backend": backend,
        "clf_type": clf_type,
        "clf_params": clf_params,
        "solver": solver
    }

    result = request.post_json(host + "/api/v2/fit_and_predict", params)

    return result
