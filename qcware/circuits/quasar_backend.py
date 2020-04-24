from quasar.backend import Backend
from quasar import Circuit
import numpy as np
from . import (has_run_statevector, has_statevector_input, run_measurement,
               run_statevector)


class QuasarBackend(Backend):
    def __init__(self, forge_backend: str, backend_args={}):
        self.forge_backend = forge_backend
        self.backend_args = backend_args

    @property
    def has_run_statevector(self):
        return has_run_statevector(backend=self.forge_backend)

    @property
    def has_statevector_input(self):
        return has_statevector_input(backend=self.forge_backend)

    def run_statevector(self,
                        circuit: Circuit,
                        statevector: np.ndarray = None,
                        min_qubit: int = None,
                        dtype: type = np.complex128,
                        **kwargs):
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
        return run_measurement(backend=self.forge_backend,
                               backend_args=self.backend_args,
                               circuit=circuit,
                               nmeasurement=nmeasurement,
                               statevector=statevector,
                               min_qubit=min_qubit,
                               nqubit=nqubit,
                               dtype=dtype)
