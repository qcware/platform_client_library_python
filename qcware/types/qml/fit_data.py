"""Fit data, data structures only.

This is intended to ease the separation of fit_and_predict into
the obvious layers of fitting and prediction, but to do that we
need to be prepared to serialize the sklearn fitting and prediction
classes which are the basis of the quantum algorithms, as well
as additional internal data.
"""

from typing import Optional, Union

import numpy.typing
import quasar
from pydantic import BaseModel
from qcware.types.ndarray import NDArray


def model_dict(m, keys):
    return {k: getattr(m, k) for k in keys}


class FitDataBase(BaseModel):
    loader_mode: str
    num_measurements: int
    absolute: bool
    opt_shape: Optional[tuple[int, int]]


class QNearestCentroidFitData(FitDataBase):
    """Fit data for QNearestCentroid.

    Note that it is not intended that users create this
    data structure themselves!  It is used for serialization.

    As such, fit data is independent of loader circuit and backend.
    """

    # The test_distances member doesn't exist for the fitting
    # step so is omitted here
    # test_distances: list
    # following from NearestCentroid
    centroids: NDArray
    classes: NDArray
    n_features_in: int
    metric: str
    shrink_threshold: None


# note: the peculiar extra regressor_ and classifier_
# prefixes seem to be necessary to distinguish the two classes
# for pydantic
class QNeighborsRegressorFitData(FitDataBase):
    """Fit data for QNeighborsRegressor.

    Note that it is not intended that users create this
    data structure themselves!  It is used for serialization.

    As such, fit data is independent of loader circuit and backend.
    """

    # set after fit
    regressor_data: NDArray
    regressor_labels: NDArray
    # from kneighborsregressor
    n_neighbors: int


class QNeighborsClassifierFitData(FitDataBase):
    # set after fit
    classifier_data: NDArray
    classifier_labels: NDArray
    # from kneighborsregressor
    n_neighbors: int


class QMeansFitData(FitDataBase):
    data: NDArray
    labels: NDArray
    cluster_centers: NDArray
    history: NDArray
    n_iter: int
    inertia: float
    analysis: bool
    # from KMeans
    n_clusters: int
    init: str
    n_init: int
    max_iter: int
    tol: float


class FitData(BaseModel):

    model_name: str
    fit_data: Union[
        QNearestCentroidFitData,
        QNeighborsRegressorFitData,
        QNeighborsClassifierFitData,
        QMeansFitData,
    ]
