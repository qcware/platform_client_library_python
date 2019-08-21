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
        solver="dwave_hw",
        host="https://forge.qcware.com"):
    r"""Classifies test data according to input training data and a selected backend and classifier type

    It is strongly recommended to wrap a call to :obj:`fit_and_predict` in a try/catch block since it is possible for the
    platform or the client library to raise an exception.

    Args:
        key (:obj:`str`): An API key for the platform.  Keys can be allocated and managed from the Forge web portal
            website.

        X (:obj:`[[float]]`): Input training vector, with the number of samples and the number of features as the
            dimensions.

        y (:obj:`[int]`): Target values.

        T (:obj:`[[float]]`): Test data vectors.

        backend (:obj:`string`): Selects the specific backend used to run the computation.

            * "simulator": Runs the algorithms on a software simulator
            * "hardware": Runs on physical hardware

            Defaults to "simulator".

        clf_type (:obj:`string`): Selects the classifier used to run the computation. Options include
            "nearest_centroids", "nearest_clusters", and "nearest_neighbors".

            Defaults to "nearest_centroids".

        clf_params (:obj:`dict`): You can put parameters specific to each classifier here.

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
