from . import request
from qcware.wrappers import print_errors, print_api_mismatch
import numpy as np
import warnings


class SolveBinaryWarning(UserWarning):
    r"""Warning type for warnings from `qcware.optimization.solve_binary`.

    Initiate warning with `SolveBinaryWarning.warn("message")`.
    """
    @classmethod
    def warn(cls, message):
        r"""Warn with cls at a default level.

        Args:
            message (:obj:`str`): message to show with the warning.
        """
        warnings.warn(message, cls, 2)


class SolverWarning(SolveBinaryWarning):
    r"""Warning type for solver related warnings in `qcware.optimization.solve_binary`.

    Initiate warning with `SolverWarning.warn("message")`.
    """


def _warnings(params):
    r"""Warn user about their inputs.

    Args:
        params (:obj:`dict`): the input parameters to `solve_binary`.

    Returns:
        None
    """

    # Warn about long computation times
    if params["solver"] == "ibm_hw_qaoa":
        SolverWarning.warn("Running QAOA on IBM hardware will be a very long "
                           "computation! Be prepared to wait hours for an output.")

    # Warn about parameters not being used
    if "dwave_anneal_offsets" in params and "dwave_anneal_offsets_delta" in params:
        SolveBinaryWarning.warn("`dwave_anneal_offsets` and `dwave_anneal_offsets_delta` "
                                "are not both used in the same call.")

    # TODO: more warnings. ie any inconsistencies that the user provides, etc.


def mat_to_dict(mat):
    r"""Convert a numpy array representing :math:`Q` to a dictionary of the appropriate format.

    This function takes a numpy matrix representation of a :math:`Q` matrix and converts it to a spare representation
    using the built-in Python dictionary datatype.  Matrix indices are encoded as keys (paris of ints).  Matrix entries
    are encoded as values in the dictionary.  :math:`Q` is assumed to be symmetric.

    Args:
        mat (:obj:`numpy.array`): A 2D numpy array (like a matrix) representing the :math:`Q` matrix associated with the
            objective function of the optimization problem being solved.

    Returns:
        :obj:`dict`: A dictionary representation of :math:`Q` that can be sent to the platform.
    """
    if isinstance(mat, list):
        mat = np.array(mat)

    the_dict = {}
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            the_dict[(i, j)] = mat[i, j]
    Q_new = {}
    for it in the_dict.keys():
        val_loop = the_dict[it]
        if (it[1], it[0]) in the_dict.keys() and it[1] != it[0] and it[1] > it[0]:
            val_loop += the_dict[(it[1], it[0])]
            Q_new[it] = val_loop
        elif it[1] == it[0]:
            Q_new[it] = the_dict[it]
    return Q_new


def enumerate_Q(Q):
    r"""Replace the keys of Q with an enumeration of the input variables.

    Args:
        Q (:obj:`dict`): A dictionary representation of :math:`Q` where the keys are tuples of ints or strings

    Returns:
        :obj:`dict`: A dictionary representation of :math:`Q` where the keys are ints
        :obj:`dict`: A dictionary mapping those ints to the original key values
        :obj:`dict`: A dictionary mapping those the original key values to those ints
    """
    enumerated_Q = {}
    enumeration_mapping = {}
    reverse_mapping = {}
    enumeration = 0
    for k, v in Q.items():
        enumerated_key = []
        for var in k:
            if var not in enumeration_mapping:
                enumeration_mapping[var] = enumeration
                reverse_mapping[enumeration] = var
                enumeration += 1
            enumerated_key.append(enumeration_mapping[var])
        enumerated_Q[tuple(enumerated_key)] = v
    return enumerated_Q, reverse_mapping, enumeration_mapping


_solution_keys = {"solution", "all_solutions", "unique_solutions", "most_common_measurement"}


