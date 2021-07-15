Binary Optimization
===================

As we evolve our binary optimization API, we will be breaking up the all-in-one
`solve_binary` function into more algorithm-specific functions.  As an interim step,
we introduce a very similar `optimize_binary` function which takes a better-defined
`BinaryProblem` class as an input and returns a more full-featured `BinaryResults`
class as output.

Types
-----

.. autoclass:: qcware.types.optimization.BinaryProblem
   :members:

.. autoclass:: qcware.types.optimization.BinaryResults
   :members:

Functions
---------

.. autofunction:: qcware.optimization.optimize_binary

.. warning:: The old `solve_binary` function has been deprecated and will be removed in a future release
.. autofunction:: qcware.optimization.solve_binary


Optimal QAOA Angles
========================
.. autofunction:: qcware.optimization.find_optimal_qaoa_angles
