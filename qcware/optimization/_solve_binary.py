"""._solve_binary.py.

Contains the main call to the platform for binary optimization.

"""

from qcware import request
from qcware.wrappers import print_errors, print_api_mismatch
import numpy as np
from . import QUBO, PUBO
from .utils import matrix_to_qubo, SolveBinaryWarning, SolverWarning


__all__ = "solve_binary", "SolveBinaryResult"


class SolveBinaryResult(dict):
    """

    """

    def __init__(self, *args, **kwargs):
        """

        """
        super().__init__(*args, **kwargs)
        for key in self:
            if isinstance(self[key], dict):
                self[key] = SolveBinaryResult(self[key])

    def __getattr__(self, name):
        """

        """
        try:
            return self[name]
        except KeyError:
            raise AttributeError("No attribute %s" % name)

    def __setattr__(self, name, value):
        """

        """
        self[name] = value


def _warnings(params):
    r"""Warn user about their inputs.

    Args:
        params (:obj:`dict`): the input parameters to `solve_binary`.

    Returns:
        None
    """

    # Warn about long computation times
    if params["solver"] == "ibm_hw_qaoa":
        SolverWarning.warn("IBM hardware solver is currently disabled due to"
                           "queue waiting times. Defaulting to ibm_sw_qaoa "
                           "for this run.")
        params["solver"] = "ibm_sw_qaoa"

    # Warn about parameters not being used
    if "dwave_anneal_offsets" in params and "dwave_anneal_offsets_delta" in params:
        SolveBinaryWarning.warn("`dwave_anneal_offsets` and `dwave_anneal_offsets_delta` "
                                "are not both used in the same call.")

    # TODO: more warnings. ie any inconsistencies that the user provides, etc.


_solution_keys = {"solution", "all_solutions", "unique_solutions", "most_common_measurement"}


def _recursively_convert_solutions(result, convert_solution):
    r"""Convert solutions with their enumeration.

    The output of the request to `solve_binary` is a dictionary with various
    keys. `mapping` is a `dict` that maps indicies of the solutions lists to
    the keys that the user originally used in their QUBO `dict`. This
    function recursively goes through the result and converts all solution
    lists to a dictionary that maps the user's original keys to the correct
    values. Note that the `result` dictionary is modified in place!

    Args:
        result (:obj:`dict`): The output of `qcware.optimization.solve_binary`.
        convert_solution (:obj:`function`):
            A function that takes in a solution and converts it.

    Returns:
        None. The :obj:`result` dictionary is modified in place.
    """
    # through recursive calls
    if isinstance(result, list):
        try:
            return convert_solution(result)
        except (KeyError, TypeError, IndexError):
            return [_recursively_convert_solutions(x, convert_solution) for x in result]

    elif isinstance(result, dict):
        for k, v in tuple(result.items()):
            if isinstance(v, dict):
                _recursively_convert_solutions(v, convert_solution)
            elif k in _solution_keys:
                result[k] = _recursively_convert_solutions(v, convert_solution)


