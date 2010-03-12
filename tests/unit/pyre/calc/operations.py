#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Verify on-the-fly building of nodes using the overloaded operators
"""


import pyre.calc


def test():
    # free variables
    c = 100.
    s = 20.

    # make some nodes
    cost = pyre.calc.newNode(value=c)
    shipping = pyre.calc.newNode(value=s)
    margin = cost / 2
    price = cost + margin + shipping
    profit = price - margin

    # gather them up
    nodes = [ cost, shipping, margin, price, profit ]

    # verify their values
    # print(cost.value, shipping.value, margin.value, price.value, profit.value)
    assert cost.value == c
    assert shipping.value == s
    assert margin.value == .5*cost.value
    assert price.value == cost.value + shipping.value + margin.value
    assert profit.value == price.value - margin.value

    # make some changes
    c = 200.
    s = 40.
    cost.value = c
    shipping.value = s

    # try again
    # print(cost.value, shipping.value, margin.value, price.value, profit.value)
    assert cost.value == c
    assert shipping.value == s
    assert margin.value == .5*cost.value
    assert price.value == cost.value + shipping.value + margin.value
    assert profit.value == price.value - margin.value

    return


# main
if __name__ == "__main__":
    # get the extent manager
    from pyre.patterns.ExtentAware import ExtentAware
    # install it
    pyre.calc._metaclass_Node = pyre.calc._metaclass_Evaluator = ExtentAware
    # run the test
    test()
    # verify reference counts
    # for nodes
    from pyre.calc.Node import Node
    # print([node for node in Node._pyre_extent])
    assert set(Node._pyre_extent) == set()
    # for evaluators
    from pyre.calc.Evaluator import Evaluator
    # print([evaluator for evaluator in Evaluator._pyre_extent])
    assert set(Evaluator._pyre_extent) == set()


# end of file 
