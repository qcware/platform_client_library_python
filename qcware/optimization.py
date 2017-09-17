from . import request


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
                 num_runs=1000,
                 dwave_chain_coupling=-1.5,
                 dwave_optimize_chain_coupling=False,
                 dwave_num_runs_chain_coupling=1000,
                 dwave_use_dwave_embedder=False,
                 dwave_use_gauges=False,
                 dwave_num_gauges=3,
                 dwave_num_runs_gauge_selection=500,
                 dwave_chain_coupling_pi_fraction=0.1,
                 dwave_embedding="",
                 sa_num_sweeps=200,
                 use_sample_persistence=False,
                 sample_persistence_solution_threshold = 0.5,
                 sample_persistence_persistence_threshold = 0.5,
                 sample_persistence_persistence_iterations = 0
                 ):
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
        "dwave_chain_coupling": dwave_chain_coupling,
        "dwave_optimize_chain_coupling": dwave_optimize_chain_coupling,
        "dwave_num_runs_chain_coupling": dwave_num_runs_chain_coupling,
        "dwave_use_dwave_embedder": dwave_use_dwave_embedder,
        "dwave_use_gauges": dwave_use_gauges,
        "dwave_num_gauges": dwave_num_gauges,
        "dwave_num_runs_gauge_selection": dwave_num_runs_gauge_selection,
        "dwave_chain_coupling_pi_fraction": dwave_chain_coupling_pi_fraction,
        "dwave_embedding": dwave_embedding,
        "sa_num_sweeps": sa_num_sweeps,
        "use_sample_persistence": use_sample_persistence,
        "sample_persistence_solution_threshold": sample_persistence_solution_threshold,
        "sample_persistence_persistence_threshold": sample_persistence_persistence_threshold,
        "sample_persistence_persistence_iterations": sample_persistence_persistence_iterations
    }

    return request.post("https://platform.qcware.com/api/v2/solve_binary", params)
