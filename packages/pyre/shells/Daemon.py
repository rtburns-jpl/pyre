# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
import os # access to os services
import sys
import pyre # access the framework
from .Fork import Fork # my superclass


# declaration
class Daemon(Fork, family="pyre.shells.daemon"):
    """
    A shell that turns a process into a daemon, i.e. a process that is detached from its
    parent and has no access to a terminal
    """


    # interface
    @pyre.export
    def launch(self, application, *args, **kwds):
        """
        Invoke the application behavior

        For daemons, this is somewhat involved: the process forks twice in order to detach
        itself completely from its parent.
        """
        # if i was told not to spawn, just invoke the behavior
        if self.debug: return application.main(*args, **kwds)

        # otherwise, build the communication channels
        channels = self.channels()
        # fork
        pid = os.fork()

        # in the parent process, build and return the parent side channels
        if pid > 0: return self.parentChannels(channels)

        # in the intermediate child, decouple from the parent environment
        os.chdir("/")
        os.setsid()
        os.umask(0)

        # respawn
        pid = os.fork()

        # in the intermediate process, just exit
        if pid > 0: return os._exit(0)

        # in the final child process, convert {stdout} and {stderr} into channels
        stdout, stderr = self.childChannels(channels)
        # launch the application
        status = application.main(*args, stdout=stdout, stderr=stderr, **kwds)
        # and exit
        return sys.exit(status)


# end of file 
