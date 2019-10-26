NP Problems
===========


Note that the ``problems`` or ``np`` modules will not be imported with ``from qcware.optimization import *``. You must import ``qcware.optimization.problems`` explicitly.

For example, you can use the ``SetCover`` class with any of the following.

.. code:: python

    import qcware.optimization
    qcware.optimization.problems.SetCover(...)
    qcware.optimization.problems.np.SetCover(...)
    qcware.optimization.problems.np.covering.SetCover(...)


.. toctree::
   :maxdepth: 2
   :caption: Contents

   setcover
   vertexcover
   jobsequencing
   graphpartitioning
   numberpartitioning
   bilp
