
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

Sign up for an API key at [https://forge.qcware.com](https://forge.qcware.com) to access *Forge*. 

## Using QC Ware Forge
From your Forge dashboard, you will have access to many notebooks with detailed tutorials and examples. Below we will show a few Hello World examples.

### Optimization
Consider the following optimization problem: 
![img](http://www.sciweavers.org/tex2img.php?eq=%24%24x%5E%2A%20%3D%20%5Cmin_%7Bx%5Cin%20%5C%7B0%2C%201%20%5C%7D%5E3%7D%20%5Cleft%28x_0%20x_1%20%2B%202x_0x_2%20-%20x_1x_2%20%20%2B%20x_0%20-%203x_1%5Cright%29%24%24&bc=White&fc=Black&im=png&fs=12&ff=arev&edit=0)
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
