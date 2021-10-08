

.. image:: http://qcwareco.wpengine.com/wp-content/uploads/2019/08/qc-ware-logo-11.png
   :target: http://qcwareco.wpengine.com/wp-content/uploads/2019/08/qc-ware-logo-11.png
   :alt: logo


========================================
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
============

To install with pip:

.. code:: shell

   pip install qcware

To install from source, first, you must install `poetry <https://python-poetry.org/docs/>`_.
Then, execute the following:

.. code:: shell

   git clone https://github.com/qcware/platform_client_library_python.git
   cd platform_client_library_python
   poetry build
   cd dist
   pip install qcware-6.0.0-py3-none-any.whl

Finally, to access Forge, sign up for an API key at `https://forge.qcware.com <https://forge.qcware.com>`_.
