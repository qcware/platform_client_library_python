Quantum Circuit Programming
===========================

Forge has a number of facilities for "traditional" circuit-model quantum machine
programming using our Quasar library for building and executing quantum circuits.

The most current version of Quasar is present on our jupyter notebook server.
To use quasar to build a circuit, you can do something like the following::

  >>> from quasar import Circuit
  >>> bell_pair = Circuit()
  >>> bell_pair.H(0).CX(0,1)
  <quasar.circuit.Circuit object at 0x7febc7c93dd8>
  >>> print(bell_pair)
  T  : |0|1|
  q0 : -H-@-
          |
  q1 : ---X-
  T  : |0|1|


You can then run the circuit one of two ways: using the API or by using
the quasar forge backend.

Using the API
`````````````

Given a circuit, you can execute it on a given backend one of two ways:
by producing a statevector (supported on simulators which can exactly
calculate a statevector) or by a traditional measurement-based method
(which should work on any quantum processor or simulator).  Using our
circuit from above, we'll show execution on the `classical/simulator` backend::

  >>> has_run_statevector(backend='classical/simulator')
  True
  >>> run_statevector(circuit=bell_pair, backend='classical/simulator')
  array([0.70710678+0.j, 0.        +0.j, 0.        +0.j, 0.70710678+0.j])


Since any supported backend should support `run_measurement` we don't need to
check for that::

  >>> run_measurement(circuit=bell_pair, backend='classical/simulator', nmeasurement=1000)
  {'histogram': {'0': 0.511, '3': 0.489}, 'nmeasurement': 1000, 'nqubit': 2}

.. autofunction:: qcware.circuits.has_run_statevector
.. autofunction:: qcware.circuits.has_statevector_input
.. autofunction:: qcware.circuits.run_statevector
.. autofunction:: qcware.circuits.run_measurement


Using the quasar Forge backend:
```````````````````````````````

The `QuasarBackend` class provides a more integrated backend to Quasar using Forge
as a platform.  You can import the class from `qcware.circuits.quasar_backend`
and use it as shown below::

  >>> from qcware.circuits.quasar_backend import QuasarBackend
  >>> backend = QuasarBackend("classical/simulator")
  >>> backend.has_run_statevector
  True
  >>> backend.run_statevector(circuit=bell_pair)
  array([0.70710678+0.j, 0.        +0.j, 0.        +0.j, 0.70710678+0.j])
  >>> phist = backend.run_measurement(circuit=bell_pair, nmeasurement=1000)
  >>> p
  <quasar.measurement.ProbabilityHistogram object at 0x7f83e0526eb8>
  >>> print(p)
  nqubit       : 2
  nmeasurement : None
  |00> : 0.500000
  |11> : 0.500000


.. autoclass:: qcware.circuits.quasar_backend.QuasarBackend
   :members:
