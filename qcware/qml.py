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
        solver="ibm_sw",
        host="https://api.forge.qcware.com"):
    """
    Classifies test data according to input training data and a selected
    backend and classifier type.

    Args:
        key (:obj:`str`) : An API key for the platform.
         Keys can be allocated and managed
         from the Forge web portal website.

        X (:obj:`[[float]]`):
         A numpy array holding the training points. d is the number dimensionality
         (number of features) of a training example.
         of size [n_train, d].

        y (:obj:`[int]`): A numpy array of class
         labels (strings or integers) of size [n_samples]
         corresponding to the training points.

        T (:obj:`[[float]]`): A numpy array of the test data [n_tests, d].

        backend (:obj:`string`): Selects
         the specific backend used to run the computation.

            The currently supported backend is:

            * "simulator": Runs the algorithms on a software simulator


        clf_type (:obj:`string`):
         Selects the quantum classifier. The options are
            "nearest_centroids", "nearest_clusters",
             and "nearest_neighbours". Defaults to "nearest_centroids".

        clf_params (:obj:`dict`): A dictionary of the parameters for
         each specific classifier (see description of
         each classifier below for details)

            The structure of `clf_params` depends on
             `clf_type` and is the following:

                1. For `clf_type` = "nearest_centroids", `
                clf_params` is {"mode": s}
                 where `s` is either the string
                 "exact" or the string "sample".

                    - If s = "sample", then the classifier
                     uses a fast quantum
                     inner product estimation procedure
                     to sample a centroid
                     with probability proportional to the
                     closeness to the test point.


                     - If s = "exact", the above procedure
                     is repeated a number of times
                     so multiple samples are taken
                     in order to choose the nearest
                     centroid with high probability.

                2. For `clf_type` = "nearest_clusters",
                 `clf_params` is the empty dictionary.

                3. For `clf_type` = "nearest_neighbours",
                 `clf_params` is the dictionary
                 {"k": n_neighbors} where `n_neighbors`
                 is the (positive integer)
                 number of nearest neighbours to
                 be computed for each point.
    Returns:
        JSON object: A JSON object, possibly containing the fields:
            * 'labels' (:obj:`list`): A Python
             list representing the classification labels.



    The function supports three different quantum classifiers.

    **Nearest Centroids Classifier**

    The classical Nearest Centroid classifier
     uses the training
     points belonging to each of $k$ classes
     in order to compute
     the centroid of each class.
     Then, the label of a test point is
     chosen by computing the distance of the
     point to all centroids
     and assigning the label of the nearest centroid.
     One can assign the label deterministically
     to the nearest centroid (exact assignment) or
     probabilistically proportional to the
     closeness (sample assignment).

    In this release, we perform the centroid
     calculation classically,
     meaning that we use scikit-learn’s nearest
     centroids fit() function
     to find the centroids. We also prepare the
     quantum circuits necessary for a fast loading of
     the centroids and the test points.
     Then, we assign a label to a test point by a
     quantum classifier that works in two modes.

    If mode=“sample”, then the classifier uses a fast quantum
     inner product estimation procedure
     to sample a centroid with probability proportional
     to the closeness to the test point.
     More precisely, the label $\\ell_j$ of
     centroid $C_j$ is assigned to a test point $T_i$ with probability


    $$\\Pr[\\mbox{ assign label }\\ell_j
     \\mbox{ to point } T_i \\;] \\; \\propto \\; 1 - d^2(C_j,T_i),$$


    where $d^2(\\cdot,\\cdot)$ is the square Euclidean distance
     between the two vectors normalized
     by their norms in order to take values in $[0,1]$.
     This corresponds to a “sample” assignment.

    If mode=“exact”, the above procedure is repeated a
     number of times so multiple samples are
     taken in order to choose the nearest
     centroid with high probability.

    The solution returned is a numpy array
     containing the label of the nearest centroid.

    **Nearest Clusters Classifier**

    This classifier takes advantage of the power
     of quantum superposition.
     Here we do not fit the model (by finding the
     centroids for example), we just do
     one pass over the training and test points in order to
     prepare the quantum loaders.
     When we want to assign a label to a test point we estimate
     the distance of the
     point to each cluster by estimating the average square
     Euclidean distance between the
     test point and the points of the cluster.
     We then assign the label that corresponds to the nearest cluster.

    The solution returned is a numpy array
     containing the label of the nearest cluster.

    **Nearest Neighbors Classifier**

    The classical nearest neighbors method with a
     user-defined parameter $k$ finds the $k$ training points
     that are closest in Euclidean distance to the test point.
     Then it assigns the label that, for example, corresponds
     to the majority or a weighted majority.

    The quantum nearest neighbor classifier with parameter
     $k$ uses quantum
     techniques to sample the $k$ nearest neighbors.
     More precisely, we estimate the distance
     between the test point $T_i$
     and each training point in superposition and sample a
     training point $X_j$ with probability

    $$\\Pr[\\mbox{ sampling }X_j \\mbox{ as a neighbor of }
     T_i \\;] \\; \\propto \\; 1 - d^2(X_j,T_i),$$

    where $d^2$ is the square Euclidean distance between
     the two vectors normalized by
     their norms in order to take values in $[0,1]$.
     We take enough samples to estimate the $k$ nearest neighbors.

    The solution returned is a numpy array
     containing the list of $k$ nearest neighbors.
     These neighbors can then be used to assign a label
     classically, for example through a
     majority or weighted majority vote.

    It is strongly recommended to wrap a call to
     :obj:`fit_and_predict`
     in a try/catch block since it is possible for the
    platform or the client library to raise an exception.
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
