#  AUTO-GENERATED FILE - MODIFY AT OWN RISK
#  Project: qcware
#  Copyright (c) 2019 QC Ware Corp - All Rights Reserved

import qcware.types.optimization as types

from typing import Optional

import warnings
from qcware.forge.api_calls import declare_api_call


@declare_api_call(
    name="optimization.brute_force_minimize",
    endpoint="optimization/brute_force_minimize",
)
def brute_force_minimize(
    objective: types.PolynomialObjective,
    constraints: Optional[types.Constraints] = None,
    backend: str = "qcware/cpu",
):
    r"""Minimize given objective polynomial subject to constraints.

    Arguments:

    :param objective: The integer-coefficient polynomial to be evaluated should be specified by a PolynomialObjective. See documentation for PolynomialObjective for more information. Note that variables are boolean in the sense that their values are 0 and 1.
    :type objective: types.PolynomialObjective

    :param constraints: Optional constraints are specified with an object of class Constraints. See its documentation for further information., defaults to None
    :type constraints: Optional[types.Constraints]

    :param backend: String specifying the backend.  Currently only [qcware/cpu] available, defaults to qcware/cpu
    :type backend: str


    :return: BruteOptimizeResult object specifying the minimum value of the objective function (that does not violate a constraint) as well as the variables that attain this value.
    :rtype: types.BruteOptimizeResult"""
    pass
