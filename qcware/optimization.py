from . import request
from qcware.wrappers import print_errors, print_api_mismatch


def mat_to_dict(mat):
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


# Note: this is good for both HOBOs and QUBOs
@print_api_mismatch
@print_errors
def solve_binary(key,
                 Q,
                 higher_order=False,
                 solver="dwave_software",
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
                 host="https://platform.qcware.com",
                 ):
    """Solve a variety of optimization problems, in particular Quadratic
    Unconstrained Binary Optimization (QUBO) or Higher Order Binary
    Optimization (HOBO) problems.

    In its most basic form, given an objective matrix Q, solves the
    problem of finding the vector x which minimizes the equation
    xT*Q*x.  Linear equality constraints can be added and a variety of
    solvers used.

    Returns a dictionary containing several entries; the entry
    `solution` contains the chosen solution, but other information can
    be provided as well. If an error occurred, it will be
    under the entry `error`.

    """
    params = {
        "key": key,
        "Q": mat_to_dict(Q) if not isinstance(Q, dict) else Q,
        "higher_order": higher_order,
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

    return request.post(host + "/api/v2/solve_binary", params, "solve_binary")
