#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Load records from a csv file
"""


def test():
    import pyre.records

    # layout the record
    class item(pyre.records.record):
        # the fields
        sku = pyre.records.field()
        description = pyre.records.field()
        production = pyre.records.field()
        overhead = pyre.records.field()
        shipping = pyre.records.field()
        margin = pyre.records.field()
        # type information
        sku.type = pyre.schema.str()
        description.type = pyre.schema.str()
        production.type = pyre.schema.float()
        overhead.type = pyre.schema.float()
        shipping.type = pyre.schema.float()
        margin.type = pyre.schema.float()

    # build the target tuple
    target = [
        ("4000", "tomatoes", 2.95, 5, .2, 50),
        ("4001", "pepers", 0.35, 15, .1, 25),
        ("4002", "grapes", 1.65, 15, .15, 15),
        ("4003", "kiwis", 0.95, 7, .15, 75),
        ("4004", "lemons", 0.50, 4, .25, 50),
        ("4005", "oranges", 0.50, 4, .25, 50),
        ]

    # create the reader
    csv = pyre.records.csv()
    # read the csv data
    source = csv.read(layout=item, filename="vegetables.csv")
    # check
    for given, loaded in zip(target, source):
        assert given == loaded

    return


# main
if __name__ == "__main__":
    test()


# end of file 
