from quasar.backend import Backend
from quasar import Circuit
import numpy as np
from . import (has_run_statevector, has_statevector_input, run_measurement,
               run_statevector)


class QuasarBackend(Backend):
    """
    A backend for Quasar which runs on the Forge SaaS service.
    Forge must be configured with an api key prior to using this.
    """
    def __init__(self, forge_backend: str, backend_args={}):
        """
        Creates the QuasarBackend.  You must provide a Forge backend, and
        provide Forge backend arguments if necessary.

        :param forge_backend: A backend string such as `classical/simulator`
        :type forge_backend: str

        :param backend_args: A dict of arguments for the Forge backend.  Typically not necessary; defaults to `{}`
        :type backend_args: dict
        """
        self.forge_backend = forge_backend
        self.backend_args = backend_args

    @property
    def has_run_statevector(self):
        """
        Whether or not the Forge backend can run a circuit and provide a statevector output

        :return: whether statevector output is possible
        :rtype: bool
        """
        return has_run_statevector(backend=self.forge_backend)

    @property
    def has_statevector_input(self):
        """
        Whether or not the Forge backend can accept a starting statevector for a circuit
        
        :return: whethert statevector input is possible
        :rtype: bool
        """
        return has_statevector_input(backend=self.forge_backend)

    def run_statevector(self,
                        circuit: Circuit,
                        statevector: np.ndarray = None,
                        min_qubit: int = None,
                        nqubit: int = None,
                        dtype: type = np.complex128,
                        **kwargs):
        """
        Executes the given circuit on a Forge backend.  Returns a statevector
        representing the state of the quantum machine after the circuit execution is
        complete.

        :param circuit: A quasar circuit
        :type circuit: quasar.Circuit

        :param statevector: Input statevector if `has_statevector_input` is true
        :type statevector: numpy.ndarray

        :param min_qubit: The minimum qubit of the circuit to use for execution.  Typically leave this at None
        :type min_qubit: int

        :param nqubit: The number of qubits to run in the circuit.  Typically leave this at None
        :type nqubit: int

        :param dtype: Type of number to use for the statevector.  Typically leave at `np.complex128`
        :type: numpy dtype

        :returns: Statevector representing the state of the quantum system after circuit execution
        :rtype: numpy.ndarray
        """
        if self.has_run_statevector:
            return run_statevector(backend=self.forge_backend,
                                   backend_args=self.backend_args,
                                   circuit=circuit,
                                   statevector=statevector,
                                   min_qubit=min_qubit,
                                   dtype=dtype)
        else:
            raise NotImplementedError

    def run_measurement(self,
                        circuit: Circuit,
                        nmeasurement: int = None,
                        statevector: np.ndarray = None,
                        min_qubit: int = None,
                        nqubit: int = None,
                        dtype: type = np.complex128):
        """
        Run a circuit with a measurement-based result.

        :param circuit: Circuit to execute
        :type circuit: quasar.Circuit

        :param nmeasurement: Number of measurements to take
        :type nmeasurement: int

        :param statevector: Starting state of the quantum machine if supported by `has_statevector_input`
        :type statevector: numpy.ndarray

        :param min_qubit: The minimum qubit of the circuit to use for execution.  Typicall leave this at None
        :type min_qubit: integer

        :param nqubit: The number of qubits to run in the circuit.  Typically leave this at None
        :type nqubit: int

        :param dtype: Type of number to use for the statevector.  Typically leave at `np.complex128`
        :type: numpy dtype

        :returns: a quasar `ProbabilityHistogram` object containing a histogram of measurements, the number of measurements, and other data
        :type: quasar.ProbabilityHistogram
        """
        return run_measurement(backend=self.forge_backend,
                               backend_args=self.backend_args,
                               circuit=circuit,
                               nmeasurement=nmeasurement,
                               statevector=statevector,
                               min_qubit=min_qubit,
                               nqubit=nqubit,
                               dtype=dtype)
