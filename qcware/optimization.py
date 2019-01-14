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
def solve_binary(
    key,
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
    num_runs=1000,
    dwave_algorithm=None,
    dwave_solver_limit=None,
    dwave_target_energy=None,
    dwave_find_max=False,
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
    be obtained from keys such as `num_qubits`, `num_runs`,
    `num_logical_variables`, etc.  If an error occurred, it will be
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
        "dwave_find_max": dwave_find_max,
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

    return request.post(host + "/api/v2/solve_binary", params, "solve_binary")


async def async_solve_binary(
    client,
    key,
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
    num_runs=1000,
    dwave_algorithm=None,
    dwave_solver_limit=None,
    dwave_target_energy=None,
    dwave_find_max=False,
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
    be obtained from keys such as `num_qubits`, `num_runs`,
    `num_logical_variables`, etc.  If an error occurred, it will be
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
        "dwave_find_max": dwave_find_max,
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

    return await request.async_post(client, host + "/api/v2/solve_binary", params, "solve_binary")
