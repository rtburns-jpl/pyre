# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis, leif strand
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# channel access
def pipe(descriptors=None, **kwds):
    """
    If {descriptors} is not {None}, it is expected to be a pair ({infd}, {outfd}) of already
    open file descriptors; just wrap a channel around them. Otherwise, build a pair of pipes
    suitable for bidirectional communication between two processes on the same host

    """
    # access the channel
    from .Pipe import Pipe
    # if we were handed already opened descriptors
    if descriptors:
        # unpack
        infd, outfd = descriptors
        # and go straight to the constructor
        return Pipe(infd=infd, outfd=outfd, **kwds)

    # build the pair and return it
    return Pipe.open(**kwds)


def tcp(address=None, connection=None):
    """
    Builds a channel over a TCP connection to a server

    If {connection} is not {None}, it is expected to be a valid and already connected socket,
    in which case this routine just wraps a channel around this existing connection.
    Otherwise, {address} is expected to be convertible to a {pyre.schema.inet} compatible
    address.
    """
    # access the channel
    from .SocketTCP import SocketTCP
    # get it to build the channel
    return SocketTCP.open(address=address, existing=connection)


# convenient access to the inet parser that builds addresses
def inet(spec=''):
    """
    Convert {spec} to a {pyre.schema.inet} address
    """
    # access the type
    from ..schema import inet
    # get it to cast the value
    return inet.pyre_cast(value=spec)


# marshaller access
from .Pickler import Pickler as pickler

# access to the scheduler
from .Scheduler import Scheduler as scheduler
# access to the selector
from .Selector import Selector as selector


# end of file 
