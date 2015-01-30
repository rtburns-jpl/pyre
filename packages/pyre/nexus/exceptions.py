# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# exceptions
from ..framework.exceptions import FrameworkError


# local anchor
class NexusError(FrameworkError):
    """
    Base exceptions for all error conditions detected by nexus components
    """


# connection reset by peer
class ConnectionResetError(NexusError):
    """
    The connection was closed by the peer
    """


# end of file