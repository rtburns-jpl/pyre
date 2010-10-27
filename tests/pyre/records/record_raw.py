#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Instantiate a record using the raw form
"""


import pyre.records


class record(pyre.records.record):
    """
    A sample record
    """
    sku = pyre.records.field()
    description = pyre.records.field()
    cost = pyre.records.field()
    overhead = pyre.records.field()
    price = pyre.records.field()


def test():
    # build a record
    r = record.pyre_raw(data=("9-4013", "organic kiwi", .85, .15, 1.0))
    # check
    assert r.sku == "9-4013"
    assert r.description == "organic kiwi"
    assert r.cost == .85
    assert r.overhead == .15
    assert r.price == 1.0

    return r


# main
if __name__ == "__main__":
    test()


# end of file 