# Note: this is good for both HOBOs and QUBOs
@print_api_mismatch
@print_errors
def solve_binary(
        key,
        Q,
        solver="dwave_hw",
        constraints_linear_A=[],
        constraints_linear_b=[],
        constraints_sat_max_runs=3100,
        constraints_hard=False,
        constraints_penalty_scaling_factor=1,
        constraints_equality_R=[],
        constraints_equality_c=[],
        constraints_inequality_S=[],
        constraints_inequality_d=[],
        return_all_solutions=False,
        num_runs=50,
        dwave_algorithm=None,
        dwave_solver_limit=None,
        dwave_target_energy=None,
        dwave_find_max=None,
        dwave_reduce_intersample_correlation=None,
        dwave_num_spin_reversal_transforms=None,
        dwave_programming_thermalization=None,
        dwave_reinitialize_state=None,
        dwave_anneal_offsets=None,
        dwave_anneal_offsets_delta=None,
        dwave_num_reads=None,
        dwave_max_answers=None,
        dwave_flux_biases=None,
        dwave_beta=None,
        dwave_answer_mode=None,
        dwave_auto_scale=None,
        dwave_postprocess=None,
        dwave_annealing_time=None,
        dwave_anneal_schedule=None,
        dwave_initial_state=None,
        dwave_chains=None,
        dwave_flux_drift_compensation=None,
        dwave_beta_range=None,
        dwave_num_sweeps=None,
        dwave_precision_ancillas=None,
        dwave_precision_ancillas_tuples=None,
        constraints_hard_num=4,
        sa_num_sweeps=200,
        use_sample_persistence=False,
        sample_persistence_solution_threshold=0.5,
        sample_persistence_persistence_threshold=0.5,
        sample_persistence_persistence_iterations=0,
        google_num_steps=1,
        google_n_samples=1000,
        google_arguments_optimizer={},
        google_step_sampling=True,
        google_n_samples_step_sampling=1000,
        number_of_blocks=1,
        iterations=50,
        initial_solution=None,
        always_update_with_best=True,
        update_q_each_block_solution=True,
        convert_solution=None,
        host="https://api.forge.qcware.com",
        ):
    r"""Solve a binary optimization problem using one of the solvers provided by the platform.

    This function solves a binary optimization problem that is either:
        * Unconstrained (quadratic or higher order)
        * Linearly and/or quadratically Constrained (quadratic)

    Constraints may be linear or quadratic.  Specifically, the function is capable of solving a function of the form

    .. math::
        \min_x x^T Q x \\
        \text{such that} \\
        Ax = b \\
        x^T R_i x = c_i \\
        x^T S_i x \geq d_i \\

    Here, :math:`x` is a length-:math:`n` vector of binary values, i.e., :math:`\{0,1\}^n` (this is what the solver
    finds).  :math:`Q` is a :math:`(n\times n)` matrix of reals.  :math:`A` is a :math:`(m \times n)` matrix of reals
    (partially specifying :math:`m` different linear constraints).  :math:`b` is a length-:math:`m` vector of reals
    (specifying the other component of `m` different linear constraints).  Every :math:`R_i` and :math:`S_i` is a
    :math:`(n \times n)` matrix of reals, and every :math:`c_i` and :math:`d_i` is a real constant.  The
    :math:`(R_i, c_i)` pairs specify quadratic equality constraints, and the :math:`(S_i, d_i)` pairs specify
    quadratic inequality constraints.

    In the simplest case, the only variables required to be passed to this function are a valid access key for the platform and a dictionary representing a QUBO.  Additional options are available to:
        * Specify constraints for a problem
        * Select different solvers (note: different accounts have different solvers available)
        * Specify solver-specific parameters

    Error handling is provided by the platform, and warnings and errors that are detected while attempting to run a
    problem are returned in the JSON object returned by this function.

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

    It is strongly recommended to wrap a call to :obj:`solve_binary` in a try/catch block since it is possible for the
    platform or the client library to raise an exception.

    Args:
        key (:obj:`str`):
            An API key for the platform.
            Keys can be allocated and managed from the Forge web portal.

        Q (:obj:`dict`):
            The objective function matrix in the optimization problem
            described above.  In the case of a quadratic problem, this is a
             2D matrix; generally, in the case of higher-order problems,
             this is an :math:`n`-dimensional matrix (a tensor).

            Since :math:`Q` is usually sparse, :math:`Q` should be specified
            as a Python dictionary with integer or string pairs :math:`(i,j)` as keys (representing the :math:`(i,j)`th
            entry of :math:`Q`) and integer or float values.  In the case of a cubic function, for example, some
            dictionary keys will be 3-tuples of integers, rather than pairs.

            Alternatively, :math:`Q` may be specified as a numpy array or list, in which case :obj:`mat_to_dict` is called on
            :math:`Q` before sending it to the platform.  Note that that helper function assumes :math:`Q` is symmetric,
            which may not be true in general. It is strongly encouraged to format :math:`Q` is a dictionary.

        solver (:obj:`str`, optional):
            The name of the solver to use for the given problem.  Valid values are:

            * "dwave_hw": Run on a physical D-Wave machine
            * "brute_force": Run using a brute force algorithm
            * "hfs": Run using the Hamze-de Freitas-Selby algorithm
            * "google_sw_qaoa": Run using the Google simulator implementation of the QAOA algorithm
            * "ibm_hw_qaoa": This solver is currently disabled due to queue issues.
                Run the QAOA algorithm on a physical IBM machine, this may take over 2 hours for even small problems!
            * "ibm_sw_qaoa": Run the QAOA algorithm on IBM's software simulator of the QAOA algorithm


            Note that only certain solvers may be enabled depending on your account.  Default value "dwave_hw".

        constraints_linear_A (:obj:`list`, optional):
            The :math:`A` matrix for specifying linear constraints.  :math:`A`
            should be formatted as a two-dimensional Python list.  Default value :obj:`[]`.

        constraints_linear_b (:obj:`list`, optional):
            The :math:`b` vector for specifying linear constraints.  :math:`b`
            should be formatted as a one-dimensional Python list.  Default value :obj:`[]`.

        constraints_sat_max_runs (:obj:`int`, optional):
            The maximum number of iterations the platform should run in
            order to find a formulation where all constraints are satisfied.  Default value :obj:`3100`.

        constraints_hard (:obj:`bool`, optional):
            Whether to strictly enforce all constraints; if :obj:`False`,
            constraint penalties may be low enough such that constraints are violated, with the benefit of an improved
            energy landscape.  Default value :obj:`False`.

        constraints_penalty_scaling_factor (:obj:`int`, optional):
            An extra constant scaling factor for the Lagrange
            multipliers associated with the penalty terms for the constraints.  This may be helpful if constraints are
            being violated too much or too often.  Default value 1.

        constraints_equality_R (:obj:`list`, optional):
            The :math:`R` matrices for specifying quadratic equality
            constraints.  :math:`R` should be formatted as a list of two-dimensional lists (i.e., a list of matrices).
            Default value :obj:`[]`.

        constraints_equality_c (:obj:`list`, optional):
            The :math:`c` vectors for specifying quadratic equality
            constraints.  :math:`c` should be formatted as a list of one-dimensional Python lists (i.e., a list of
            vectors).  Default value :obj:`[]`.

        constraints_inequality_S (:obj:`list`, optional):
            The :math:`S` matrices for specifying quadratic inequality
            constraints.  :math:`S` should be formatted as a list of two-dimensional lists (i.e., a list of matrices).
            Default value :obj:`[]`.

        constraints_inequality_d (:obj:`list`, optional):
            The :math:`d` vectors for specifying quadratic inequality
            constraints.  :math:`d` should be formatted as a list of one-dimensional Python lists (i.e., a list of
            vectors).  Default value :obj:`[]`.

        return_all_solutions (:obj:`bool`, optional):
            Whether to return all the candidate solutions found for a problem;
            if :obj:`False`, the platform will only return the solution corresponding to the lowest energy found.
            Default value :obj:`False`.

        num_runs (:obj:`int`, optional):
            The number of iterations to run with the selected solver.  Default value
            :obj:`50`.


        dwave_reduce_intersample_correlation (:obj:`bool`, optional):
            D-Wave hardware system parameter. See `reduce_intersample_correlation <https://docs.dwavesys.com/docs/latest/c_solver_1.html#reduce-intersample-correlation>`_.

        dwave_num_spin_reversal_transforms (:obj:`int`, optional):
            D-Wave hardware system parameter. See `num_spin_reversal_transforms <https://docs.dwavesys.com/docs/latest/c_solver_1.html#num-spin-reversal-transforms>`_.

        dwave_programming_thermalization (:obj:`int`, optional):
            D-Wave hardware system parameter. See `programming_thermalization <https://docs.dwavesys.com/docs/latest/c_solver_1.html#programming-thermalization>`_.

        dwave_reinitialize_state (:obj:`bool`, optional):
            D-Wave hardware system parameter. See `reinitialize_state <https://docs.dwavesys.com/docs/latest/c_solver_1.html#reinitialize-state>`_.

        dwave_anneal_offsets (:obj:`[float]`, optional):
            D-Wave hardware system parameter. See `anneal_offsets <https://docs.dwavesys.com/docs/latest/c_solver_1.html#anneal-offsets>`_.

        dwave_anneal_offsets_delta: (:obj:`float`, optional):
            Parameter greater or equal to 0 that is used to generate anneal offsets, cannot be specified if dwave_anneal_offsets is also specified. We recommend the value to be in [0, 0.05]. See `<https://arxiv.org/pdf/1806.11091.pdf>`_.

        dwave_num_reads (:obj:`int`, optional):
            D-Wave hardware system parameter. See `num_reads <https://docs.dwavesys.com/docs/latest/c_solver_1.html#num-reads>`_.

        dwave_max_answers (:obj:`int`, optional):
            D-Wave hardware system parameter. See `max_answers <https://docs.dwavesys.com/docs/latest/c_solver_1.html#max-answers>`_.

        dwave_flux_biases (:obj:`[float]`, optional):
            D-Wave hardware system parameter. See `flux_biases <https://docs.dwavesys.com/docs/latest/c_solver_1.html#flux-biases>`_.

        dwave_beta (:obj:`float`, optional):
            D-Wave hardware system parameter. See `beta <https://docs.dwavesys.com/docs/latest/c_solver_1.html#beta>`_.

        dwave_answer_mode (:obj:`string`, optional):
            D-Wave hardware system parameter. See `answer_mode <https://docs.dwavesys.com/docs/latest/c_solver_1.html#answer-mode>`_.

        dwave_auto_scale (:obj:`bool`, optional):
            D-Wave hardware system parameter. See `auto_scale <https://docs.dwavesys.com/docs/latest/c_solver_1.html#auto-scale>`_.

        dwave_postprocess (:obj:`string`, optional):
            D-Wave hardware system parameter. See `postprocess <https://docs.dwavesys.com/docs/latest/c_solver_1.html#postprocess>`_.

        dwave_annealing_time (:obj:`int`, optional):
            D-Wave hardware system parameter. See `annealing_time <https://docs.dwavesys.com/docs/latest/c_solver_1.html#annealing-time>`_.

        dwave_anneal_schedule (:obj:`[(int, float)]`, optional):
            D-Wave hardware system parameter. See `anneal_schedule <https://docs.dwavesys.com/docs/latest/c_solver_1.html#anneal-schedule>`_.

        dwave_initial_state (:obj:`[(int, int)]`, optional):
            D-Wave hardware system parameter. See `initial_state <https://docs.dwavesys.com/docs/latest/c_solver_1.html#initial-state>`_.

        dwave_chains (:obj:`[[int]]`, optional):
            D-Wave hardware system parameter. See `chains <https://docs.dwavesys.com/docs/latest/c_solver_1.html#chains>`_.

        dwave_flux_drift_compensation (:obj:`bool`, optional):
            D-Wave hardware system parameter. See `flux_drift_compensation <https://docs.dwavesys.com/docs/latest/c_solver_1.html#flux-drift-compensation>`_.

        dwave_beta_range (:obj:`[int]`, optional):
            D-Wave software system parameter. See `beta_range <https://docs.ocean.dwavesys.com/projects/dimod/en/latest/reference/generated/dimod.reference.samplers.SimulatedAnnealingSampler.sample.html>`_.

        dwave_num_sweeps (:obj:`int`, optional):
            D-Wave software system parameter. See `num_sweeps <https://docs.ocean.dwavesys.com/projects/dimod/en/latest/reference/generated/dimod.reference.samplers.SimulatedAnnealingSampler.sample.html>`_.

        dwave_precision_ancillas (:obj:`bool`, optional):

        dwave_precision_ancillas_tuples (:obj:`[[int]]`, optional):

        constraints_hard_num (:obj:`[[int]]`, optional):

        sa_num_sweeps (:obj:`int`, optional):
            If using a simulated annealing solver, how many sweeps to perform per
            run of the algorithm.  Default value :obj:`200`.

        use_sample_persistence (:obj:`bool`, optional):
            Whether to use the sample persistence method of
            https://arxiv.org/abs/1606.07797 , which aims to improve the probability of a quantum annealer to obtain
            an optimal solution.

        sample_persistence_solution_threshold (:obj:`float`, optional):
            A threshold that is used to filter out
            higher-energy candidate solutions from the sample persistence method.  A percentage that ranges from 0 to 1.

        sample_persistence_persistence_threshold (:obj:`float`, optional):
            A threshold between 0 and 1 such that a
            variable is fixed if its mean absolute value across the filtered sample is larger than the value of the
            threshold.  Called fixing_threshold in the original paper.

        sample_persistence_persistence_iterations (:obj:`int`, optional):
            The number of iterations to run the sample
            persistence algorithm.  Generally speaking, more iterations will make the algorithm more successful, at
            the cost of increased computation time.

        google_num_steps (:obj:`int`, optional):
            The number of QAOA steps implemented
            by the algorithm.  Default value :obj:`1`.

        google_n_samples (:obj:`int`, optional):
            The number of runs corresponding to
            the final sampling step.  Default value :obj:`1000`.

        google_arguments_optimizer (:obj:`dict`, optional):
            The dictionary that contains the parameters
            of the bayesain-optimization optimizer.  Default value :obj:`{'init_point': 10, 'number_iter': 20, 'kappa': 2}`.

        google_step_sampling (:obj:`bool`, optional):
            Wheter to sample the circuit with the current parameters
            at every step of the optimization (True) or just at the final one.  Default value :obj:`True`.

        google_n_samples_step_sampling (:obj:`int`, optional):
            The number of runs corresponding to
            sampling at every step of the optimization.  Default value :obj:`1000`.

        number_of_blocks (:obj:`int`, optional):
            number of blocks to decompose problem into using
            random decomposition. Default value :obj: `1` meaning no decomposition.

        iterations (:obj:`int`, optional):
            number of iterations to cycle through when using
            random decomposition. Only valid if :obj: `number_of_blocks` is greater than 1.
            Each iterations corresponds to solving all blocks of the decomposition once.
            Default value :obj:`50`.

        initial_solution (:obj:`dict`, optional):
            initial solution seed for constructing the
            blocks using random decomposition. If none is provided, a random solution is
            initialized. Default value :obj: `None`. :obj:`initial_solution` should be the same type
            as :obj:`Q`.

        always_update_with_best (:obj:`bool`, optional):
            solutions found using decomposition
            do not monotonically get better with each iterations. The best solution is always returned,
            but this flag determines whether or not to construct new decomposition using best solution.
            Default value :obj: `True`.

        update_q_each_block_solution (:obj:`bool`, optional):
            each blocks decomposed Q matrix
            can be constructed at the onset of block composition, or updated every time a block is
            solved. Default value :obj: `True`.

        convert_solution (:obj:`function`, optional):
            A function that takes in a solution and ouputs a converted solution. This keyword argument
            is meant for internal use, it should not generally be used.

        host (:obj:`str`, optional):
            The Forge QC Ware server to which the client library should connect.
              Defaults to https://api.forge.qcware.com .


    Returns:
        qcware.optimization.SolveBinaryResult: A dict, possibly containing the fields:
            * 'solution' (:obj:`dict`): A Python dictionary representing the solution vector.  If :obj:`return_all_solutions`
              is :obj:`True`, this is a list of dicts. However, if the input :obj:`Q` is a 2D numpy array, then each :obj`solution` will
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

    """

    converted_Q = matrix_to_qubo(Q) if not isinstance(Q, dict) else Q
    problem = converted_Q if type(converted_Q) == QUBO else PUBO(converted_Q)
    qubo, reverse_mapping = problem.to_qubo().Q, problem.reverse_mapping

    params = {
        "key": key,
        "Q": qubo,
        "higher_order": False,
        "solver": solver,
        "constraints_linear_A": constraints_linear_A,
        "constraints_linear_b": constraints_linear_b,
        "constraints_sat_max_runs": constraints_sat_max_runs,
        "constraints_hard": constraints_hard,
        "constraints_penalty_scaling_factor": constraints_penalty_scaling_factor,
        "constraints_equality_R": constraints_equality_R,
        "constraints_equality_c": constraints_equality_c,
        "constraints_inequality_S": constraints_inequality_S,
        "constraints_inequality_d": constraints_inequality_d,
        "return_all_solutions": return_all_solutions,
        "num_runs": num_runs,
        "sa_num_sweeps": sa_num_sweeps,
        "use_sample_persistence": use_sample_persistence,
        "sample_persistence_solution_threshold": sample_persistence_solution_threshold,
        "sample_persistence_persistence_threshold": sample_persistence_persistence_threshold,
        "sample_persistence_persistence_iterations": sample_persistence_persistence_iterations,
        "google_num_steps": google_num_steps,
        "google_n_samples": google_n_samples,
        "google_arguments_optimizer": google_arguments_optimizer,
        "google_step_sampling": google_step_sampling,
        "google_n_samples_step_sampling": google_n_samples_step_sampling,
        "number_of_blocks": number_of_blocks,
        "iterations": iterations,
        "always_update_with_best": always_update_with_best,
        "update_q_each_block_solution": update_q_each_block_solution,
    }

    if dwave_reduce_intersample_correlation is not None:
        params["dwave_reduce_intersample_correlation"] = dwave_reduce_intersample_correlation
    if dwave_num_spin_reversal_transforms is not None:
        params["dwave_num_spin_reversal_transforms"] = dwave_num_spin_reversal_transforms
    if dwave_programming_thermalization is not None:
        params["dwave_programming_thermalization"] = dwave_programming_thermalization
    if dwave_reinitialize_state is not None:
        params["dwave_reinitialize_state"] = dwave_reinitialize_state
    if dwave_anneal_offsets is not None:
        params["dwave_anneal_offsets"] = dwave_anneal_offsets
    if dwave_anneal_offsets_delta is not None:
        params["dwave_anneal_offsets_delta"] = dwave_anneal_offsets_delta
    if dwave_num_reads is not None:
        params["dwave_num_reads"] = dwave_num_reads
    if dwave_max_answers is not None:
        params["dwave_max_answers"] = dwave_max_answers
    if dwave_flux_biases is not None:
        params["dwave_flux_biases"] = dwave_flux_biases
    if dwave_beta is not None:
        params["dwave_beta"] = dwave_beta
    if dwave_answer_mode is not None:
        params["dwave_answer_mode"] = dwave_answer_mode
    if dwave_auto_scale is not None:
        params["dwave_auto_scale"] = dwave_auto_scale
    if dwave_postprocess is not None:
        params["dwave_postprocess"] = dwave_postprocess
    if dwave_annealing_time is not None:
        params["dwave_annealing_time"] = dwave_annealing_time
    if dwave_anneal_schedule is not None:
        params["dwave_anneal_schedule"] = dwave_anneal_schedule
    if dwave_initial_state is not None:
        params["dwave_initial_state"] = dwave_initial_state
    if dwave_chains is not None:
        params["dwave_chains"] = dwave_chains
    if dwave_flux_drift_compensation is not None:
        params["dwave_flux_drift_compensation"] = dwave_flux_drift_compensation
    if dwave_beta_range is not None:
        params["dwave_beta_range"] = dwave_beta_range
    if dwave_num_sweeps is not None:
        params["dwave_num_sweeps"] = dwave_num_sweeps
    if dwave_precision_ancillas is not None:
        params["dwave_precision_ancillas"] = dwave_precision_ancillas
    if dwave_precision_ancillas_tuples is not None:
        params["dwave_precision_ancillas_tuples"] = dwave_precision_ancillas_tuples
    if constraints_hard_num is not None:
        params["constraints_hard_num"] = constraints_hard_num
    if initial_solution is not None:
        if isinstance(Q, dict):
            if not isinstance(initial_solution, dict):
                raise ValueError("initial_solution should be a dict")
            params["initial_solution"] = {reverse_mapping[k]: v
                                          for k, v in initial_solution.items()}
        elif isinstance(Q, (list, np.ndarray)):
            if not isinstance(initial_solution, (list, np.ndarray)):
                raise ValueError("initial_solution should be a list or np.array")
            params["initial_solution"] = {reverse_mapping[k]: v
                                          for k, v in enumerate(initial_solution)}
        else:
            raise ValueError("Q formatted incorrectly")

    # warn user about their inputs
    _warnings(params)

    result = request.post(host + "/api/v2/solve_binary", params, "solve_binary")

    if convert_solution is None:
        def convert_solution(sol):
            if isinstance(Q, dict):
                return problem.convert_solution(sol)
            elif isinstance(Q, np.ndarray):
                return np.array([int(v) for v in result])
            elif isinstance(Q, list):
                return [int(v) for v in result]
            else:
                raise ValueError("Invalid Q type")

    _recursively_convert_solutions(result, convert_solution)
    return SolveBinaryResult(result)