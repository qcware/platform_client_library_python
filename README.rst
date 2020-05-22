

.. image:: http://qcwareco.wpengine.com/wp-content/uploads/2019/08/qc-ware-logo-11.png
   :target: http://qcwareco.wpengine.com/wp-content/uploads/2019/08/qc-ware-logo-11.png
   :alt: logo


QC Ware Platform Client Library (Python)
========================================

This package contains functions for easily interfacing with the QC Ware
Platform from Python.


.. image:: https://badge.fury.io/py/qcware.svg
   :target: https://badge.fury.io/py/qcware
   :alt: PyPI version
 
.. image:: https://pepy.tech/badge/qcware
   :target: https://pepy.tech/project/qcware
   :alt: Downloads
 
.. image:: https://pepy.tech/badge/qcware/month
   :target: https://pepy.tech/project/qcware/month
   :alt: Downloads
 
.. image:: https://circleci.com/gh/qcware/platform_client_library_python.svg?style=svg
   :target: https://circleci.com/gh/qcware/platform_client_library_python
   :alt: CircleCI

.. image:: https://readthedocs.org/projects/qcware/badge/?version=latest
   :target: https://qcware.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status


Installation
____________

This documentation is for the latest (prerelease) version of QCWare's Forge client, which
at present relies on some internal packages.  It is "baked into" QCWare's Jupyterhub
notebooks, but local installation will have to wait until Quasar, our circuit-model
library, is publicly available.

Ordinarily, you would install as follows:

To install with pip:

.. code:: shell

   pip install qcware

Or, to install from source:

.. code:: shell

   git clone https://github.com/qcware/platform_client_library_python.git
   cd platform_client_library_python
   pip install -e .

Sign up for an API key at `https://forge.qcware.com <https://forge.qcware.com>`_ to access *Forge*. Please see our `documentation <https://qcware.readthedocs.io>`_.

Using QC Ware Forge
-------------------

From your Forge dashboard, you will have access to many notebooks with detailed tutorials and examples. Below we will show a few Hello World examples.

Optimization
^^^^^^^^^^^^

Consider the following optimization problem: 

.. image:: https://latex.codecogs.com/png.latex?x=\min{x%20\in%20\{0,%201\}^3}(x_0x_1+2x_0x_2-x_1x_2+x_0-3x_1)
   :alt: qubo_example

We can solve this with the ``qcware`` software package. First, create a QUBO representation (see the `notebooks <https://forge.qcware.com>`_ for details).

.. code:: python

   Q = {(0, 1): 1, (0, 2): 2, (1, 2): -1, (0, 0): 1, (1, 1): -3}

Next, choose a backend (formerly _solver_). For example, to solve the problem with D'Wave's quantum annealer, set the `backend` argument to ``'dwave'``.

.. code:: python

   backend = 'dwave'

Finally, configure the QCWare library and call the solver (note! configuration has changed; see below.  You no longer need to supply your api key with every call)

.. code:: python

   import qcware
   qcware.config.set_api_key('your_api_key_here')
   result = qcware.optimization.solve_binary(Q=Q, backend=backend)
   print(result)

Please see the `documentation <https://qcware.readthedocs.io>`_ and `notebooks <https://forge.qcware.com>`_ for more details.
