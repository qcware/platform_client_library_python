import qcware
import numpy as np


def test_fit_and_predict():
    X = np.array([[-1, -2, 2, -1], [-1, -1, 2, 0], [2, 1, -2, -1],
                  [1, 2, 0, -1]])
    y = np.array([0, 0, 1, 1])
    result = qcware.qml.fit_and_predict(X=X, y=y, model="QNearestCentroid")
    assert (result == [0, 0, 1, 1]).all()
