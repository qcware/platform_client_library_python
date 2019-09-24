
![logo](http://qcwareco.wpengine.com/wp-content/uploads/2019/08/qc-ware-logo-11.png)

# QC Ware Platform Client Library (Python)

This package contains functions for easily interfacing with the QC Ware
Platform from Python.

[![PyPI version](https://badge.fury.io/py/qcware.svg)](https://badge.fury.io/py/qcware) [![Downloads](https://pepy.tech/badge/qcware)](https://pepy.tech/project/qcware) [![Downloads](https://pepy.tech/badge/qcware/month)](https://pepy.tech/project/qcware/month) [![CircleCI](https://circleci.com/gh/qcware/platform_client_library_python.svg?style=svg)](https://circleci.com/gh/qcware/platform_client_library_python)

To install with pip:
```shell
pip install qcware
```
Or, to install from source:
```shell
git clone https://github.com/qcware/platform_client_library_python.git
cd platform_client_library_python
pip install -e .
```

Sign up for an API key at [https://forge.qcware.com](https://forge.qcware.com) to access *Forge*. Please see our [documentation](https://qcware.readthedocs.io).

## Using QC Ware Forge
From your Forge dashboard, you will have access to many notebooks with detailed tutorials and examples. Below we will show a few Hello World examples.

### Optimization
Consider the following optimization problem: 

![img](https://latex.codecogs.com/png.latex?$$x^*&space;=&space;\min_{x\in&space;\{0,&space;1&space;\}^3}&space;\left(x_0&space;x_1&space;&plus;&space;2x_0x_2&space;-&space;x_1x_2&space;&plus;&space;x_0&space;-&space;3x_1\right)$$)

We can solve this with the `qcware` software package. First, create a QUBO representation (see the [notebooks](https://forge.qcware.com) for details).
```python
Q = {(0, 1): 1, (0, 2): 2, (1, 2): -1, (0, 0): 1, (1, 1): -3}
``` 
Next, choose a solver. For example, to solve the problem with D'Wave's quantum annealer, set the solver argument to `'dwave_hw'`.
```python
solver = 'dwave_hw'
```
Finally, call the solver.
```python
import qcware

API_KEY = 'enter api key'
result = qcware.optimization.solve_binary(key=API_KEY, Q=Q, solver=solver)
print(result)
```
Your account dashboard has information on all the available solvers that can be used.

### Chemistry
Consider trying to find the ground state energy of the H2 molecule with a given bond distance `d`. This can be done with the [Variational Quantum Eigensolver](https://arxiv.org/abs/1304.3061) with the `qcware.physics` library.

```python
import qcware 

API_KEY = 'enter api key'

geometry_data = [['H',[0,0,0]],['H',[0,0,d]]]

# find ground state energy for the configuration of the hydrogen molecule provided
h2_energy_1 = qcware.physics.find_ground_state_energy(
    molecule=geometry_data,
    key=QCWARE_API_KEY
)
print(h2_energy_1) 
```

### Quantum Machine learning
The `qcware.qml` library contains `fit_and_predict` functionality. Consider the training data `X`, the training labels `y`, and the test data `T`.

```python
import numpy as np

X = np.array([[-1,-2, 2, -1], [-1, -1, 2,0], [2,1, -2, -1], [1,2, 0, -1]])
y = np.array([0, 0, 1, 1])
T = np.array([[1, -2, 2,1]])
```

We use a quantum machine learning algorithm to classify the data point in `T` based on the `X, y` training data.

```python
result = qcware.qml.fit_and_predict(key=key, X=X, y=y, T=T)
print(result)
```

Please see the [documentation](https://qcware.readthedocs.io) and [notebooks](https://forge.qcware.com) for more details.