def _recursively_convert_solutions(result, mapping, Q):
    r"""Convert solutions with their enumeration.

    The output of the request to `solve_binary` is a dictionary with various
    keys. `mapping` is a `dict` that maps indicies of the solutions lists to
    the keys that the user originally used in their QUBO `dict`. This
    function recursively goes through the result and converts all solution
    lists to a dictionary that maps the user's original keys to the correct
    values. Note that the `result` dictionary is modified in place!

    Args:
        result (:obj:`dict`): The output of `qcware.optimization.solve_binary`.
        mapping (:obj:`dict`): Dictionary that maps integer indices used in the QUBO to the user's original inputs.
        Q (:obj:`dict`,:obj:`list`,or :obj:`np.array`): QUBO dictionary.

    Returns:
        None. The `result` dictionary is modified in place.
    """
    # through recursive calls
    if isinstance(result, list):
        try:
            if isinstance(Q, dict):
                return {mapping[i]: int(v) for i, v in enumerate(result)}
            elif isinstance(Q, np.ndarray):
                return np.array([int(v) for v in result])
            elif isinstance(Q, list):
                return [int(v) for v in result]
            else:
                raise ValueError("Invalid Q type")
        except (KeyError, TypeError):
            return [_recursively_convert_solutions(x, mapping, Q) for x in result]

    elif isinstance(result, dict):
        for k, v in tuple(result.items()):
            if isinstance(v, dict):
                _recursively_convert_solutions(v, mapping, Q)
            elif k in _solution_keys:
                result[k] = _recursively_convert_solutions(v, mapping, Q)


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
        host="https://forge.qcware.com",
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
        key (:obj:`str`): An API key for the platform.  Keys can be allocated and managed from the Forge web portal.

        Q (:obj:`dict`): The objective function matrix in the optimization problem described above.  In the case of a
            quadratic problem, this is a 2D matrix; generally, in the case of higher-order problems, this is an
            :math:`n`-dimensional matrix (a tensor).

            Since :math:`Q` is usually sparse, :math:`Q` should be specified
            as a Python dictionary with integer or string pairs :math:`(i,j)` as keys (representing the :math:`(i,j)`th
            entry of :math:`Q`) and integer or float values.  In the case of a cubic function, for example, some
            dictionary keys will be 3-tuples of integers, rather than pairs.

            Alternatively, :math:`Q` may be specified as a numpy array or list, in which case :obj:`mat_to_dict` is called on
            :math:`Q` before sending it to the platform.  Note that that helper function assumes :math:`Q` is symmetric,
            which may not be true in general. It is strongly encouraged to format :math:`Q` is a dictionary.

        solver (:obj:`str`, optional): The name of the solver to use for the given problem.  Valid values are:

            * "dwave_hw": Run on a physical D-Wave machine
            * "brute_force": Run using a brute force algorithm
            * "hfs": Run using the Hamze-de Freitas-Selby algorithm
            * "google_sw_qaoa": Run using the Google simulator implementation of the QAOA algorithm
            * "ibm_hw_qaoa": Run the QAOA algorithm on a physical IBM machine, this may take over 2 hours for even small problems!
            * "ibm_sw_qaoa": Run the QAOA algorithm on IBM's software simulator of the QAOA algorithm


            Note that only certain solvers may be enabled depending on your account.  Default value "dwave_hw".

        constraints_linear_A (:obj:`list`, optional): The :math:`A` matrix for specifying linear constraints.  :math:`A`
            should be formatted as a two-dimensional Python list.  Default value :obj:`[]`.

        constraints_linear_b (:obj:`list`, optional): The :math:`b` vector for specifying linear constraints.  :math:`b`
            should be formatted as a one-dimensional Python list.  Default value :obj:`[]`.

        constraints_sat_max_runs (:obj:`int`, optional): The maximum number of iterations the platform should run in
            order to find a formulation where all constraints are satisfied.  Default value :obj:`3100`.

        constraints_hard (:obj:`bool`, optional): Whether to strictly enforce all constraints; if :obj:`False`,
            constraint penalties may be low enough such that constraints are violated, with the benefit of an improved
            energy landscape.  Default value :obj:`False`.

        constraints_penalty_scaling_factor (:obj:`int`, optional): An extra constant scaling factor for the Lagrange
            multipliers associated with the penalty terms for the constraints.  This may be helpful if constraints are
            being violated too much or too often.  Default value 1.

        constraints_equality_R (:obj:`list`, optional): The :math:`R` matrices for specifying quadratic equality
            constraints.  :math:`R` should be formatted as a list of two-dimensional lists (i.e., a list of matrices).
            Default value :obj:`[]`.

        constraints_equality_c (:obj:`list`, optional): The :math:`c` vectors for specifying quadratic equality
            constraints.  :math:`c` should be formatted as a list of one-dimensional Python lists (i.e., a list of
            vectors).  Default value :obj:`[]`.

        constraints_inequality_S (:obj:`list`, optional): The :math:`S` matrices for specifying quadratic inequality
            constraints.  :math:`S` should be formatted as a list of two-dimensional lists (i.e., a list of matrices).
            Default value :obj:`[]`.

        constraints_inequality_d (:obj:`list`, optional): The :math:`d` vectors for specifying quadratic inequality
            constraints.  :math:`d` should be formatted as a list of one-dimensional Python lists (i.e., a list of
            vectors).  Default value :obj:`[]`.

        return_all_solutions (:obj:`bool`, optional): Whether to return all the candidate solutions found for a problem;
            if :obj:`False`, the platform will only return the solution corresponding to the lowest energy found.
            Default value :obj:`False`.

        num_runs (:obj:`int`, optional): The number of iterations to run with the selected solver.  Default value
            :obj:`50`.

        dwave_algorithm (:obj:`int`, optional): D-Wave software system parameter. See `algorithm <https://docs.ocean.dwavesys.com/projects/qbsolv/en/latest/source/generated/dwave_qbsolv.QBSolv.sample.html#dwave_qbsolv.QBSolv.sample>`_.

        dwave_solver_limit (:obj:`int`, optional): D-Wave software system parameter. See `solver_limit <https://docs.ocean.dwavesys.com/projects/qbsolv/en/latest/source/generated/dwave_qbsolv.QBSolv.sample.html#dwave_qbsolv.QBSolv.sample>`_.

        dwave_target_energy (:obj:`float`, optional): D-Wave software system parameter. See `target_energy <https://docs.ocean.dwavesys.com/projects/qbsolv/en/latest/source/generated/dwave_qbsolv.QBSolv.sample.html#dwave_qbsolv.QBSolv.sample>`_.

        dwave_find_max (:obj:`bool`, optional): D-Wave software system parameter. See `D-Wave find_max <https://docs.ocean.dwavesys.com/projects/qbsolv/en/latest/source/generated/dwave_qbsolv.QBSolv.sample.html#dwave_qbsolv.QBSolv.sample>`_.

        dwave_reduce_intersample_correlation (:obj:`bool`, optional): D-Wave hardware system parameter. See `reduce_intersample_correlation <https://docs.dwavesys.com/docs/latest/c_solver_1.html#reduce-intersample-correlation>`_.

        dwave_num_spin_reversal_transforms (:obj:`int`, optional): D-Wave hardware system parameter. See `num_spin_reversal_transforms <https://docs.dwavesys.com/docs/latest/c_solver_1.html#num-spin-reversal-transforms>`_.

        dwave_programming_thermalization (:obj:`int`, optional): D-Wave hardware system parameter. See `programming_thermalization <https://docs.dwavesys.com/docs/latest/c_solver_1.html#programming-thermalization>`_.

        dwave_reinitialize_state (:obj:`bool`, optional): D-Wave hardware system parameter. See `reinitialize_state <https://docs.dwavesys.com/docs/latest/c_solver_1.html#reinitialize-state>`_.

        dwave_anneal_offsets (:obj:`[float]`, optional): D-Wave hardware system parameter. See `anneal_offsets <https://docs.dwavesys.com/docs/latest/c_solver_1.html#anneal-offsets>`_.

        dwave_anneal_offsets_delta: (:obj:`float`, optional): Parameter greater or equal to 0 that is used to generate anneal offsets, cannot be specified if dwave_anneal_offsets is also specified. We recommend the value to be in [0, 0.05]. See `<https://arxiv.org/pdf/1806.11091.pdf>`_.

        dwave_num_reads (:obj:`int`, optional): D-Wave hardware system parameter. See `num_reads <https://docs.dwavesys.com/docs/latest/c_solver_1.html#num-reads>`_.

        dwave_max_answers (:obj:`int`, optional): D-Wave hardware system parameter. See `max_answers <https://docs.dwavesys.com/docs/latest/c_solver_1.html#max-answers>`_.

        dwave_flux_biases (:obj:`[float]`, optional): D-Wave hardware system parameter. See `flux_biases <https://docs.dwavesys.com/docs/latest/c_solver_1.html#flux-biases>`_.

        dwave_beta (:obj:`float`, optional): D-Wave hardware system parameter. See `beta <https://docs.dwavesys.com/docs/latest/c_solver_1.html#beta>`_.

        dwave_answer_mode (:obj:`string`, optional): D-Wave hardware system parameter. See `answer_mode <https://docs.dwavesys.com/docs/latest/c_solver_1.html#answer-mode>`_.

        dwave_auto_scale (:obj:`bool`, optional): D-Wave hardware system parameter. See `auto_scale <https://docs.dwavesys.com/docs/latest/c_solver_1.html#auto-scale>`_.

        dwave_postprocess (:obj:`string`, optional): D-Wave hardware system parameter. See `postprocess <https://docs.dwavesys.com/docs/latest/c_solver_1.html#postprocess>`_.

        dwave_annealing_time (:obj:`int`, optional): D-Wave hardware system parameter. See `annealing_time <https://docs.dwavesys.com/docs/latest/c_solver_1.html#annealing-time>`_.

        dwave_anneal_schedule (:obj:`[(int, float)]`, optional): D-Wave hardware system parameter. See `anneal_schedule <https://docs.dwavesys.com/docs/latest/c_solver_1.html#anneal-schedule>`_.

        dwave_initial_state (:obj:`[(int, int)]`, optional): D-Wave hardware system parameter. See `initial_state <https://docs.dwavesys.com/docs/latest/c_solver_1.html#initial-state>`_.

        dwave_chains (:obj:`[[int]]`, optional): D-Wave hardware system parameter. See `chains <https://docs.dwavesys.com/docs/latest/c_solver_1.html#chains>`_.

        dwave_flux_drift_compensation (:obj:`bool`, optional): D-Wave hardware system parameter. See `flux_drift_compensation <https://docs.dwavesys.com/docs/latest/c_solver_1.html#flux-drift-compensation>`_.

        dwave_beta_range (:obj:`[int]`, optional): D-Wave software system parameter. See `beta_range <https://docs.ocean.dwavesys.com/projects/dimod/en/latest/reference/generated/dimod.reference.samplers.SimulatedAnnealingSampler.sample.html>`_.

        dwave_num_sweeps (:obj:`int`, optional): D-Wave software system parameter. See `num_sweeps <https://docs.ocean.dwavesys.com/projects/dimod/en/latest/reference/generated/dimod.reference.samplers.SimulatedAnnealingSampler.sample.html>`_.

        dwave_precision_ancillas (:obj:`bool`, optional):

        dwave_precision_ancillas_tuples (:obj:`[[int]]`, optional):

        constraints_hard_num (:obj:`[[int]]`, optional):

        sa_num_sweeps (:obj:`int`, optional): If using a simulated annealing solver, how many sweeps to perform per
            run of the algorithm.  Default value :obj:`200`.

        use_sample_persistence (:obj:`bool`, optional): Whether to use the sample persistence method of
            https://arxiv.org/abs/1606.07797 , which aims to improve the probability of a quantum annealer to obtain
            an optimal solution.

        sample_persistence_solution_threshold (:obj:`float`, optional): A threshold that is used to filter out
            higher-energy candidate solutions from the sample persistence method.  A percentage that ranges from 0 to 1.

        sample_persistence_persistence_threshold (:obj:`float`, optional): A threshold between 0 and 1 such that a
            variable is fixed if its mean absolute value across the filtered sample is larger than the value of the
            threshold.  Called fixing_threshold in the original paper.

        sample_persistence_persistence_iterations (:obj:`int`, optional): The number of iterations to run the sample
            persistence algorithm.  Generally speaking, more iterations will make the algorithm more successful, at
            the cost of increased computation time.

        google_num_steps (:obj:`int`, optional): The number of QAOA steps implemented
            by the algorithm.  Default value :obj:`1`.

        google_n_samples (:obj:`int`, optional): The number of runs corresponding to
            the final sampling step.  Default value :obj:`1000`.

        google_arguments_optimizer (:obj:`dict`, optional): The dictionary that contains the parameters
            of the bayesain-optimization optimizer.  Default value :obj:`{'init_point': 10, 'number_iter': 20, 'kappa': 2}`.

        google_step_sampling (:obj:`bool`, optional): Wheter to sample the circuit with the current parameters
            at every step of the optimization (True) or just at the final one.  Default value :obj:`True`.

        google_n_samples_step_sampling (:obj:`int`, optional): The number of runs corresponding to
            sampling at every step of the optimization.  Default value :obj:`1000`.

        number_of_blocks (:obj:`int`, optional): number of blocks to decompose problem into using
            random decomposition. Default value :obj: `1` meaning no decomposition.

        iterations (:obj:`int`, optional): number of iterations to cycle through when using
            random decomposition. Only valid if :obj: `number_of_blocks` is greater than 1.
            Each iterations corresponds to solving all blocks of the decomposition once.
            Default value :obj:`50`.

        initial_solution (:obj:`dict`, optional): initial solution seed for constructing the
            blocks using random decomposition. If none is provided, a random solution is
            initialized. Default value :obj: `None`. `initial_solution` should be the same type
            as `Q`.

        always_update_with_best (:obj:`bool`, optional):  solutions found using decomposition
            do not monotonically get better with each iterations. The best solution is always returned,
            but this flag determines whether or not to construct new decomposition using best solution.
            Default value :obj: `True`.

        update_q_each_block_solution (:obj:`bool`, optional): each blocks decomposed Q matrix
            can be constructed at the onset of block composition, or updated every time a block is
            solved. Default value :obj: `True`.

        host (:obj:`str`, optional): The AQUA server to which the client library should connect.  Defaults to https://platform.qcware.com .


    Returns:
        JSON object: A JSON object, possibly containing the fields:
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

    converted_Q = mat_to_dict(Q) if not isinstance(Q, dict) else Q
    enumerated_Q, mapping, reverse_mapping = enumerate_Q(converted_Q)

    params = {
        "key": key,
        "Q": enumerated_Q,
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

    if dwave_algorithm is not None:
        params["dwave_algorithm"] = dwave_algorithm
    if dwave_solver_limit is not None:
        params["dwave_solver_limit"] = dwave_solver_limit
    if dwave_target_energy is not None:
        params["dwave_target_energy"] = dwave_target_energy
    if dwave_find_max is not None:
        params["dwave_find_max"] = dwave_find_max
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

    _recursively_convert_solutions(result, mapping, Q)
    result['enumeration'] = mapping

    return result


# Utilities

def qubo_to_ising(Q, offset=0):
    r"""Convert the specified QUBO problem into an Ising problem.
    Note that QUBO {0, 1} values go to Ising {-1, 1} values in that order!

    Args:
        Q (:obj:`dict`): QUBO dictionary.
            Maps tuples of binary variables indices to the Q value.
            ie `Q[(i, j)]` is the `(i, j)` QUBO value.
        offset (:obj:`float`, optional): defaults to 0.
            The part of the objective function that does not depend on the
            variables.

    Returns:
        result (:object:`tuple`): (h, J, offset).
            h (:obj:`dict`): Field values.
                The field of each spin in the Ising formulation.
                `h[i]` is the field value for the ith spin.
            J (:obj:`dict`): Coupling values.
                `J[(i, j)]` is the coupling between the ith and jth spin.
            offset : float.
                It is the sum of the terms in the formulation that don't involve any variables.
    """
    h, J = {}, {}

    for (i, j), v in Q.items():
        if i != j:

            val = J.get((i, j), 0) + v / 4.
            if val:
                J[(i, j)] = val
            else:
                J.pop((i, j), 0)

            for a in (i, j):
                val = h.get(a, 0) + v / 4.
                if val:
                    h[a] = val
                else:
                    h.pop(a, 0)

            offset += v / 4.

        else:

            val = h.get(i, 0) + v / 2.
            if val:
                h[i] = val
            else:
                h.pop(i, 0)

            offset += v / 2.

    return h, J, offset


def ising_to_qubo(h, J, offset=0):
    """Convert the specified Ising problem into a QUBO problem.
    Note that Ising {-1, 1} values go to QUBO {0, 1} values in that order!

    Args:
        h (:obj:`dict`): Field values.
            The field of each spin in the Ising formulation.
            `h[i]` is the field value for the ith spin.
        J (:obj:`dict`): Coupling values.
            `J[(i, j)]` is the coupling between the ith and jth spin. Note
            that `J` cannot have a key that has a repeated index, ie `(1, 1)` is an
            invalid key.
        offset (:obj:`float`, optional): Defaults to 0.
            It is the sum of the terms in the formulation that don't involve any variables.

    Return:
        result (:obj:`tuple`): (Q, offset).
        Q (:obj:`dict`): QUBO dictionary.
            Maps tuples of binary variables indices to the Q value.
            ie `Q[(i, j)]` is the `(i, j)` QUBO value.
        offset (:obj:`float`): Numeric.
            The part of the objective function that does not depend on the
            variables.
    """
    Q = {}

    for (i, j), v in J.items():
        if i == j:
            raise KeyError("J formatted incorrectly, key cannot "
                           "have repeated indices")
        val = Q.get((i, j), 0) + 4. * v
        if val:
            Q[(i, j)] = val
        else:
            Q.pop((i, j), 0)

        for a in (i, j):
            val = Q.get((a, a), 0) - 2. * v
            if val:
                Q[(a, a)] = val
            else:
                Q.pop((a, a), 0)

        offset += v

    for i, v in h.items():
        val = Q.get((i, i), 0) + 2. * v
        if val:
            Q[(i, i)] = val
        else:
            Q.pop((i, i), 0)

        offset -= v

    return Q, offset


def qubo_value(x, Q, offset=0):
    r"""Find the value of the QUBO objective function for a given bit string.

    Args:
        x (:obj:`dict` or :obj:`iterable`): Bit string.
            Maps binary variable indices to their binary values, 0 or 1. Ie
            `x[i]` must be the binary value of variable i.
        Q (:obj:`dict`): QUBO dictionary.
            Maps tuples of binary variables indices to the Q value.
        offset (:obj:`float`, optional): Defaults to 0.
            The part of the objective function that does not depend on the
            variables.

    Return:
        value (:obj:`float`): The value of the QUBO with the given assignment `x`.
    """
    return sum(v * x[i] * x[j] for (i, j), v in Q.items()) + offset


def ising_value(z, h, J, offset=0):
    r"""Find the value of the Ising objective function for a given spin configuration.

    Args:
        z (:obj:`dict` or :obj:`iterable`): spin configuration.
            Maps variable labels to their values, -1 or 1. Ie `z[i]` must be the
            value of variable i.
        J (:obj:`dict`): Coupling dictionary.
            Maps pairs of variables labels to the J value.
        h (:obj:`dict`): Field dictionary.
            Maps variable names to their field value.
        offset (:obj:`float`, optional): Defaults to 0.
            The part of the objective function that does not depend on the
            variables.

    Return:
        value (:obj:`float`): The value of the Ising with the given assignment `z`.
    """
    return sum(
        v * z[i] * z[j] for (i, j), v in J.items()
    ) + sum(
        v * z[i] for i, v in h.items()
    ) + offset
