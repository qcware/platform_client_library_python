Higher Order Binary Optimization (HOBO)
=======================================

Accessed with ``qcware.optimization.HOBO``. Note that it is important to use the ``HOBO.convert_solution`` function to convert solutions of the PUBO, QUBO, Hising or Ising formulations of the HOBO back to a solution to the HOBO formulation.

We also discuss the ``qcware.optimization.binary_var`` function here, which just creates a ``HOBO``.


.. autoclass:: qcware.optimization.HOBO
    :members:


.. autofunction:: qcware.optimization.binary_var
