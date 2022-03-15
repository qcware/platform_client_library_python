from abc import ABC, abstractmethod
from typing import Optional, Tuple

from qcware.forge.qml import fit, predict


class Classifier(ABC):
    def fit(self, X, y=None):
        self.fit_data = fit(X, type(self).__name__, y, self.parameters, self.backend)

    def predict(self, X):
        result = predict(X, self.fit_data, self.backend)
        return result


class QNearestCentroid(Classifier):
    def __init__(
        self,
        loader_mode: str = "parallel",
        backend: str = "qcware/cpu_simulator",
        num_measurements: int = 100,
        absolute: bool = False,
        opt_shape: Optional[Tuple[int, int]] = None,
    ):
        self.parameters = dict(
            loader_mode=loader_mode,
            num_measurements=num_measurements,
            absolute=absolute,
            opt_shape=opt_shape,
        )
        # we keep backend separate as it is passed separately to the API call
        self.backend = backend


class QNeighborsRegressor(Classifier):
    def __init__(
        self,
        n_neighbors: int = 3,
        loader_mode: str = "parallel",
        backend: str = "qcware/cpu_simulator",
        num_measurements: int = 100,
        absolute: bool = False,
        opt_shape: Optional[Tuple[int, int]] = None,
    ):
        self.parameters = dict(
            n_neighbors=n_neighbors,
            loader_mode=loader_mode,
            num_measurements=num_measurements,
            absolute=absolute,
            opt_shape=opt_shape,
        )
        self.backend = backend


class QNeighborsClassifier(Classifier):
    def __init__(
        self,
        n_neighbors: int = 3,
        loader_mode: str = "parallel",
        backend: str = "qcware/cpu_simulator",
        num_measurements: int = 100,
        absolute: bool = False,
        opt_shape: Optional[Tuple[int, int]] = None,
    ):
        self.parameters = dict(
            n_neighbors=n_neighbors,
            loader_mode=loader_mode,
            num_measurements=num_measurements,
            absolute=absolute,
            opt_shape=opt_shape,
        )
        self.backend = backend


class QMeans(Classifier):
    def __init__(
        self,
        n_clusters: int = 3,
        init: str = "random",
        n_init: int = 1,
        max_iter: int = 10,
        tol: float = 1e-4,
        analysis: bool = False,
        loader_mode: str = "parallel",
        backend: str = "qcware/cpu_simulator",
        num_measurements: int = 100,
        absolute: bool = False,
        opt_shape: Optional[Tuple[int, int]] = None,
    ):
        self.parameters = dict(
            n_clusters=n_clusters,
            init=init,
            n_init=n_init,
            max_iter=max_iter,
            tol=tol,
            analysis=analysis,
            loader_mode=loader_mode,
            num_measurements=num_measurements,
            absolute=absolute,
            opt_shape=opt_shape,
        )
        self.backend = backend
