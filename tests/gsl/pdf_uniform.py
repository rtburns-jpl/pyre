#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Exercise the uniform pdf
"""


def test():
    # access the package
    import gsl

    # the support of the distribution
    support = (-1,1)
    # build a random number generator
    rng = gsl.rng()
    # build a uniform distribution
    uniform = gsl.pdf.uniform(support)

    # sample it
    sample = uniform.sample(rng)
    assert sample >= support[0] and sample < support[1]

    density = uniform.density(0)
    assert density == 1/(support[1]-support[0])

    return uniform


# main
if __name__ == "__main__":
    test()


# end of file 