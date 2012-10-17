# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
from .. import tracking
# superclass
from .Requirement import Requirement


# class declaration
class Actor(Requirement):
    """
    The metaclass of components

    {Actor} takes care of all the tasks necessary to convert a component declaration into a
    configurable entity that coöperates fully with the framework
    """


    # types
    from .Role import Role
    from .exceptions import ImplementationSpecificationError, ProtocolError


    # meta-methods
    def __new__(cls, name, bases, attributes, *, family=None, implements=None, **kwds):
        """
        Build a new component record

        parameters:
            {cls}: the metaclass invoked; guaranteed to be a descendant of {Actor}
            {name}, {bases}, {attributes}: the usual class specification
            {implements}: the tuple of protocols that this component is known to implement
        """
        # build the protocol specification
        protocol = cls.pyre_buildProtocol(name, bases, implements)

        # build and add the protocol specification to the attributes
        attributes["pyre_implements"] = protocol
        # save the location of the component declaration
        attributes["pyre_locator"] = tracking.here(1)
        
        # get my ancestors to build the class record
        component = super().__new__(cls, name, bases, attributes, **kwds)

        # if a protocol spec was derivable from the declaration, check protocol compatibility 
        if protocol:
            # check whether the requirements were implemented correctly
            check = component.pyre_isCompatible(protocol)
            # if not
            if not check:
                # complain
                raise cls.ProtocolError(component, protocol, check)

        # and pass the component on
        return component


    def __init__(self, name, bases, attributes, *, family=None, **kwds):
        """
        Initialize a new component class record
        """
        # initialize the record
        super().__init__(name, bases, attributes, **kwds)

        # get the executive
        executive = self.pyre_executive

        # if this is an internal component, there is nothing further to do
        if self.pyre_internal: return

        # if the component author specified a family name
        if family:
            #  register the component class with the executive
            self.pyre_key = executive.registerComponentClass(
                family=family, component=self, locator=self.pyre_locator)
        # otherwise
        else:
            # i have no registration key
            self.pyre_key = None
        # register with the component registrar
        executive.registrar.registerComponentClass(component=self)
        # invoke the registration hook
        self.pyre_classRegistered()

        # build the component class inventory
        self.pyre_inventory = self.pyre_buildClassInventory()
        # if i have a registration key
        if self.pyre_key:
            # hand me to the configurator
            executive.configurator.configureComponentClass(component=self)
        # invoke the configuration hook
        self.pyre_classConfigured()

        # all done
        return
            

    def __call__(self, locator=None, **kwds):
        """
        Build an instance of one of my classes
        """
        # record the caller's location
        locator = tracking.here(1) if locator is None else locator
        # build the instance
        instance = super().__call__(locator=locator, **kwds)
        # and return it
        return instance


    def __setattr__(self, name, value):
        """
        Trap attribute setting in my class record instances to support setting the default
        value using the natural syntax
        """
        # print("Actor.__setattr__: {!r}<-{!r}".format(name, value))
        # recognize internal attributes
        if name.startswith('pyre_'):
            # and process them normally
            return super().__setattr__(name, value)
        # for the rest, try to
        try:
            # locate the trait 
            trait = self.pyre_trait(alias=name)
        # if it doesn't
        except self.TraitNotFoundError as error:
            # treat as a normal assignment
            return super().__setattr__(name, value)
        # the name refers to one of my traits; build an appropriate locator
        locator = tracking.here(level=1)
        # set the priority
        priority = self.pyre_executive.priority.explicit()
        # ask it to set the value
        trait.setClassTrait(configurable=self, value=value, locator=locator, priority=priority)
        # and return
        return


    def __str__(self):
        # get my family name
        family = self.pyre_family()
        # if i gave one, use it
        if family: return 'component {!r}'.format(family)
        # otherwise, use my class name
        return 'component {.__name__!r}'.format(self)


    # implementation details
    @classmethod
    def pyre_buildProtocol(cls, name, bases, implements):
        """
        Build a class that describes the implementation requirements imposed on this
        {component}, given its class record and the list of protocols it {implements}
        """
        # initialize the list of protocols
        protocols = []

        # try to understand what the component author specified
        if implements is not None:
            # accumulator for the protocols {component} doesn't implement correctly
            errors = []
            # if {implements} is a single protocol, add it to the pile
            if isinstance(implements, cls.Role): protocols.append(implements)
            # the only legal alternative is an iterable of {Protocol} subclasses
            else:
                try:
                    for protocol in implements:
                        # if it's an actual {Protocol} subclass
                        if isinstance(protocol, cls.Role):
                            # add it to the pile
                            protocols.append(protocol)
                        # otherwise, place it in the error bin
                        else:
                            errors.append(protocol)
                # if {implemenents} is not iterable
                except TypeError as error:
                    # put it in the error bin
                    errors.append(implements)
            # report the errors we encountered
            if errors: raise cls.ImplementationSpecificationError(name=name, errors=errors)

        # now, add the commitments made by my immediate ancestors
        protocols += [
            base.pyre_implements for base in bases
            if isinstance(base, cls) and base.pyre_implements is not None ]

        # bail out if we didn't manage to find any protocols
        if not protocols: return None
        # if there is only one protocol on my pile
        if len(protocols) == 1:
            # use it directly
            return protocols[0]
        # otherwise, derive an protocol from the harvested ones and return it as the
        # implementation specification
        return cls.Role("protocol".format(name), tuple(protocols), dict(), internal=True)


# end of file 
