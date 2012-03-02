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
    # verify we can access its elements
    for i in range(len(p)): assert i == p[i]
    # and return it
    return p


# main
if __name__ == "__main__":
    test()


# end of file 