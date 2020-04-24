import pytest
from qcware.util.transforms import (client_args_to_wire, server_args_from_wire,
                                    server_result_to_wire,
                                    client_result_from_wire)
import numpy as np


# numpy test covers qio.loader
@pytest.mark.parametrize("method_name, client_args, server_args", [
    ('optimization.solve_binary', {
        'Q': {
            (0, 1): 1
        }
    }, {
        'Q': {
            '(0, 1)': 1
        }
    }),
])
def test_arg_transformations(method_name: str, client_args: dict,
                             server_args: dict):
    sargs = client_args_to_wire(method_name, **client_args)
    assert sargs == server_args
    cargs = server_args_from_wire(method_name, **sargs)
    assert cargs == client_args
