# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Sanity check: verify that we can instantiate parsers
"""


def test():
    import pyre.xml
    return pyre.xml.newReader()


# main
if __name__ == "__main__":
    test()


# end of file 
