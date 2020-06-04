from quasar.backend import Backend
from quasar import Circuit
import numpy as np
from . import (run_backend_method)


class QuasarBackend(object):
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

    def __getattr__(self, name):
        def wrapper(*args, **kwargs):
            if ((name in dir(Backend)) and (name[0] != '_') and (name not in (
                    'linear_commuting_group',
                    'run_pauli_expectation_value_gradient_pauli_contraction',
                    'run_pauli_expectation_value_hessian'))):
                return run_backend_method(self.forge_backend, name, kwargs)
            else:
                raise NotImplementedError(name)

        return wrapper
