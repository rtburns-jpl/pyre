# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# externals
import collections
# access the framework
import pyre
# get my protocol
from .Terminal import Terminal as terminal


# declaration
class Plain(pyre.component, family='pyre.terminals.plain', implements=terminal):
    """
    A terminal that provides no color capabilities
    """

    # implementation details
    colors = collections.defaultdict(str) # all color decorations are empty strings...


# end of file
