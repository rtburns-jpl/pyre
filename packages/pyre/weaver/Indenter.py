# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


class Indenter:
    """
    A mix-in class that keeps track of the indentation level
    """


    # public data
    leader = "" # the current contents to prepend to every line


    # interface
    def indent(self):
        """
        Increase the indentation level by one
        """
        self._level += 1
        self.leader = self._indenter * self._level
        return


    def outdent(self):
        """
        Decrease the indentation level by one
        """
        self._level -= 1
        self.leader = self._indenter * self._level
        return


    def place(self, line):
        return self.leader + line


    # meta methods
    def __init__(self, indenter=None, **kwds):
        super().__init__(**kwds)

        self._level = 0
        self.leader = ""
        self._indenter = self.INDENTER if indenter is None else indenter

        return


    # constants
    INDENTER = " "*4


    # private data
    _level = 0
    _indenter = None


# end of file 
