#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Verify that the trait defaults get bound correctly from the configuration store
"""


def test():
    import pyre

    # declare a protocol
    class job(pyre.protocol):
        """a protocol"""
        @pyre.provides
        def do(self):
            """do something"""

    # declare a component the implements this protocol
    class worker(pyre.component, family="sample.worker", implements=job):
        """an implementation"""
        host = pyre.properties.str(default="localhost")
        @pyre.export
        def do(self):
            """do something"""

    # declare a component
    class component(pyre.component, family="sample.manager"):
        """the base component"""
        jobs = pyre.properties.int(default=1)
        gopher = job(default=worker)
        @pyre.export
        def say(self):
            """say something"""

    # instantiate the component
    c = component(name="c")
    # check that the configuration settings were applied correctly
    assert c.jobs == 10
    assert isinstance(c.gopher, worker)
    assert c.gopher.pyre_name == "c.gopher"
    assert c.gopher.host == "foxtrot.caltech.edu"
    # instantiate the worker
    w = worker(name="w")
    assert w.host == "pyre.caltech.edu"
    # bind the two; verify that that {w} retained its configuration as a result of the assignment
    c.gopher = w
    # check that the binding left {w} untouched
    assert c.gopher == w
    assert c.gopher.pyre_name == "w"
    assert c.gopher.host == "pyre.caltech.edu"

    return c


# main
if __name__ == "__main__":
    test()


# end of file 
