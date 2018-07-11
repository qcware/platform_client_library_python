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


# VQE call

def find_ground_state_energy(key,
                             molecule,
                             basis='sto-3g',
                             solver="simulator",
                             multiplicity=1,
                             charge=0,
                             sampling=False,
                             sampling_trials=1000,
                             guess_amplitudes=[],
                             initial_state='UCCSD',
                             minimizer='CG',

                             host="https://platform.qcware.com",
                             ):

    params = {
        "key": key,
        "molecule": molecule,
        "basis": basis,
        "solver": solver,
        "multiplicity": multiplicity,
        "charge": charge,
        "sampling": sampling,
        "sampling_trials": sampling_trials,
        'guess_amplitudes': guess_amplitudes,
        'initial_state': initial_state,
        'minimizer': minimizer
        }

    return request.post(host + "/api/v2/find_ground_state_energy", params, 'VQE')
