# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


class Processor:
    """
    The base class for decorators that attach value processors to descriptors
    """


    # public data
    descriptors = () # the sequence of descriptors that i decorate


    # meta methods
    def __init__(self, descriptors=descriptors, **kwds):
        # chain up
        super().__init__(**kwds)
        # record which descriptors i decorate
        self.descriptors = tuple(descriptors)
        # all done
        return


    def __call__(self, method):
        raise NotImplementedError(
            "class {.__name__!r} must implement '__call__'".format(type(self)))


# end of file 