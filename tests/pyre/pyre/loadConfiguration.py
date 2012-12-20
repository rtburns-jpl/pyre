#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Exercise loading a configuration file explicitly
"""


def test():
    # access the framework
    import pyre

    # load the configuration file
    pyre.loadConfiguration('vfs:/pyre/startup/sample.cfg')

    # access the nameserver
    ns = pyre.executive.nameserver

    # verify that the configuration settings were read properly
    assert ns["package.home"] == "home"
    assert ns["package.prefix"] == "prefix"
    assert ns["package.user.name"] == "michael a.g. aïvázis"
    assert ns["package.user.email"] == "aivazis@caltech.edu"
    assert ns["package.user.affiliation"] == "california institute of technology"

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file 