#  AUTO-GENERATED FILE - MODIFY AT OWN RISK
#  Project: qcware
#  Copyright (c) 2019 QC Ware Corp - All Rights Reserved


  
import asyncio
from .. import logger
from ..api_calls import post_call, wait_for_call, handle_result
from ..util.transforms import client_args_to_wire
from ..exceptions import ApiTimeoutError  


def solve_binary(Q:dict, backend:str, constraints_linear_A:list=[], constraints_linear_b:list=[], constraints_sat_max_runs:int=3100, constraints_hard:bool=False, constraints_penalty_scaling_factor:int=1, constraints_equality_R:list=[], constraints_equality_c:list=[], constraints_inequality_S:list=[], constraints_inequality_d:list=[], return_all_solutions:bool=False, num_runs:int=50, dwave_algorithm:str=None, dwave_solver_limit:str=None, dwave_target_energy:str=None, dwave_find_max:str=None, dwave_reduce_intersample_correlation:str=None, dwave_num_spin_reversal_transforms:str=None, dwave_programming_thermalization:str=None, dwave_reinitialize_state:str=None, dwave_anneal_offsets:str=None, dwave_anneal_offsets_delta:str=None, dwave_num_reads:str=None, dwave_max_answers:str=None, dwave_flux_biases:str=None, dwave_beta:str=None, dwave_answer_mode:str=None, dwave_auto_scale:str=None, dwave_postprocess:str=None, dwave_annealing_time:str=None, dwave_anneal_schedule:str=None, dwave_initial_state:str=None, dwave_chains:str=None, dwave_flux_drift_compensation:bool=None, dwave_beta_range:str=None, dwave_num_sweeps:str=None, dwave_precision_ancillas:str=None, dwave_precision_ancillas_tuples:str=None, constraints_hard_num:int=4, sa_num_sweeps:int=200, use_sample_persistence:bool=False, sample_persistence_solution_threshold:float=0.5, sample_persistence_persistence_threshold:float=0.5, sample_persistence_persistence_iterations:int=0, google_num_steps:int=1, google_n_samples:int=1000, google_arguments_optimizer:dict={}, google_step_sampling:bool=True, google_n_samples_step_sampling:int=1000, number_of_blocks:int=1, iterations:int=50, initial_solution:list=None, always_update_with_best:bool=True, update_q_each_block_solution:bool=True, qaoa_nmeasurement:int=None, qaoa_optimizer:str='COBYLA', qaoa_beta:float=None, qaoa_gamma:float=None, qaoa_p_val:int=1, api_key:str=None, host:str=None):
    r"""Solve a binary optimization problem using one of the solvers provided by the platform.
This function solves a binary optimization problem that is either
  * Unconstrained (quadratic or higher order)
  * Linearly and/or quadratically Constrained (quadratic)
  
Constraints may be linear or quadratic.  Specifically, the function is capable of solving a function of the form

.. math::
    \min_x x^T& Q x \\
    
    \text{such that} \hspace{4em} Ax &= b \\
    
    x^T R_i x &= c_i \\
    
    x^T S_i x &\geq d_i \\

Here, :math:`x` is a length-:math:`n` vector of binary values, i.e., :math:`\{0,1\}^n` (this is what the solver finds).  :math:`Q` is a :math:`(n\times n)` matrix of reals.  :math:`A` is a :math:`(m \times n)` matrix of reals (partially specifying :math:`m` different linear constraints).  :math:`b` is a length-:math:`m` vector of reals (specifying the other component of `m` different linear constraints).  Every :math:`R_i` and :math:`S_i` is a :math:`(n \times n)` matrix of reals, and every :math:`c_i` and :math:`d_i` is a real constant.  The :math:`(R_i, c_i)` pairs specify quadratic equality constraints, and the :math:`(S_i, d_i)` pairs specify quadratic inequality constraints.

In the simplest case, the only variables required to be passed to this function are a valid access key for the platform and a dictionary representing a QUBO.  Additional options are available to:
  
    * Specify constraints for a problem
    * Select different solvers (note: different accounts have different solvers available)
    * Specify solver-specific parameters
    

Error handling is provided by the platform, and warnings and errors that are detected while attempting to run a problem are returned in the JSON object returned by this function.

Possible warnings include:
  

+--------------+--------------------------------------------------------------------+
| Warning Code | Warning Message                                                    |
+==============+====================================================================+
| 7            | Precision required not supported by the machine, still proceeding. |
+--------------+--------------------------------------------------------------------+
| 10           | Hardware solver failed, solving in software solver.                |
+--------------+--------------------------------------------------------------------+
| 22           | Automatic parameter setting failed; solving using default values.  |
+--------------+--------------------------------------------------------------------+

Possible errors include:

+------------+----------------------------------------+
| Error Code | Error Message                          |
+============+========================================+
| 6          | Integer formulation for HFS not found. |
+------------+----------------------------------------+
| 11         | D-Wave hardware solver returned error. |
+------------+----------------------------------------+
| 100        | Invalid solver selected.               |
+------------+----------------------------------------+

It is strongly recommended to wrap a call to :obj:`solve_binary` in a try/catch block since it is possible for the platform or the client library to raise an exception.

Arguments:

:param Q: The objective function matrix in the optimization problem described above.  In the case of a quadratic problem, this is a 2D matrix; generally, in the case of higher-order problems, this is an :math:`n`-dimensional matrix (a tensor). Since :math:`Q` is usually sparse, :math:`Q` should be specified as a Python dictionary with integer or string pairs :math:`(i,j)` as keys (representing the :math:`(i,j)`th entry of :math:`Q`) and integer or float values.  In the case of a cubic function, for example, some dictionary keys will be 3-tuples of integers, rather than pairs. Alternatively, :math:`Q` may be specified as a numpy array or list, in which case :obj:`mat_to_dict` is called on :math:`Q` before sending it to the platform.  Note that that helper function assumes :math:`Q` is symmetric, which may not be true in general. It is strongly encouraged to format :math:`Q` is a dictionary.
:type Q: dict

:param backend: The name of the backend to use for the given problem.  Currently valid values are:

  * "dwave": Run on a physical d-wave machine using quantum annealing
  * "classical": Run on a classical computing backend using a brute-force solver
  * "classical/simulator": Run on a classical computing simulation of a quantum computer, using QAOA
  * "vulcan/simulator": Run on a gpu-accelerated simulation of a quantum computer, using QAOA
:type backend: str

:param constraints_linear_A: The :math:`A` matrix for specifying linear constraints.  :math:`A` should be formatted as a two-dimensional Python list.  Default value :obj:`[]`., defaults to []
:type constraints_linear_A: list

:param constraints_linear_b: The :math:`b` vector for specifying linear constraints.  :math:`b` should be formatted as a one-dimensional Python list.  Default value :obj:`[]`., defaults to []
:type constraints_linear_b: list

:param constraints_sat_max_runs: The maximum number of iterations the platform should run in order to find a formulation where all constraints are satisfied.  Default value :obj:`3100`., defaults to 3100
:type constraints_sat_max_runs: int

:param constraints_hard: Whether to strictly enforce all constraints; if :obj:`False`, constraint penalties may be low enough such that constraints are violated, with the benefit of an improved energy landscape.  Default value :obj:`False`., defaults to False
:type constraints_hard: bool

:param constraints_penalty_scaling_factor: An extra constant scaling factor for the Lagrange multipliers associated with the penalty terms for the constraints.  This may be helpful if constraints are being violated too much or too often.  Default value 1., defaults to 1
:type constraints_penalty_scaling_factor: int

:param constraints_equality_R: The :math:`R` matrices for specifying quadratic equality constraints.  :math:`R` should be formatted as a list of two-dimensional lists (i.e., a list of matrices). Default value :obj:`[]`., defaults to []
:type constraints_equality_R: list

:param constraints_equality_c: The :math:`c` vectors for specifying quadratic equality constraints.  :math:`c` should be formatted as a list of one-dimensional Python lists (i.e., a list of vectors).  Default value :obj:`[]`., defaults to []
:type constraints_equality_c: list

:param constraints_inequality_S: The :math:`S` matrices for specifying quadratic inequality constraints.  :math:`S` should be formatted as a list of two-dimensional lists (i.e., a list of matrices). Default value :obj:`[]`., defaults to []
:type constraints_inequality_S: list

:param constraints_inequality_d: The :math:`d` vectors for specifying quadratic inequality constraints.  :math:`d` should be formatted as a list of one-dimensional Python lists (i.e., a list of vectors).  Default value :obj:`[]`., defaults to []
:type constraints_inequality_d: list

:param return_all_solutions: Whether to return all the candidate solutions found for a problem; if :obj:`False`, the platform will only return the solution corresponding to the lowest energy found. Default value :obj:`False`., defaults to False
:type return_all_solutions: bool

:param num_runs: The number of iterations to run with the selected solver.  Default value :obj:`50`., defaults to 50
:type num_runs: int

:param dwave_algorithm: , defaults to None
:type dwave_algorithm: str

:param dwave_solver_limit: , defaults to None
:type dwave_solver_limit: str

:param dwave_target_energy: , defaults to None
:type dwave_target_energy: str

:param dwave_find_max: , defaults to None
:type dwave_find_max: str

:param dwave_reduce_intersample_correlation: D-Wave hardware system parameter. See `reduce_intersample_correlation <https://docs.dwavesys.com/docs/latest/c_solver_1.html#reduce-intersample-correlation>`_., defaults to None
:type dwave_reduce_intersample_correlation: str

:param dwave_num_spin_reversal_transforms: D-Wave hardware system parameter. See `num_spin_reversal_transforms <https://docs.dwavesys.com/docs/latest/c_solver_1.html#num-spin-reversal-transforms>`_.                , defaults to None
:type dwave_num_spin_reversal_transforms: str

:param dwave_programming_thermalization: D-Wave hardware system parameter. See `programming_thermalization <https://docs.dwavesys.com/docs/latest/c_solver_1.html#programming-thermalization>`_., defaults to None
:type dwave_programming_thermalization: str

:param dwave_reinitialize_state: D-Wave hardware system parameter. See `reinitialize_state <https://docs.dwavesys.com/docs/latest/c_solver_1.html#reinitialize-state>`_., defaults to None
:type dwave_reinitialize_state: str

:param dwave_anneal_offsets: D-Wave hardware system parameter. See `anneal_offsets <https://docs.dwavesys.com/docs/latest/c_solver_1.html#anneal-offsets>`_., defaults to None
:type dwave_anneal_offsets: str

:param dwave_anneal_offsets_delta: Parameter greater or equal to 0 that is used to generate anneal offsets, cannot be specified if dwave_anneal_offsets is also specified. We recommend the value to be in [0, 0.05]. See `<https://arxiv.org/pdf/1806.11091.pdf>`_., defaults to None
:type dwave_anneal_offsets_delta: str

:param dwave_num_reads: D-Wave hardware system parameter. See `num_reads <https://docs.dwavesys.com/docs/latest/c_solver_1.html#num-reads>`_., defaults to None
:type dwave_num_reads: str

:param dwave_max_answers: D-Wave hardware system parameter. See `max_answers <https://docs.dwavesys.com/docs/latest/c_solver_1.html#max-answers>`_., defaults to None
:type dwave_max_answers: str

:param dwave_flux_biases: D-Wave hardware system parameter. See `flux_biases <https://docs.dwavesys.com/docs/latest/c_solver_1.html#flux-biases>`_., defaults to None
:type dwave_flux_biases: str

:param dwave_beta: D-Wave hardware system parameter. See `beta <https://docs.dwavesys.com/docs/latest/c_solver_1.html#beta>`_.                , defaults to None
:type dwave_beta: str

:param dwave_answer_mode: D-Wave hardware system parameter. See `answer_mode <https://docs.dwavesys.com/docs/latest/c_solver_1.html#answer-mode>`_., defaults to None
:type dwave_answer_mode: str

:param dwave_auto_scale: D-Wave hardware system parameter. See `auto_scale <https://docs.dwavesys.com/docs/latest/c_solver_1.html#auto-scale>`_., defaults to None
:type dwave_auto_scale: str

:param dwave_postprocess: D-Wave hardware system parameter. See `postprocess <https://docs.dwavesys.com/docs/latest/c_solver_1.html#postprocess>`_., defaults to None
:type dwave_postprocess: str

:param dwave_annealing_time: D-Wave hardware system parameter. See `annealing_time <https://docs.dwavesys.com/docs/latest/c_solver_1.html#annealing-time>`_., defaults to None
:type dwave_annealing_time: str

:param dwave_anneal_schedule: D-Wave hardware system parameter. See `anneal_schedule <https://docs.dwavesys.com/docs/latest/c_solver_1.html#anneal-schedule>`_., defaults to None
:type dwave_anneal_schedule: str

:param dwave_initial_state: D-Wave hardware system parameter. See `initial_state <https://docs.dwavesys.com/docs/latest/c_solver_1.html#initial-state>`_., defaults to None
:type dwave_initial_state: str

:param dwave_chains: D-Wave hardware system parameter. See `chains <https://docs.dwavesys.com/docs/latest/c_solver_1.html#chains>`_., defaults to None
:type dwave_chains: str

:param dwave_flux_drift_compensation: D-Wave hardware system parameter. See `flux_drift_compensation <https://docs.dwavesys.com/docs/latest/c_solver_1.html#flux-drift-compensation>`_., defaults to None
:type dwave_flux_drift_compensation: bool

:param dwave_beta_range: D-Wave software system parameter. See `beta_range <https://docs.ocean.dwavesys.com/projects/dimod/en/latest/reference/generated/dimod.reference.samplers.SimulatedAnnealingSampler.sample.html>`_., defaults to None
:type dwave_beta_range: str

:param dwave_num_sweeps: D-Wave software system parameter. See `num_sweeps <https://docs.ocean.dwavesys.com/projects/dimod/en/latest/reference/generated/dimod.reference.samplers.SimulatedAnnealingSampler.sample.html>`_., defaults to None
:type dwave_num_sweeps: str

:param dwave_precision_ancillas: , defaults to None
:type dwave_precision_ancillas: str

:param dwave_precision_ancillas_tuples: , defaults to None
:type dwave_precision_ancillas_tuples: str

:param constraints_hard_num: , defaults to 4
:type constraints_hard_num: int

:param sa_num_sweeps: If using a simulated annealing solver, how many sweeps to perform per run of the algorithm.  Default value :obj:`200`., defaults to 200
:type sa_num_sweeps: int

:param use_sample_persistence: Whether to use the sample persistence method of https://arxiv.org/abs/1606.07797 , which aims to improve the probability of a quantum annealer to obtain an optimal solution., defaults to False
:type use_sample_persistence: bool

:param sample_persistence_solution_threshold: A threshold that is used to filter out higher-energy candidate solutions from the sample persistence method.  A percentage that ranges from 0 to 1., defaults to 0.5
:type sample_persistence_solution_threshold: float

:param sample_persistence_persistence_threshold: A threshold between 0 and 1 such that a variable is fixed if its mean absolute value across the filtered sample is larger than the value of the threshold.  Called fixing_threshold in the original paper., defaults to 0.5
:type sample_persistence_persistence_threshold: float

:param sample_persistence_persistence_iterations: The number of iterations to run the sample persistence algorithm.  Generally speaking, more iterations will make the algorithm more successful, at the cost of increased computation time., defaults to 0
:type sample_persistence_persistence_iterations: int

:param google_num_steps: The number of QAOA steps implemented by the algorithm.  Default value :obj:`1`., defaults to 1
:type google_num_steps: int

:param google_n_samples: The number of runs corresponding to the final sampling step.  Default value :obj:`1000`., defaults to 1000
:type google_n_samples: int

:param google_arguments_optimizer: The dictionary that contains the parameters of the bayesian-optimization optimizer.  Default value :obj:`{'init_point': 10, 'number_iter': 20, 'kappa': 2}`., defaults to {}
:type google_arguments_optimizer: dict

:param google_step_sampling: Whether to sample the circuit with the current parameters at every step of the optimization (True) or just at the final one.  Default value :obj:`True`., defaults to True
:type google_step_sampling: bool

:param google_n_samples_step_sampling: The number of runs corresponding to sampling at every step of the optimization.  Default value :obj:`1000`., defaults to 1000
:type google_n_samples_step_sampling: int

:param number_of_blocks: number of blocks to decompose problem into using random decomposition. Default value :obj: `1` meaning no decomposition., defaults to 1
:type number_of_blocks: int

:param iterations: number of iterations to cycle through when using random decomposition. Only valid if :obj: `number_of_blocks` is greater than 1. Each iterations corresponds to solving all blocks of the decomposition once. Default value :obj:`50`., defaults to 50
:type iterations: int

:param initial_solution: initial solution seed for constructing the blocks using random decomposition. If none is provided, a random solution is initialized. Default value :obj: `None`. :obj:`initial_solution` should be the same type as :obj:`Q`../, defaults to None
:type initial_solution: list

:param always_update_with_best: solutions found using decomposition do not monotonically get better with each iterations. The best solution is always returned, but this flag determines whether or not to construct new decomposition using best solution. Default value :obj: `True`., defaults to True
:type always_update_with_best: bool

:param update_q_each_block_solution: each blocks decomposed Q matrix can be constructed at the onset of block composition, or updated every time a block is solved. Default value :obj: `True`., defaults to True
:type update_q_each_block_solution: bool

:param qaoa_nmeasurement: The number of measurements to use for the QAOA algorithm if a simulator is chosen.  Leave at null to attempt an ideal Pauli measurement, defaults to None
:type qaoa_nmeasurement: int

:param qaoa_optimizer: The optimizer to use for the QAOA algorithm if a simulator backend is chosen.  Valid options are `COBYLA`, `bounded_Powell`, and `analytical`, or `None` if qaoa_beta and qaoa_gamma are provided, defaults to COBYLA
:type qaoa_optimizer: str

:param qaoa_beta: A :math:`\beta` angle(s) to provide to the QAOA algorithm if a simulator backend is chosen.  This can either be a float or a list of floats of length `qaoa_p_val`.  Invalid unless qaoa_gamma is also provided and has the same length., defaults to None
:type qaoa_beta: float

:param qaoa_gamma: A :math:`\gamma` angle(s) to provide to the QAOA algorithm if a simulator backend is chosen.  This can either be a float or a list of floats of length `qaoa_p_val`.  Invalid unless qaoa_beta is also provided and has the same length., defaults to None
:type qaoa_gamma: float

:param qaoa_p_val: A p_val to provide the qaoa algorithm if a simulator backend is chosen.  Must be equal to the number of :math:`\beta` and :math:`\gamma` angles provided in `qaoa_beta` and `qaoa_gamma`., defaults to 1
:type qaoa_p_val: int


:return: A dict, containing zero or more of the fields:

  * 'solution' (:obj:`dict`): A Python dictionary representing the solution vector.  If :obj:`return_all_solutions` is
    :obj:`True`, this is a list of dicts. However, if the input :obj:`Q` is a 2D numpy array, then each :obj`solution` will
    be a 1D numpy array; if the input :obj:`Q` is a list of lists, then each :obj`solution` will also be a list. :obj`solution`
    maps variables labels to their binary values, thus :obj`solution[i]` is the value of the :obj`i`th binary variable.
  * 'num_runs' (:obj:`int`): How many total runs of the chosen solver were performed in order to produce the
    returned solution.
  * 'num_qubits' (:obj:`int`): How many physical qubits (or simulated qubits, in the case of a software
    solver) were used for solving the problem.
  * 'num_logical_variables' (:obj:`int`): How many logical variables were contained in the problem.
  * 'warnings' (:obj:`list`): A list of strings containing warning messages from the platform generated when
    attempting to solve the problem.  This key does not exist if no warnings were raised.
  * 'warning_codes' (:obj:`list`): A list of ints containing warning codes from the platform generated when
    attempting to solve the problem.  This key does not exist if no warnings were raised.
  * 'error' (:obj:`str`): A string containing an error message from the platform generated when
    attempting to solve the problem.  This key does not exist if no error occurred.
  * 'error_code' (:obj:`int`): An int containing an error codes from the platform generated when
    attempting to solve the problem.  This key does not exist if no error occurred.
  * 'extra_info' (:obj:`list`): A Python list containing additional information returned by a solver.

  
:rtype: dict
    """
    data = client_args_to_wire('optimization.solve_binary', **locals())
    api_call = post_call('optimization/solve_binary', data, host=host )
    logger.info(f'API call to optimization.solve_binary successful. Your API token is {api_call["uid"]}')
    return handle_result(wait_for_call(api_key=api_key,
                                       host=host,
                                       call_token=api_call['uid']))


