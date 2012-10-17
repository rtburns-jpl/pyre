#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Verify that the Actor metaclass decorates class records properly
"""


def test():
    # access
    import pyre

    # declare a class
    class base(pyre.component):
        """test class"""

    # did my ancestor list get built properly
    assert base.pyre_pedigree == (base, pyre.component)
        
    return base


# main
if __name__ == "__main__":
    test()


# end of file 
