# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# superclass
from .MPI import MPI


# the mpich package manager
class MPICH(MPI, family='pyre.externals.mpich'):
    """
    The package manager for MPICH packages
    """


# end of file 