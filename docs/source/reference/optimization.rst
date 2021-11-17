Optimization
============


Brute Force Minimization
------------------------

Types
^^^^^

The brute-force minimization functions in Forge rely on custom
types for problem specification, constraints, and results.

.. autoclass:: qcware.types.optimization.PolynomialObjective
   :members:

.. autoclass:: qcware.types.optimization.Constraints
   :members:

.. autoclass:: qcware.types.optimization.BruteOptimizeResult
   :members:

Functions
^^^^^^^^^

.. autofunction:: qcware.forge.optimization.brute_force_minimize


Binary Optimization
-------------------

Types
^^^^^

.. autoclass:: qcware.types.optimization.BinaryProblem
   :members:

.. autoclass:: qcware.types.optimization.BinaryResults
   :members:

Functions
^^^^^^^^^

.. autofunction:: qcware.forge.optimization.optimize_binary


Quantum Approximate Optimization Algorithm (QAOA)
-------------------------------------------------

.. autofunction:: qcware.forge.optimization.find_optimal_qaoa_angles
.. autofunction:: qcware.forge.optimization.qaoa_expectation_value
.. autofunction:: qcware.forge.optimization.qaoa_sample
