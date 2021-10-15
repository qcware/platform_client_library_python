from quasar.backend import Backend
from types import MethodType, FunctionType
from qcware.forge.api_calls.api_call_decorator import ApiCall
from qcware.serialization.transforms import client_args_to_wire
import inspect


class QuasarBackendApiCall(ApiCall):

    # you must manually assign backend and method
    def data(self, *args, **kwargs):
        if hasattr(self, "signature"):
            new_bound_kwargs = self.signature.bind(*[[self] + [args]], **kwargs)
            new_bound_kwargs.apply_defaults()
            new_kwargs = new_bound_kwargs.arguments
            # one problem here is that "kwargs" isn't a real argument, so
            if "kwargs" in new_kwargs:
                del new_kwargs["kwargs"]
        else:
            new_kwargs = {}
        if "self" in new_kwargs:
            del new_kwargs["self"]
        all_kwargs = dict(backend=self.backend, method=self.method, kwargs=new_kwargs)
        return client_args_to_wire("circuits.run_backend_method", **all_kwargs)


class QuasarBackend(object):
    """
    A backend for Quasar which runs on the Forge SaaS service.
    Forge must be configured with an api key prior to using this.
    """

    def __init__(self, forge_backend: str, backend_args={}):
        """
        Creates the QuasarBackend.  You must provide a Forge backend, and
        provide Forge backend arguments if necessary.

        :param forge_backend: A backend string such as `qcware/cpu_simulator`
        :type forge_backend: str

        :param backend_args: A dict of arguments for the Forge backend.  Typically not necessary; defaults to `{}`
        :type backend_args: dict
        """
        self.forge_backend = forge_backend
        self.backend_args = backend_args

    def __getattr__(self, name):
        # we override this to return a BackendApiCall object instead of
        # an actual wrapper
        if (
            (name not in dir(Backend))
            or (name[0] == "_")
            or (
                name
                in (
                    "linear_commuting_group",
                    "run_pauli_expectation_value_gradient_pauli_contraction",
                    "run_pauli_expectation_value_hessian",
                )
            )
        ):
            raise NotImplementedError
        f = getattr(Backend, name)

        if isinstance(f, MethodType) or isinstance(f, FunctionType):
            result = type(
                name,
                (QuasarBackendApiCall,),
                dict(
                    {
                        "name": "circuits.run_backend_method",
                        "endpoint": "circuits/run_backend_method",
                        "backend": self.forge_backend,
                        "method": name,
                        "_decorated": True,
                        "__doc__": f.__doc__,
                        "__module__": f.__module__,
                        "__annotations__": f.__annotations__,
                        "signature": inspect.signature(f),
                        "__wrapper__": f,
                    }
                ),
            )()

        else:
            result = type(
                name,
                (QuasarBackendApiCall,),
                dict(
                    {
                        "name": "circuits.run_backend_method",
                        "endpoint": "circuits/run_backend_method",
                        "backend": self.forge_backend,
                        "method": name,
                    }
                ),
            )()
        return result
