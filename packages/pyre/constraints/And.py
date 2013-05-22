# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# superclass
from .Constraint import Constraint


# declaration
class And(Constraint):
    """
    Meta-constraint that is satisfied when all of its constraints are satisfied
    """


    # interface
    def validate(self, candidate):
        """
        Check whether {candidate} satisfies this constraint
        """
        # i am happy only if every one of my constraints is happy
        for constraint in self.constraints: constraint.validate(candidate)
        # return success
        return candidate


    # meta-methods
    def __init__(self, *constraints, **kwds):
        # chain up
        super().__init__(**kwds)
        # save my list of constraints
        self.constraints = constraints
        # all done
        return


    def __str__(self):
        return " and ".join("({})".format(constraint) for constraint in self.constraints)


# end of file 
