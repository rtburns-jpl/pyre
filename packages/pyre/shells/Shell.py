# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# access to my base class
import pyre


# declaration
class Shell(pyre.interface, family="pyre.shells"):
    """
    The interface implemented by the pyre application hosting strategies
    """


    # public data
    home = pyre.properties.str(default=None)
    home.doc = "the process home directory"


    # interface
    @pyre.provides
    def run(self, *args, **kwds):
        """
        Launch the application
        """


# end of file 