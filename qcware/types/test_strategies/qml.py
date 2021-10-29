from hypothesis import strategies as st
from hypothesis.extra import numpy as hnp
from qcware.types.qml import FitData, QNearestCentroidFitData
from quasar import Circuit

sample_backends = sorted(["qcware/cpu", "qcware/cpu_simulator", "qcware/gpu_simulator"])

sample_loader_modes = sorted(["parallel", "diagonal", "optimized"])

model_names = sorted(["QNearestCentroid"])


@st.composite
def q_nearest_centroid_fit_datas(draw):
    """Generates bogus data for testing serialization.
    Of particular note: the circuit is just a bell pair.
    """
    backend = draw(st.sampled_from(sample_backends))
    loader_mode = draw(st.sampled_from(sample_loader_modes))
    num_measurements = draw(st.integers())
    absolute = draw(st.booleans())
    opt_shape = draw(st.one_of(st.tuples(st.integers(), st.integers()), st.none()))
    _n_classes = draw(st.integers(min_value=1, max_value=5))
    _n_features = draw(st.integers(min_value=1, max_value=5))

    centroids = draw(
        hnp.arrays(
            "float64",
            (_n_classes, _n_features),
            elements={"allow_nan": False, "allow_infinity": False},
        )
    )
    classes = draw(
        hnp.arrays(
            "float64",
            (_n_classes,),
            elements={"allow_nan": False, "allow_infinity": False},
        )
    )
    n_features_in = _n_features
    feature_names_in = None
    metric = "euclidean"
    shrink_threshold = None
    return QNearestCentroidFitData(
        backend=backend,
        loader_mode=loader_mode,
        num_measurements=num_measurements,
        absolute=absolute,
        opt_shape=opt_shape,
        centroids=centroids,
        classes=classes,
        n_features_in=n_features_in,
        feature_names_in=feature_names_in,
        metric=metric,
        shrink_threshold=shrink_threshold,
    )


@st.composite
def fit_datas(draw):
    model_name = draw(st.sampled_from(model_names))
    if model_name == "QNearestCentroid":
        fit_data = draw(q_nearest_centroid_fit_datas())
    return FitData(model_name=model_name, fit_data=fit_data)
