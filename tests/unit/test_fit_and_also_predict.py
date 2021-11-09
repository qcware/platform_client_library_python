import pprint

import numpy as np
import pytest
import qcware.forge
from qcware.forge.exceptions import ApiCallExecutionError
from qcware.forge.qml import (
    Classifier,
    QMeans,
    QNearestCentroid,
    QNeighborsClassifier,
    QNeighborsRegressor,
    fit,
    predict,
)


@pytest.mark.parametrize(
    "backend",
    [
        "qcware/cpu_simulator",
        "qcware/gpu_simulator",
        "ibm/simulator",
        "ibmq:ibmq_qasm_simulator",
        "awsbraket/sv1",
        # "awsbraket/tn1",
    ],
)
@pytest.mark.parametrize(
    "classifier_class, params",
    [
        (QNearestCentroid, dict(num_measurements=100)),
        (QNeighborsRegressor, dict(num_measurements=100, n_neighbors=2)),
        (QNeighborsClassifier, dict(num_measurements=100, n_neighbors=2)),
        (QMeans, dict(n_clusters=2, num_measurements=100)),
    ],
)
def test_fit_and_predict(backend: str, classifier_class, params):
    X = np.array([[-1, -2], [-1, -1], [2, 1], [1, 2]])
    y = np.array([0, 0, 1, 1])
    try:
        with qcware.forge.config.additional_config(client_timeout=5 * 60):
            fit_data = fit(
                X=X,
                y=y,
                model=classifier_class.__name__,
                backend=backend,
                parameters=params,
            )

            result = predict(X=X, fit_data=fit_data, backend=backend)
            # instantiate the classifier with default args for now
            classifier = classifier_class(**params)
            classifier.fit(X=X, y=y)
            print(classifier)
            result2 = classifier.predict(X)

    except ApiCallExecutionError as e:
        print(e)
        print(type(e.traceback))
        print(type(eval(e.traceback)))
        print("".join(eval(e.traceback)))
    # smoke test here in the client
    assert set(result).issubset({0, 1})
    assert len(result) == 4
    # extra faff below from the fact that q-means is unsupervised so it could
    # go either way on the labels
    assert (
        np.array_equal(result, [0, 0, 1, 1])
        if classifier_class.__name__ != "QMeans"
        else (
            np.array_equal(result, [0, 0, 1, 1]) or np.array_equal(result, [1, 1, 0, 0])
        )
    )

    assert set(result2).issubset({0, 1})
    assert len(result2) == 4
    assert (
        np.array_equal(result2, [0, 0, 1, 1])
        if classifier_class.__name__ != "QMeans"
        else (
            np.array_equal(result, [0, 0, 1, 1]) or np.array_equal(result, [1, 1, 0, 0])
        )
    )
