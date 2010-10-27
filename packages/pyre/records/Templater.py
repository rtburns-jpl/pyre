# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from ..patterns.AttributeClassifier import AttributeClassifier


class Templater(AttributeClassifier):
    """
    Metaclass that inspects records and extracts their field descriptors
    """


    # types
    from .Field import Field


    # meta methods
    def __new__(cls, name, bases, attributes, **kwds):
        """
        Build a new {Record} class
        """
        # harvest the locally declared fields from the class declaration
        localFields = tuple(cls.pyre_harvest(attributes, cls.Field))
        # remove them from the attributes for now
        # we will replace them with record specific accessors in __init__; see below
        for field in localFields:
            del attributes[field.name]

        # disable the wasteful __dict__
        attributes["__slots__"] = ()

        # build the class record
        record = super().__new__(cls, name, bases, attributes, **kwds)

        # attach the local fields
        record.pyre_localFields = localFields

        # scan the mro for inherited fields, subject to name shadowing
        # initialize the temporary storage for the harvest
        inherited = []
        # prime the set of known names
        known = set(attributes)
        # iterate over my ancestors
        for base in record.__mro__[1:]:
            # narrow the search down to subclasses of Record
            if isinstance(base, cls):
                # loop over this ancestor's local fields
                for field in base.pyre_localFields:
                    # skip this field if it is shadowed
                    if field.name in known: continue
                    # otherwise save it
                    inherited.append(field)
            # in any case, add the attributes of this base to the known pile
            known.update(base.__dict__)
        # attach the inherited fields to the record
        record.pyre_inheritedFields = tuple(inherited)

        # return the record
        return record


    def __init__(self, name, bases, attributes, **kwds):
        """
        Decorate a newly minted {Record} class
        """
        # delegate
        super().__init__(name, bases, attributes, **kwds)

        # iterate over all the fields in declaration order
        for index, descriptor in enumerate(self.pyre_fields()):
            # build the data accessor
            accessor = self.pyre_accessor(index=index, descriptor=descriptor)
            # and attach it
            setattr(self, descriptor.name, accessor)
        return


# end of file 
