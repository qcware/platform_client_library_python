"""_problem_parentclass.py.

This file contains the class Problem, which is the parent class to all
the problem classes.

"""

from qcware.optimization.utils import Conversions
import qcware


__all__ = 'Problem',


class Problem(Conversions):
    """Problem.

    This acts a parent class to all the QUBO and Ising conversion problem
    classes. The ``__new__`` method keeps track of the problem args. The
    ``repr`` method uses those input args, such that
    ``eval(repr(cls)) == cls``. Finally, we define a ``__eq__`` method to
    determine if two problems are the same. The rest of the methods are to be
    implemented in child classes.

    Subclasses `must` define at least one of the following methods:
        ``to_qubo``, ``to_ising``.
    If at least one of them is defined, then they will both work. The same is
    true for ``to_pubo`` and ``to_hising``.
    ``Problem`` inherits from ``Conversions``, for more details see
    ``help(qcware.optimization.utils.Conversions)``
    """

    def __new__(cls, *args, **kwargs):
        """__new__.

        Creates the object and keeps track of the input arguments and keyword
        arguments. Child classes should not change this. This method will be
        called before every __init__ is called. We use __new__ to keep track
        of input arguments instead of using __init__ so that child class
        implementations don't have to worry about it. Ie child classes
        don't have to call `super().__init__(*args, **kwargs)` in their
        __init__ method.

        Parameters
        ---------
        arguments : Defined in child classes.

        Return
        -------
        obj : instance of the child class.

        """
        obj = super().__new__(cls)
        obj._problem_args, obj._problem_kwargs = args, kwargs.copy()
        return obj

    @property
    def num_binary_variables(self):
        """num_binary_variables.

        The number of binary variables that the QUBO/Ising uses. Should be
        implemented in the child class.

        Return
        -------
        num : int.
            The number of variables in the QUBO/Ising formulation.

        """
        return self.to_qubo().num_binary_variables

    def __repr__(self):
        """__repr__.

        Same as __str__, but will give a truncted output.

        Return
        -------
        s : str.

        """
        s = str(self)
        if len(s) < 50:
            return s
        return s[:50] + " ...)"

    def __str__(self):
        """__str__.

        Defined such that the following is true (assuming you have imported
        * from qcware.optimization.problems).

        >>> s = Class_derived_from_Problem(*args)
        >>> eval(str(s)) == s
        True

        Return
        -------
        s : str.

        """
        s = self.__class__.__name__ + "("
        if not self._problem_args and not self._problem_kwargs:
            return s + ")"
        for a in self._problem_args:
            val = str(a) if not isinstance(a, str) else "'%s'" % a
            s += val + ", "
        for k, v in self._problem_kwargs.items():
            val = str(v) if not isinstance(v, str) else "'%s'" % v
            s += str(k) + "=" + val + ", "
        return s[:-2] + ")"

    def __eq__(self, other):
        """__eq__.

        Determine if ``self`` and ``other`` define the same problem.

        Parameters
        ----------
        other : an object derived from the ``Problem`` class.

        Return
        -------
        eq : boolean.
            If ``self`` and ``other`` represent the same problem.

        """
        return (
            isinstance(other, type(self)) and
            self._problem_args == other._problem_args and
            self._problem_kwargs == other._problem_kwargs
        )

    def convert_solution(self, solution, *args, **kwargs):
        """convert_solution.

        Convert the solution to the QUBO to the solution to the problem.
        Should be implemented in child classes. If it is not implemented in the
        child class, then this function will by default return the same
        solution as what inputted.

        Parameters
        ----------
        solution : iterable or dict.
            The QUBO or Ising solution output. The QUBO solution output
            is either a list or tuple where indices specify the label of the
            variable and the element specifies whether it's 0 or 1 for QUBO
            (or -1 or 1 for Ising), or it can be a dictionary that maps the
            label of the variable to is value.

        Return
        -------
        Implemented in the child class.

        """
        return solution

    def is_solution_valid(self, solution, *args, **kwargs):
        """is_solution_valid.

        Returns whether or not the proposed solution is valid. Should be
        implemented in child classes. If it is not implemented in the child
        class, then this function will by default return True.

        Parameters
        ----------
        solution : iterable or dict.
            solution can be the output of ``convert_solution``,
            or the  QUBO or Ising solver output. The QUBO solution output
            is either a list or tuple where indices specify the label of the
            variable and the element specifies whether it's 0 or 1 for QUBO
            (or -1 or 1 for Ising), or it can be a dictionary that maps the
            label of the variable to is value.

        Return
        -------
        valid : boolean.
            True if the proposed solution is valid, else False.

        """
        return True

    def solve_bruteforce(self, *args, **kwargs):
        """solve_bruteforce.

        Solve the problem bruteforce. THIS SHOULD NOT BE USED FOR LARGE
        PROBLEMS! This is implemented in the parent ``qcware.optimization.utils.Problem``
        class. Some problems use a lot of slack binary variables for their
        QUBO/Ising formulations. If this is the case, then the child class
        for this problem should override this method with a better bruteforce
        solver. But, for problems that do not use slack variables, this
        method will suffice. It converts the problem to QUBO, solves it with
        ``qcware.optimization.utils.solve_qubo_bruteforce``, and then calls and returns
        ``convert_solution``.

        Parameters
        ----------
        aruments : arguments and keyword arguments.
            Contains args and kwargs for the ``to_qubo`` method. Also contains
            a ``all_solutions`` boolean flag, which indicates whether or not
            to return all the solutions, or just the best one found.
            ``all_solutions`` defaults to False.

        Return
        ------
        res : the output or outputs of the ``convert_solution`` method.
            If ``all_solutions`` is False, then ``res`` is just the output
            of the ``convert_solution`` method.
            If ``all_solutions`` is True, then ``res`` is a list of outputs
            of the ``convert_solution`` method, e.g. a converted solution
            for each solution that the bruteforce solver returns.

        """
        kwargs = kwargs.copy()
        all_solutions = kwargs.pop("all_solutions", False)
        qubo = self.to_qubo(*args, **kwargs)
        sol = qubo.solve_bruteforce(all_solutions)
        if all_solutions:
            return [self.convert_solution(x) for x in sol]
        return self.convert_solution(sol)

    def solve(self, key, **kwargs):
        """solve.

        Call ``qcware.optimization.solve_binary``, and convert the
        outputted solution/solutions.

        Parameters
        ----------
        key : str.
            API key.
        kwargs : dict.
            Keyword arugments for the ``qcware.optimization.solve_binary``
            function.

        Returns
        -------
        res : qcware.optimization.SolveBinaryResult object.

        """
        kwargs = kwargs.copy()
        kwargs["key"] = key
        kwargs["convert_solution"] = self.convert_solution
        kwargs["Q"] = self.to_qubo()
        return qcware.optimization.solve_binary(**kwargs)