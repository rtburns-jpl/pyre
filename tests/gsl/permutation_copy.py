#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Create a permutation
"""


def test():
    # get the package
    import gsl
    # make a permutation
    p = gsl.permutation(shape=100).init()
    # check that we got a valid permutation back
    assert p
    # clone it
    q = p.clone()
    # check that it is valid
    assert q
    # and return them
    return p,q


# main
if __name__ == "__main__":
    test()


# end of file 