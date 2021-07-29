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


You can then run the circuit by using
the quasar forge backend.

Using the quasar Forge backend:
```````````````````````````````

The `QuasarBackend` class provides a more integrated backend to Quasar using Forge
as a platform.  You can import the class from `qcware.forge.circuits.quasar_backend`
and use it as shown below::

  >>> from qcware.forge.circuits.quasar_backend import QuasarBackend
  >>> backend = QuasarBackend("qcware/cpu_simulator")
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


The `QuasarBackend` class supports all the features of the Quasar backends
(please see the Quasar documentation `here <https://qcware-quasar.readthedocs.io>`_ )
