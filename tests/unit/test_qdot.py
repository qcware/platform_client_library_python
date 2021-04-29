from qcware.qutils import qdot
from qcware.api_calls import status, retrieve_result
import numpy as np
import pytest
import itertools
import time
# the tricky thing here for serialization is to make
# sure that the types come out right.  For dot,
# we have
# scalar -> scalar -> scalar
# [m]->[m]->scalar
# m rows, n columns
# [mxn]->[n]->[m]
# [m]->[mxn]->[n]
# otherwise throw an exception

# I really wanted to use hypothesis here, but the fact is it
# takes too long to send it over the wire, so we'll do case studies
# for each
backends = (('qcware/cpu_simulator', None), ('awsbraket/sv1', 100),
            ('ibm/simulator', 100), ('qcware/gpu_simulator', None))


def flatten(x):
    return list(itertools.chain.from_iterable(x))


@pytest.mark.parametrize(
    'x, y, backend, num_measurements',
    (flatten(x) for x in itertools.product(((np.array([5]), np.array([5])),
                                            (np.array([[5, 4, 3], [2, 1, 0]]),
                                             np.array([8, 7, 6]))), backends)))
def test_qdot(x, y, backend, num_measurements):
    result = qdot(x, y, backend=backend, num_measurements=num_measurements)
    numpy_result = np.dot(x, y)
    if np.isscalar(numpy_result):
        assert np.isscalar(result)
    elif isinstance(numpy_result, np.ndarray):
        assert isinstance(result,
                          np.ndarray) and result.shape == numpy_result.shape
    # big tolerance here since this is more or less a smoke test for the client
    assert np.allclose(result, numpy_result, atol=7)


@pytest.mark.parametrize('backend', ['ibmq:ibmq_qasm_simulator'])
def test_qdot_ibmq(backend):
    """This is primarily a smoke test, and uses the submit_ forms
    because of the often long IBM queue times
    """
    x = np.array([5, 4])
    y = np.array([3, 1])
    job_id = qdot.submit(x, y, backend=backend, num_measurements=100)

    job_status = status(job_id)
    while job_status['status'] == 'open':
        time.sleep(0.5)
        job_status = status(job_id)

    result = retrieve_result(job_id)
    numpy_result = np.dot(x, y)

    assert np.allclose(result, numpy_result, atol=7)