async def async_solve_binary(Q:dict, backend:str, constraints_linear_A:list=[], constraints_linear_b:list=[], constraints_sat_max_runs:int=3100, constraints_hard:bool=False, constraints_penalty_scaling_factor:int=1, constraints_equality_R:list=[], constraints_equality_c:list=[], constraints_inequality_S:list=[], constraints_inequality_d:list=[], return_all_solutions:bool=False, num_runs:int=50, dwave_algorithm:str=None, dwave_solver_limit:str=None, dwave_target_energy:str=None, dwave_find_max:str=None, dwave_reduce_intersample_correlation:str=None, dwave_num_spin_reversal_transforms:str=None, dwave_programming_thermalization:str=None, dwave_reinitialize_state:str=None, dwave_anneal_offsets:str=None, dwave_anneal_offsets_delta:str=None, dwave_num_reads:str=None, dwave_max_answers:str=None, dwave_flux_biases:str=None, dwave_beta:str=None, dwave_answer_mode:str=None, dwave_auto_scale:str=None, dwave_postprocess:str=None, dwave_annealing_time:str=None, dwave_anneal_schedule:str=None, dwave_initial_state:str=None, dwave_chains:str=None, dwave_flux_drift_compensation:bool=None, dwave_beta_range:str=None, dwave_num_sweeps:str=None, dwave_precision_ancillas:str=None, dwave_precision_ancillas_tuples:str=None, constraints_hard_num:int=4, sa_num_sweeps:int=200, use_sample_persistence:bool=False, sample_persistence_solution_threshold:float=0.5, sample_persistence_persistence_threshold:float=0.5, sample_persistence_persistence_iterations:int=0, google_num_steps:int=1, google_n_samples:int=1000, google_arguments_optimizer:dict={}, google_step_sampling:bool=True, google_n_samples_step_sampling:int=1000, number_of_blocks:int=1, iterations:int=50, initial_solution:list=None, always_update_with_best:bool=True, update_q_each_block_solution:bool=True, qaoa_nmeasurement:int=None, qaoa_optimizer:str='COBYLA', qaoa_beta:float=None, qaoa_gamma:float=None, qaoa_p_val:int=1, api_key:str=None, host:str=None):
    r"""Async version of solve_binary
Solve a binary optimization problem using one of the solvers provided by the platform.
This function solves a binary optimization problem that is either
  * Unconstrained (quadratic or higher order)
  * Linearly and/or quadratically Constrained (quadratic)
  
Constraints may be linear or quadratic.  Specifically, the function is capable of solving a function of the form

.. math::
    \min_x x^T& Q x \\
    
    \text{such that} \hspace{4em} Ax &= b \\
    
    x^T R_i x &= c_i \\
    
    x^T S_i x &\geq d_i \\

Here, :math:`x` is a length-:math:`n` vector of binary values, i.e., :math:`\{0,1\}^n` (this is what the solver finds).  :math:`Q` is a :math:`(n\times n)` matrix of reals.  :math:`A` is a :math:`(m \times n)` matrix of reals (partially specifying :math:`m` different linear constraints).  :math:`b` is a length-:math:`m` vector of reals (specifying the other component of `m` different linear constraints).  Every :math:`R_i` and :math:`S_i` is a :math:`(n \times n)` matrix of reals, and every :math:`c_i` and :math:`d_i` is a real constant.  The :math:`(R_i, c_i)` pairs specify quadratic equality constraints, and the :math:`(S_i, d_i)` pairs specify quadratic inequality constraints.

In the simplest case, the only variables required to be passed to this function are a valid access key for the platform and a dictionary representing a QUBO.  Additional options are available to:
  
    * Specify constraints for a problem
    * Select different solvers (note: different accounts have different solvers available)
    * Specify solver-specific parameters
    

Error handling is provided by the platform, and warnings and errors that are detected while attempting to run a problem are returned in the JSON object returned by this function.

Possible warnings include:
  

+--------------+--------------------------------------------------------------------+
| Warning Code | Warning Message                                                    |
+==============+====================================================================+
| 7            | Precision required not supported by the machine, still proceeding. |
+--------------+--------------------------------------------------------------------+
| 10           | Hardware solver failed, solving in software solver.                |
+--------------+--------------------------------------------------------------------+
| 22           | Automatic parameter setting failed; solving using default values.  |
+--------------+--------------------------------------------------------------------+

Possible errors include:

+------------+----------------------------------------+
| Error Code | Error Message                          |
+============+========================================+
| 6          | Integer formulation for HFS not found. |
+------------+----------------------------------------+
| 11         | D-Wave hardware solver returned error. |
+------------+----------------------------------------+
| 100        | Invalid solver selected.               |
+------------+----------------------------------------+

It is strongly recommended to wrap a call to :obj:`solve_binary` in a try/catch block since it is possible for the platform or the client library to raise an exception.


Arguments:

:param Q: The objective function matrix in the optimization problem described above.  In the case of a quadratic problem, this is a 2D matrix; generally, in the case of higher-order problems, this is an :math:`n`-dimensional matrix (a tensor). Since :math:`Q` is usually sparse, :math:`Q` should be specified as a Python dictionary with integer or string pairs :math:`(i,j)` as keys (representing the :math:`(i,j)`th entry of :math:`Q`) and integer or float values.  In the case of a cubic function, for example, some dictionary keys will be 3-tuples of integers, rather than pairs. Alternatively, :math:`Q` may be specified as a numpy array or list, in which case :obj:`mat_to_dict` is called on :math:`Q` before sending it to the platform.  Note that that helper function assumes :math:`Q` is symmetric, which may not be true in general. It is strongly encouraged to format :math:`Q` is a dictionary.
:type Q: dict

:param backend: The name of the backend to use for the given problem.  Currently valid values are:

  * "dwave": Run on a physical d-wave machine using quantum annealing
  * "classical": Run on a classical computing backend using a brute-force solver
  * "classical/simulator": Run on a classical computing simulation of a quantum computer, using QAOA
  * "vulcan/simulator": Run on a gpu-accelerated simulation of a quantum computer, using QAOA
:type backend: str

:param constraints_linear_A: The :math:`A` matrix for specifying linear constraints.  :math:`A` should be formatted as a two-dimensional Python list.  Default value :obj:`[]`., defaults to []
:type constraints_linear_A: list

:param constraints_linear_b: The :math:`b` vector for specifying linear constraints.  :math:`b` should be formatted as a one-dimensional Python list.  Default value :obj:`[]`., defaults to []
:type constraints_linear_b: list

:param constraints_sat_max_runs: The maximum number of iterations the platform should run in order to find a formulation where all constraints are satisfied.  Default value :obj:`3100`., defaults to 3100
:type constraints_sat_max_runs: int

:param constraints_hard: Whether to strictly enforce all constraints; if :obj:`False`, constraint penalties may be low enough such that constraints are violated, with the benefit of an improved energy landscape.  Default value :obj:`False`., defaults to False
:type constraints_hard: bool

:param constraints_penalty_scaling_factor: An extra constant scaling factor for the Lagrange multipliers associated with the penalty terms for the constraints.  This may be helpful if constraints are being violated too much or too often.  Default value 1., defaults to 1
:type constraints_penalty_scaling_factor: int

:param constraints_equality_R: The :math:`R` matrices for specifying quadratic equality constraints.  :math:`R` should be formatted as a list of two-dimensional lists (i.e., a list of matrices). Default value :obj:`[]`., defaults to []
:type constraints_equality_R: list

:param constraints_equality_c: The :math:`c` vectors for specifying quadratic equality constraints.  :math:`c` should be formatted as a list of one-dimensional Python lists (i.e., a list of vectors).  Default value :obj:`[]`., defaults to []
:type constraints_equality_c: list

:param constraints_inequality_S: The :math:`S` matrices for specifying quadratic inequality constraints.  :math:`S` should be formatted as a list of two-dimensional lists (i.e., a list of matrices). Default value :obj:`[]`., defaults to []
:type constraints_inequality_S: list

:param constraints_inequality_d: The :math:`d` vectors for specifying quadratic inequality constraints.  :math:`d` should be formatted as a list of one-dimensional Python lists (i.e., a list of vectors).  Default value :obj:`[]`., defaults to []
:type constraints_inequality_d: list

:param return_all_solutions: Whether to return all the candidate solutions found for a problem; if :obj:`False`, the platform will only return the solution corresponding to the lowest energy found. Default value :obj:`False`., defaults to False
:type return_all_solutions: bool

:param num_runs: The number of iterations to run with the selected solver.  Default value :obj:`50`., defaults to 50
:type num_runs: int

:param dwave_algorithm: , defaults to None
:type dwave_algorithm: str

:param dwave_solver_limit: , defaults to None
:type dwave_solver_limit: str

:param dwave_target_energy: , defaults to None
:type dwave_target_energy: str

:param dwave_find_max: , defaults to None
:type dwave_find_max: str

:param dwave_reduce_intersample_correlation: D-Wave hardware system parameter. See `reduce_intersample_correlation <https://docs.dwavesys.com/docs/latest/c_solver_1.html#reduce-intersample-correlation>`_., defaults to None
:type dwave_reduce_intersample_correlation: str

:param dwave_num_spin_reversal_transforms: D-Wave hardware system parameter. See `num_spin_reversal_transforms <https://docs.dwavesys.com/docs/latest/c_solver_1.html#num-spin-reversal-transforms>`_.                , defaults to None
:type dwave_num_spin_reversal_transforms: str

:param dwave_programming_thermalization: D-Wave hardware system parameter. See `programming_thermalization <https://docs.dwavesys.com/docs/latest/c_solver_1.html#programming-thermalization>`_., defaults to None
:type dwave_programming_thermalization: str

:param dwave_reinitialize_state: D-Wave hardware system parameter. See `reinitialize_state <https://docs.dwavesys.com/docs/latest/c_solver_1.html#reinitialize-state>`_., defaults to None
:type dwave_reinitialize_state: str

:param dwave_anneal_offsets: D-Wave hardware system parameter. See `anneal_offsets <https://docs.dwavesys.com/docs/latest/c_solver_1.html#anneal-offsets>`_., defaults to None
:type dwave_anneal_offsets: str

:param dwave_anneal_offsets_delta: Parameter greater or equal to 0 that is used to generate anneal offsets, cannot be specified if dwave_anneal_offsets is also specified. We recommend the value to be in [0, 0.05]. See `<https://arxiv.org/pdf/1806.11091.pdf>`_., defaults to None
:type dwave_anneal_offsets_delta: str

:param dwave_num_reads: D-Wave hardware system parameter. See `num_reads <https://docs.dwavesys.com/docs/latest/c_solver_1.html#num-reads>`_., defaults to None
:type dwave_num_reads: str

:param dwave_max_answers: D-Wave hardware system parameter. See `max_answers <https://docs.dwavesys.com/docs/latest/c_solver_1.html#max-answers>`_., defaults to None
:type dwave_max_answers: str

:param dwave_flux_biases: D-Wave hardware system parameter. See `flux_biases <https://docs.dwavesys.com/docs/latest/c_solver_1.html#flux-biases>`_., defaults to None
:type dwave_flux_biases: str

:param dwave_beta: D-Wave hardware system parameter. See `beta <https://docs.dwavesys.com/docs/latest/c_solver_1.html#beta>`_.                , defaults to None
:type dwave_beta: str

:param dwave_answer_mode: D-Wave hardware system parameter. See `answer_mode <https://docs.dwavesys.com/docs/latest/c_solver_1.html#answer-mode>`_., defaults to None
:type dwave_answer_mode: str

:param dwave_auto_scale: D-Wave hardware system parameter. See `auto_scale <https://docs.dwavesys.com/docs/latest/c_solver_1.html#auto-scale>`_., defaults to None
:type dwave_auto_scale: str

:param dwave_postprocess: D-Wave hardware system parameter. See `postprocess <https://docs.dwavesys.com/docs/latest/c_solver_1.html#postprocess>`_., defaults to None
:type dwave_postprocess: str

:param dwave_annealing_time: D-Wave hardware system parameter. See `annealing_time <https://docs.dwavesys.com/docs/latest/c_solver_1.html#annealing-time>`_., defaults to None
:type dwave_annealing_time: str

:param dwave_anneal_schedule: D-Wave hardware system parameter. See `anneal_schedule <https://docs.dwavesys.com/docs/latest/c_solver_1.html#anneal-schedule>`_., defaults to None
:type dwave_anneal_schedule: str

:param dwave_initial_state: D-Wave hardware system parameter. See `initial_state <https://docs.dwavesys.com/docs/latest/c_solver_1.html#initial-state>`_., defaults to None
:type dwave_initial_state: str

:param dwave_chains: D-Wave hardware system parameter. See `chains <https://docs.dwavesys.com/docs/latest/c_solver_1.html#chains>`_., defaults to None
:type dwave_chains: str

:param dwave_flux_drift_compensation: D-Wave hardware system parameter. See `flux_drift_compensation <https://docs.dwavesys.com/docs/latest/c_solver_1.html#flux-drift-compensation>`_., defaults to None
:type dwave_flux_drift_compensation: bool

:param dwave_beta_range: D-Wave software system parameter. See `beta_range <https://docs.ocean.dwavesys.com/projects/dimod/en/latest/reference/generated/dimod.reference.samplers.SimulatedAnnealingSampler.sample.html>`_., defaults to None
:type dwave_beta_range: str

:param dwave_num_sweeps: D-Wave software system parameter. See `num_sweeps <https://docs.ocean.dwavesys.com/projects/dimod/en/latest/reference/generated/dimod.reference.samplers.SimulatedAnnealingSampler.sample.html>`_., defaults to None
:type dwave_num_sweeps: str

:param dwave_precision_ancillas: , defaults to None
:type dwave_precision_ancillas: str

:param dwave_precision_ancillas_tuples: , defaults to None
:type dwave_precision_ancillas_tuples: str

:param constraints_hard_num: , defaults to 4
:type constraints_hard_num: int

:param sa_num_sweeps: If using a simulated annealing solver, how many sweeps to perform per run of the algorithm.  Default value :obj:`200`., defaults to 200
:type sa_num_sweeps: int

:param use_sample_persistence: Whether to use the sample persistence method of https://arxiv.org/abs/1606.07797 , which aims to improve the probability of a quantum annealer to obtain an optimal solution., defaults to False
:type use_sample_persistence: bool

:param sample_persistence_solution_threshold: A threshold that is used to filter out higher-energy candidate solutions from the sample persistence method.  A percentage that ranges from 0 to 1., defaults to 0.5
:type sample_persistence_solution_threshold: float

:param sample_persistence_persistence_threshold: A threshold between 0 and 1 such that a variable is fixed if its mean absolute value across the filtered sample is larger than the value of the threshold.  Called fixing_threshold in the original paper., defaults to 0.5
:type sample_persistence_persistence_threshold: float

:param sample_persistence_persistence_iterations: The number of iterations to run the sample persistence algorithm.  Generally speaking, more iterations will make the algorithm more successful, at the cost of increased computation time., defaults to 0
:type sample_persistence_persistence_iterations: int

:param google_num_steps: The number of QAOA steps implemented by the algorithm.  Default value :obj:`1`., defaults to 1
:type google_num_steps: int

:param google_n_samples: The number of runs corresponding to the final sampling step.  Default value :obj:`1000`., defaults to 1000
:type google_n_samples: int

:param google_arguments_optimizer: The dictionary that contains the parameters of the bayesian-optimization optimizer.  Default value :obj:`{'init_point': 10, 'number_iter': 20, 'kappa': 2}`., defaults to {}
:type google_arguments_optimizer: dict

:param google_step_sampling: Whether to sample the circuit with the current parameters at every step of the optimization (True) or just at the final one.  Default value :obj:`True`., defaults to True
:type google_step_sampling: bool

:param google_n_samples_step_sampling: The number of runs corresponding to sampling at every step of the optimization.  Default value :obj:`1000`., defaults to 1000
:type google_n_samples_step_sampling: int

:param number_of_blocks: number of blocks to decompose problem into using random decomposition. Default value :obj: `1` meaning no decomposition., defaults to 1
:type number_of_blocks: int

:param iterations: number of iterations to cycle through when using random decomposition. Only valid if :obj: `number_of_blocks` is greater than 1. Each iterations corresponds to solving all blocks of the decomposition once. Default value :obj:`50`., defaults to 50
:type iterations: int

:param initial_solution: initial solution seed for constructing the blocks using random decomposition. If none is provided, a random solution is initialized. Default value :obj: `None`. :obj:`initial_solution` should be the same type as :obj:`Q`../, defaults to None
:type initial_solution: list

:param always_update_with_best: solutions found using decomposition do not monotonically get better with each iterations. The best solution is always returned, but this flag determines whether or not to construct new decomposition using best solution. Default value :obj: `True`., defaults to True
:type always_update_with_best: bool

:param update_q_each_block_solution: each blocks decomposed Q matrix can be constructed at the onset of block composition, or updated every time a block is solved. Default value :obj: `True`., defaults to True
:type update_q_each_block_solution: bool

:param qaoa_nmeasurement: The number of measurements to use for the QAOA algorithm if a simulator is chosen.  Leave at null to attempt an ideal Pauli measurement, defaults to None
:type qaoa_nmeasurement: int

:param qaoa_optimizer: The optimizer to use for the QAOA algorithm if a simulator backend is chosen.  Valid options are `COBYLA`, `bounded_Powell`, and `analytical`, or `None` if qaoa_beta and qaoa_gamma are provided, defaults to COBYLA
:type qaoa_optimizer: str

:param qaoa_beta: A :math:`\beta` angle(s) to provide to the QAOA algorithm if a simulator backend is chosen.  This can either be a float or a list of floats of length `qaoa_p_val`.  Invalid unless qaoa_gamma is also provided and has the same length., defaults to None
:type qaoa_beta: float

:param qaoa_gamma: A :math:`\gamma` angle(s) to provide to the QAOA algorithm if a simulator backend is chosen.  This can either be a float or a list of floats of length `qaoa_p_val`.  Invalid unless qaoa_beta is also provided and has the same length., defaults to None
:type qaoa_gamma: float

:param qaoa_p_val: A p_val to provide the qaoa algorithm if a simulator backend is chosen.  Must be equal to the number of :math:`\beta` and :math:`\gamma` angles provided in `qaoa_beta` and `qaoa_gamma`., defaults to 1
:type qaoa_p_val: int


:return: A dict, containing zero or more of the fields:

  * 'solution' (:obj:`dict`): A Python dictionary representing the solution vector.  If :obj:`return_all_solutions` is
    :obj:`True`, this is a list of dicts. However, if the input :obj:`Q` is a 2D numpy array, then each :obj`solution` will
    be a 1D numpy array; if the input :obj:`Q` is a list of lists, then each :obj`solution` will also be a list. :obj`solution`
    maps variables labels to their binary values, thus :obj`solution[i]` is the value of the :obj`i`th binary variable.
  * 'num_runs' (:obj:`int`): How many total runs of the chosen solver were performed in order to produce the
    returned solution.
  * 'num_qubits' (:obj:`int`): How many physical qubits (or simulated qubits, in the case of a software
    solver) were used for solving the problem.
  * 'num_logical_variables' (:obj:`int`): How many logical variables were contained in the problem.
  * 'warnings' (:obj:`list`): A list of strings containing warning messages from the platform generated when
    attempting to solve the problem.  This key does not exist if no warnings were raised.
  * 'warning_codes' (:obj:`list`): A list of ints containing warning codes from the platform generated when
    attempting to solve the problem.  This key does not exist if no warnings were raised.
  * 'error' (:obj:`str`): A string containing an error message from the platform generated when
    attempting to solve the problem.  This key does not exist if no error occurred.
  * 'error_code' (:obj:`int`): An int containing an error codes from the platform generated when
    attempting to solve the problem.  This key does not exist if no error occurred.
  * 'extra_info' (:obj:`list`): A Python list containing additional information returned by a solver.

  
:rtype: dict
    """
    data = client_args_to_wire('optimization.solve_binary', **locals())
    api_call = post_call('optimization/solve_binary', data, host=host )
    logger.info(f'API call to optimization.solve_binary successful. Your API token is {api_call["uid"]}')

    while True:
        try:
            return handle_result(wait_for_call(api_key=api_key,
                                               host=host,
                                               call_token=api_call['uid']))
        except ApiTimeoutError as e:
            await asyncio.sleep(5)


