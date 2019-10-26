"""warn.py.

This file contains warning functionality to standardize qcware's warnings.

"""


import warnings


__all__ = 'QCWareWarning', 'SolveBinaryWarning', 'SolverWarning'


class QCWareWarning(UserWarning):
    """QCWareWarning.

    Warning type to standardize qcware's warnings. Warn with
    ``QCWareWarning.warn("message")``.

    """

    @classmethod
    def warn(cls, message):
        r"""warn.

        Parameters
        ----------
        message : str.
            Message to warn with.

        """
        warnings.warn(message, cls, 3)


class SolveBinaryWarning(QCWareWarning):
    r"""Warning type for warnings from :obj:`qcware.optimization.solve_binary`.

    Initiate warning with :obj:`SolveBinaryWarning.warn("message")`.
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

    Initiate warning with :obj:`SolverWarning.warn("message")`.
    """
