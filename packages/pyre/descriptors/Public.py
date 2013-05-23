# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


class Public:
    """
    Mix-in class that endows descriptors with a name, aliases and support for simple
    documentation
    """
    

    # public data
    name = None # my name
    aliases = None # a set (eventually) of alternate names by which I can be accessed

    # documentation support
    tip = '' # short description of my purpose

    # wire doc to __doc__ so the bultin help can decorate the attributes properly
    @property
    def doc(self):
        """
        Return my documentation string
        """
        return self.__doc__

    @doc.setter
    def doc(self, text):
        """
        Store text as my documentation string
        """
        self.__doc__ = text
        return


    # framework requests
    def attach(self, name, **kwds):
        """
        Called by my client after all the available meta-data has been harvested
        """
        # set my canonical name
        self.name = name
        # update my aliases, so that I can provide easy access to the full set of my names
        self.aliases.add(name)

        # chain up
        return super.__init__(name=name, **kwds)


    # meta methods
    def __init__(self, name=None, **kwds):
        # chain up
        super().__init__(**kwds)

        # initialize my aliases
        self.aliases = set() if name is None else {name}
        # make sure I have a {__doc__} for the user to modify
        self.__doc__ = None

        # all done
        return
        

# end of file 