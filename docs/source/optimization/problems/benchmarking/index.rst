Benchmarking Problems
=====================


Note that the ``problems`` or ``benchmarking`` modules will not be imported with ``from qcware.optimization import *``. You must import ``qcware.optimization.problems`` explicitly.

For example, you can use the ``AlternatingSectorsChain`` class with any of the following.

.. code:: python

    import qcware.optimization
    qcware.optimization.problems.AlternatingSectorsChain(...)
    qcware.optimization.problems.benchmarking.AlternatingSectorsChain(...)


.. toctree::
   :maxdepth: 2
   :caption: Contents

   alternatingsectorschain
