from functools import singledispatch

from qcware.serialization.transforms.helpers import (
    dict_to_ndarray,
    ndarray_to_dict,
    remap_q_indices_from_strings,
    remap_q_indices_to_strings,
)
from qcware.types.optimization import (
    BinaryProblem,
    BruteOptimizeResult,
    Constraints,
    PolynomialObjective,
)
from qcware.types.optimization.results.results_types import BinaryResults, Sample
from qcware.types.qml import (
    FitData,
    QMeansFitData,
    QNearestCentroidFitData,
    QNeighborsClassifierFitData,
    QNeighborsRegressorFitData,
)


@singledispatch
def to_wire(x):
    """For complex types, this dispatches to create a JSON-compatible dict"""
    raise NotImplementedError(f"Unsupported Type: {type(x)}")


@to_wire.register(PolynomialObjective)
def polynomial_objective_to_wire(x):
    result = x.dict()
    result["polynomial"] = remap_q_indices_to_strings(result["polynomial"])
    result["variable_name_mapping"] = {
        str(k): v for k, v in result["variable_name_mapping"].items()
    }
    return result


def polynomial_objective_from_wire(d: dict):
    remapped_dict = d.copy()

    remapped_dict["polynomial"] = remap_q_indices_from_strings(d["polynomial"])
    remapped_dict["variable_name_mapping"] = {
        int(k): v for k, v in remapped_dict["variable_name_mapping"].items()
    }
    return PolynomialObjective(**remapped_dict)


@to_wire.register(Constraints)
def constraints_to_wire(x):
    result = x.dict()
    result["constraints"] = {
        k: [to_wire(x) for x in v] for k, v in x.dict()["constraints"].items()
    }
    return result


def constraints_from_wire(d: dict):
    remapped_dict = d.copy()
    remapped_dict["constraints"] = {
        k: [polynomial_objective_from_wire(x) for x in v]
        for k, v in d["constraints"].items()
    }

    return Constraints(**remapped_dict)


@to_wire.register(BinaryProblem)
def binary_problem_to_wire(x):
    result = x.dict()
    result["objective"] = to_wire(result["objective"])
    result["constraints"] = (
        to_wire(result["constraints"]) if result["constraints"] is not None else None
    )
    return result


def binary_problem_from_wire(d: dict):
    remapped_dict = d.copy()
    remapped_dict["objective"] = polynomial_objective_from_wire(d["objective"])
    remapped_dict["constraints"] = (
        constraints_from_wire(remapped_dict["constraints"])
        if remapped_dict["constraints"] is not None
        else None
    )
    return BinaryProblem(**remapped_dict)


@to_wire.register(BinaryResults)
def _(x):
    result = x.dict()
    result["original_problem"] = to_wire(x.original_problem)
    result["task_metadata"] = {
        k: v
        for k, v in result["task_metadata"].items()
        if k not in ("Q", "Q_array", "split_to_full_map_array", "instance")
    }
    return result


def binary_results_from_wire(d: dict):
    remapped_dict = d.copy()
    remapped_dict["sample_ordered_dict"] = {
        k: Sample(**v) for k, v in remapped_dict["sample_ordered_dict"].items()
    }
    remapped_dict["original_problem"] = binary_problem_from_wire(d["original_problem"])
    return BinaryResults(**remapped_dict)


def brute_optimize_result_from_wire(d: dict):
    return BruteOptimizeResult(**d)


@to_wire.register(QNearestCentroidFitData)
def q_nearest_centroid_fit_data_to_wire(x):
    result = x.dict()
    result["centroids"] = ndarray_to_dict(result["centroids"])
    result["classes"] = ndarray_to_dict(result["classes"])
    return result


def q_nearest_centroid_fit_data_from_wire(d: dict):
    d["centroids"] = dict_to_ndarray(d["centroids"])
    d["classes"] = dict_to_ndarray(d["classes"])
    return QNearestCentroidFitData(**d)


@to_wire.register(QNeighborsRegressorFitData)
def q_neighbors_regressor_fit_data_to_wire(x):
    result = x.dict()
    result["regressor_data"] = ndarray_to_dict(result["regressor_data"])
    result["regressor_labels"] = ndarray_to_dict(result["regressor_labels"])
    return result


def q_neighbors_regressor_fit_data_from_wire(d: dict):
    d["regressor_data"] = dict_to_ndarray(d["regressor_data"])
    d["regressor_labels"] = dict_to_ndarray(d["regressor_labels"])
    return QNeighborsRegressorFitData(**d)


@to_wire.register(QNeighborsClassifierFitData)
def q_neighbors_classifier_fit_data_to_wire(x):
    result = x.dict()
    result["classifier_data"] = ndarray_to_dict(result["classifier_data"])
    result["classifier_labels"] = ndarray_to_dict(result["classifier_labels"])
    return result


def q_neighbors_classifier_fit_data_from_wire(d: dict):
    d["classifier_data"] = dict_to_ndarray(d["classifier_data"])
    d["classifier_labels"] = dict_to_ndarray(d["classifier_labels"])
    return QNeighborsClassifierFitData(**d)


@to_wire.register(QMeansFitData)
def q_means_fit_data_to_wire(x):
    result = x.dict()
    result["data"] = ndarray_to_dict(result["data"])
    result["labels"] = ndarray_to_dict(result["labels"])
    result["cluster_centers"] = ndarray_to_dict(result["cluster_centers"])
    result["history"] = ndarray_to_dict(result["history"])
    return result


def q_means_fit_data_from_wire(d: dict):
    d["data"] = dict_to_ndarray(d["data"])
    d["labels"] = dict_to_ndarray(d["labels"])
    d["cluster_centers"] = dict_to_ndarray(d["cluster_centers"])
    d["history"] = dict_to_ndarray(d["history"])

    return QMeansFitData(**d)


@to_wire.register(FitData)
def fit_data_to_wire(x):
    result = x.dict()
    result["fit_data"] = to_wire(x.fit_data)
    return result


def fit_data_from_wire(d: dict):
    if d["model_name"] == "QNearestCentroid":
        d["fit_data"] == q_nearest_centroid_fit_data_from_wire(d["fit_data"])
    elif d["model_name"] == "QNeighborsRegressor":
        d["fit_data"] = q_neighbors_regressor_fit_data_from_wire(d["fit_data"])
    elif d["model_name"] == "QNeighborsClassifier":
        d["fit_data"] = q_neighbors_classifier_fit_data_from_wire(d["fit_data"])
    elif d["model_name"] == "QMeans":
        d["fit_data"] = q_means_fit_data_from_wire(d["fit_data"])
    return FitData(**d)
