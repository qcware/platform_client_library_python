

.. image:: http://qcwareco.wpengine.com/wp-content/uploads/2019/08/qc-ware-logo-11.png
   :alt: logo


========================================
Forge Client Library
========================================

This package contains functions for easily interfacing with Forge.


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

|

Installation
============

To install with pip:

.. code:: shell

   pip install qcware

To install from source, you must first install `poetry <https://python-poetry.org/docs/>`_.
Then, execute the following:

.. code:: shell

   git clone https://github.com/qcware/platform_client_library_python.git
   cd platform_client_library_python
   poetry build
   cd dist
   pip install qcware-7.0.0-py3-none-any.whl


API Key
=======

To use the client library, you will need an API key. You can sign up for one at `https://forge.qcware.com <https://forge.qcware.com>`__.

To access your API key, log in to `Forge <https://forge.qcware.com>`_ and navigate to the API page. Your API key should be plainly visible there.


A Tiny Program
==============

The following code snippet illustrates how you might run Forge client code locally. Please make sure that you have installed the client library and obtained an API key before running the Python code presented below.

.. code:: python

    # configuration
    from qcware.forge.config import set_api_key, set_host
    set_api_key('YOUR-API-KEY-HERE')
    set_host('https://api.forge.qcware.com')

    # specify the problem (for more details, see the "Getting Started" Jupyter notebook on Forge)
    from qcware.forge import optimization
    from qcware.types import PolynomialObjective, Constraints, BinaryProblem

    qubo = {
        (0, 0): 1,
        (0, 1): 1,
        (1, 1): 1,
        (1, 2): 1,
        (2, 2): -1
    }

    qubo_objective = PolynomialObjective(
        polynomial=qubo,
        num_variables=3,
        domain='boolean'
    )

    # run a CPU-powered brute force solution
    results = optimization.brute_force_minimize(
        objective=qubo_objective,
        backend='qcware/cpu'
    )
    print(results)

If the client code has been properly installed and configured, the above code should display a result similar to the following:

.. code:: shell

    Objective value: -1
    Solution: [0, 0, 1]

For further guidance on running client code to solve machine learning problems, optimization problems, and more, please read through the documentation made available at `https://qcware.readthedocs.io <https://qcware.readthedocs.io/>`_ as well as the Jupyter notebooks made available on `Forge <https://app.forge.qcware.com/>`__.
