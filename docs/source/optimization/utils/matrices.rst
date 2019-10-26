Matrix Objects
==============

The matrix objects are for dealing with PUBOs, HIsings, QUBOs, and Isings that have integer labels. All the ``to_`` methods return matrix objects. For example, ``HOBO.to_qubo`` returns a ``QUBOMatrix`` object.

Note that the ``utils`` module will not be imported with ``from qcware.optimization import *``. You must import ``qcware.optimization.utils`` explicitly.

Accessed with ``qcware.optimization.utils.matrix_name``.


PUBOMatrix
----------

.. autoclass:: qcware.optimization.utils.PUBOMatrix
    :members:


HIsingMatrix
------------

.. autoclass:: qcware.optimization.utils.HIsingMatrix
    :members:


QUBOMatrix
----------

.. autoclass:: qcware.optimization.utils.QUBOMatrix
    :members:


IsingMatrix
-----------

.. autoclass:: qcware.optimization.utils.IsingMatrix
    :members:
