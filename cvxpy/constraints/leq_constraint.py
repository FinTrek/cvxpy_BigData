"""
Copyright 2013 Steven Diamond

This file is part of CVXPY.

CVXPY is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

CVXPY is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with CVXPY.  If not, see <http://www.gnu.org/licenses/>.
"""

class LeqConstraint(object):
    OP_NAME = "<="
    def __init__(self, lh_exp, rh_exp):
        self.lh_exp = lh_exp
        self.rh_exp = rh_exp
        self._expr = self.lh_exp - self.rh_exp

    def name(self):
        return ' '.join([self.lh_exp.name(), 
                         self.OP_NAME, 
                         self.rh_exp.name()])

    def __repr__(self):
        return self.name()

    @property
    def size(self):
        return self._expr.size

    # Left hand expression must be convex and right hand must be concave.
    def is_dcp(self):
        return self._expr.curvature.is_convex()

    # Replace inequality with an equality with slack.
    def canonicalize(self):
        lh_obj,lh_constr = self.lh_exp.canonicalize()
        rh_obj,rh_constr = self.rh_exp.canonicalize()
        constraints = lh_constr + rh_constr + [self.__class__(lh_obj, rh_obj)]
        return (None, constraints)

    def variables(self):
        return self._expr.variables()

    def coefficients(self):
        return self._expr.coefficients()

    # The value of the dual variable.
    @property
    def dual_value(self):
        return self._dual_value

    # Save the value of the dual variable for the constraint's parent.
    def save_value(self, value):
        self._dual_value = value