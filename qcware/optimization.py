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
def solve_binary(Q, need_mat_to_dict=True, max_runs=3100, isakov_solver=0, brute_force_solver=0,
                 constrained_to_unconstrained=False,
                 soft_or_hard_constraints=0, max_rep=4, prefactor=1, A=None, B=None, list_quad_equal=None,
                 list_quad_lin_inequal=None, multiple=False, gauge=False, software_or_hardware=0, jintra_val=-1.5,
                 hardware_je_set=False, dwave_param=False, num_reads_sol=1000, num_reads=1000, num_reads_je=1000,
                 n_gauges=3, num_reads_gauge=500, pi_elite_fraction=0.1, embedding="", n_sweeps=200,
                 n_repititions=1000, name_solver="an_ss_ge_fi_vdeg", hobo=False, key=""):
    params = {
        "Q": (mat_to_dict(Q) if need_mat_to_dict else Q),
        "max_runs": max_runs,
        "isakov_solver": isakov_solver,
        "brute_force_solver": brute_force_solver,
        "constrained_to_unconstrained": constrained_to_unconstrained,
        "soft_or_hard_constraints": soft_or_hard_constraints,
        "max_rep": max_rep,
        "prefactor": prefactor,
        "A": A,
        "B": B,
        "list_quad_equal": list_quad_equal,
        "list_quad_lin_inequal": list_quad_lin_inequal,
        "multiple": multiple,
        "gauge": gauge,
        "software_or_hardware": software_or_hardware,
        "jintra_val": jintra_val,
        "hardware_je_set": hardware_je_set,
        "dwave_param": dwave_param,
        "num_reads_sol": num_reads_sol,
        "num_reads": num_reads,
        "num_reads_je": num_reads_je,
        "n_gauges": n_gauges,
        "num_reads_gauge": num_reads_gauge,
        "pi_elite_fraction": pi_elite_fraction,
        "embedding": embedding,
        "n_sweeps": n_sweeps,
        "n_repititions": n_repititions,
        "name_solver": name_solver,
        "hobo": hobo,
        "key": key
    }

    return request.post("https://platform.qcware.com/api/v2/solve_binary", params)


def solve_integer(c=None, A_eq=None, b_eq=None, A=None, b=None, l=None, u=None, prefactor=1, software_or_hardware=0,
                  constrained_to_unconstrained=0, soft_or_hard_constraints=0, max_rep=4, key=""):
    params = {
        "c": c,
        "A_eq": A_eq,
        "b_eq": b_eq,
        "A": A,
        "b": b,
        "l": l,
        "u": u,
        "prefactor": prefactor,
        "software_or_hardware": software_or_hardware,
        "constrained_to_unconstrained": constrained_to_unconstrained,
        "soft_or_hard_constraints": soft_or_hard_constraints,
        "max_rep": max_rep,
        "key": key
    }

    return request.post("https://platform.qcware.com/api/v2/solve_integer", params)
