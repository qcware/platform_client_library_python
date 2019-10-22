Utility Methods
================

Note that the ``utils`` module will not be imported with ``from qcware.optimization import *``. You must import ``qcware.optimization.utils`` explicitly.

Accessed with ``qcware.optimization.utils.function_name``.

Conversions
-----------

.. autofunction:: qcware.optimization.utils.pubo_to_hising

.. autofunction:: qcware.optimization.utils.hising_to_pubo

.. autofunction:: qcware.optimization.utils.qubo_to_ising

.. autofunction:: qcware.optimization.utils.ising_to_qubo

.. autofunction:: qcware.optimization.utils.matrix_to_qubo

.. autofunction:: qcware.optimization.utils.qubo_to_matrix

.. autofunction:: qcware.optimization.utils.binary_to_spin

.. autofunction:: qcware.optimization.utils.spin_to_binary

.. autofunction:: qcware.optimization.utils.decimal_to_binary

.. autofunction:: qcware.optimization.utils.decimal_to_spin

.. autofunction:: qcware.optimization.utils.binary_to_decimal

.. autofunction:: qcware.optimization.utils.spin_to_decimal


Values
------

.. autofunction:: qcware.optimization.utils.pubo_value

.. autofunction:: qcware.optimization.utils.hising_value

.. autofunction:: qcware.optimization.utils.qubo_value

.. autofunction:: qcware.optimization.utils.ising_value


Bruteforce Solvers
------------------

.. autofunction:: qcware.optimization.utils.solve_pubo_bruteforce

.. autofunction:: qcware.optimization.utils.solve_hising_bruteforce

.. autofunction:: qcware.optimization.utils.solve_qubo_bruteforce

.. autofunction:: qcware.optimization.utils.solve_ising_bruteforce


Hash
----

.. autofunction:: qcware.optimization.utils.hash_function


Useful functions
--------

.. autofunction:: qcware.optimization.utils.subgraph

.. autofunction:: qcware.optimization.utils.normalize
