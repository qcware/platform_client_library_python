from . import request
from .request import post_json


def solve_mcvqe(key,
                host,
                filenames=None,
                N=2,
                connectivity='linear',
                backend_name='quasar',
                nmeasurement=None,
                nmeasurement_subspace=None,
                nstate=3,
                vqe_circuit_type='mark1x'):

    endpoint_url = "/".join([host, "api/v2/mcvqe"])

    return post_json(endpoint_url, dict(key=key, filenames=filenames, N=N, connectivity=connectivity,
                     backend_name=backend_name, nmeasurement=nmeasurement,
                     nmeasurement_subspace=nmeasurement_subspace, nstate=nstate,
                     vqe_circuit_type=vqe_circuit_type))

# VQE call


def find_ground_state_energy(key,
                             molecule,
                             minimizer=None,
                             basis='sto-3g',
                             solver='projectq',
                             multiplicity=1,
                             charge=0,
                             sampling=False,
                             sampling_trials=1000,
                             guess_amplitudes=[],
                             initial_state='UCCSD',

                             host="https://forge.qcware.com",
                             ):
    """
    Finds the ground state energy configuration for
    input molecular geometry configuration. Energy output is
    measured in Hartrees and atomic spacing input is assumed
    to be in Angstroms.

    This function uses the Variational Quantum Eigensolver and variants
    thereof to obtain an estimate for the ground state energy of a molecule
    in a given configuration. This is achieved by obtaining the molecular
    hamiltonian in second quantized form using standard chemistry packages
    (PSI4 and PySCF) using Hartree-Fock theory. The second quantized molecular
    hamiltonian is converted into a Qubit Hamiltonian using the jordan-wigner
    transformation (in the future, the transformation technique will also
    be a parameter specified by the user).

    The algorithm then uses a parametrized ansatz, currently restricted to
    Unitary Coupled Cluster with Singles and Double excitations (UCCSD), to
    prepare a state on the quantum register and estimates the expectation value
    of the hamiltonian. The result is fed into a classical optimizer which
    determines an update rule for the parametrized ansatz. The returned value
    corresponds to the energy and parameters that minimize the energy.

    Args:
        key (:obj:`string`) : An API key for the platform.  Keys can be allocated
            and managed from the Forge web portal.

        molecule (:obj:`list`): List of tuples/lists the form
            [[Element,Position], [Element,Position]]
            where Element is the periodic table symbol for atom
            and Position is a list [x,y,z] with cartesian coordinates
            representing the given atom's position in the molecular geometry input
            assuming Bohr-Oppenheimer approximation that the nuclei are at fixed
            coordinates. Distances are assumed to be in angstroms.

        minimizer (:obj:`string`): classical optimizer used to minimize
            parameters in ansatz used for the state preparation. If solver is set to
            'projectq' minimizer default is 'swarm' representing swarming algorithm
            and if solver is set to 'ibm_software' or 'ibm_hardware' default value
            is set to 'cobyla'. More minimizers will be available in the future.

            * For 'projectq' valid minimizers are:
                * 'CG' for conjugate gradient
                * 'swarm' for pyswarm implementation of swarming algorithm
            * For 'ibm_x' valid minimizers are:
                * 'cobyla' Constrained optimization by linear approximation
                * 'spsa' simultaneous perturbation stochastic approximation

        basis (:obj:`string`, optional): Orbital basis set used in classical
            computation of molecular hamiltonian. Accepted values are
            the ones natively used in psi4 chemistry package. Default value
            set to :obj:`sto-3g`

        solver (:obj:`string`, optional): The name of the solver to use for
            the given problem.  Valid values are:

            * "projectq": Run on a physical D-Wave machine
            * "ibm_software": Run on D-Wave's software simulator
            * "ibm_hardware": Run using a brute force algorithm

        multiplicity (:obj:`int`, optional): integer setting the spin
            multiplicity (:math:`2 M_s+1`). Default set to 1

        charge (:obj:`int`, optional): integer setting the molecular charge.
            Default set to 0.

        sampling (:obj:`bool`, optional): boolean determining whether
            expectation value of energy will be estimated for sampling from the
            prepared state or from directly computing an inner product with the
            wavefunction. Applicable only to the `projectq` solver.

        sampling_trials (:obj:`int`, optional): if 'sampling' is set to
            :obj:`True`, then this parameter sets the number of samples
            taken to estimate expectation value of each term in the molecular
            hamiltonian. Applicable only to the `projectq` solver.

        guess_amplitudes (:obj:`list`, optional): optional list for
            seeding initialization parameters for the 'UCCSD' parametrized state.
            Only available for 'CG' in 'projectq'

        initial_state (:obj: `string`, optional): Sets the type of parametrized
            parametrized ansatz used to optimize ground state energy. Default value
            set to 'UCCSD'. Currently only available option, to be expanded in
            the future.

        host (:obj:`string`, optional): The AQUA server to which the client
            library should connect.  Defaults to https://platform.qcware.com .

    Returns:
         JSON object: A JSON object, possibly containing the fields:
            * 'solution' (:obj:`list`): A Python list representing the solution
              found for the ground state energy of input molecule.
            * 'params' (:obj:`list`): the optimized parameters for the
              parametrized ansatz which minimizes the expectation value
              of the hamiltonian.

    """

    if minimizer is None:
        if solver == 'projectq':
            minimizer = 'CG'
        else:
            minimizer = 'cobyla'

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

    return request.post(host + "/api/v2/find_ground_state_energy",
                        params, 'VQE')
