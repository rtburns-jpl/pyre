# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import weakref
import collections
import pyre.tracking
from pyre.calc.HierarchicalModel import HierarchicalModel


class Model(HierarchicalModel):
    """
    A specialization of a hierarchical model that takes into account that the model nodes have
    priorities attached to them and cannot indiscriminately replace each other
    """


    # types
    from .Slot import Slot


    # interface from HierarchicalModel
    def register(self, *, node, name=None, key=None):
        # print("pyre.config.Model.register: name={!r}, key={!r}".format(name, key))
        # build the name
        name = name if name is not None else self.separator.join(key)
        # build the key
        key = tuple(key) if key is not None else name.split(self.separator)
        # build the namespace key and name
        nskey = key[:-1]
        nsname = self.separator.join(nskey)
        item = key[-1]
        # check whether this namespace is known
        try:
            component = self.configurables[nsname]
        # nope: register it as a normal node
        except KeyError:
            return super()._register(
                name=item, fqname=name, node=node, hashkey=self._hash.hash(key))
        # we have a component: treat the name as a property
        descriptor = component.pyre_getTraitDescriptor(alias=item)
        # get the corresponding inventory slot
        slot = component.pyre_inventory[descriptor]
        # merge the two
        slot.merge(other=node)
        # all done
        return self


    def resolve(self, *, name=None, key=None):
        # print("pyre.config.Model.resolve: name={!r}, key={!r}".format(name, key))
        # build the name
        name = name if name is not None else self.separator.join(key)
        # build the key
        key = key if key is not None else name.split(self.separator)
        # build the namespace key and name
        nskey = key[:-1]
        nsname = self.separator.join(nskey)
        item = key[-1]
        # check whether this namespace is known
        try:
            component = self.configurables[nsname]
        # nope: resolve it as a normal node
        except KeyError:
            return super()._resolve(name=item, fqname=name, hashkey=self._hash.hash(key))
        # we have a component: treat the name as a property
        descriptor = component.pyre_getTraitDescriptor(alias=item)
        # and return the corresponding inventory slot
        return component.pyre_inventory[descriptor]


    # interface for my configurator
    def registerComponentClass(self, component):
        """
        Adjust the model for the presence of a component

        Look through the model for settings that correspond to {component} and transfer them to
        its inventory. Register {component} as the handler of future configuration events in
        its namespace
        """
        # the accumulator of error
        errors = []
        # get the class family
        family = component.pyre_family
        # if there is no family, we are done
        if not family: return errors
        # get the class inventory
        inventory = component.pyre_inventory
        # let's see what is known about {component}
        for key, name, fqname, node in self.children(rootKey=family):
            # find the corresponding descriptor
            try:
                descriptor = component.pyre_getTraitDescriptor(alias=name)
            # found a typo?
            except component.TraitNotFoundError as error:
                errors.append(error)

            # get the inventory slot
            slot = inventory[descriptor]
            # merge the slots
            slot.merge(other=node)
            # patch me
            self.patch(old=node, new=slot)
            # replace the node with the inventory slot so aliases still work
            self._nodes[key] = slot
            # and eliminate the old node from the name stores
            del self._names[key]
            del self._fqnames[key]
        # establish {component} as the handler of events in its configuration namespace
        self.configurables[self.separator.join(family)] = component
        # return the accumulated errors
        return errors


    # configuration event processing
    def bind(self, key, value, priority=None, locator=None):
        """
        Build a node with the given {priority} to hold {value}, and register it under {key}
        """
        # build a new node 
        slot = self.recognize(value=value, priority=priority)
        # get it registered
        return self.register(node=slot, key=key)


    def defer(self, component, family, key, value, locator, priority):
        """
        Build a node that corresponds to a conditional configuration
        """
        # print("Model.defer:")
        # print("    component={}, family={}".format(component, family))
        # print("    key={}, value={!r}".format(key, value))
        # print("    from {}".format(locator))
        # print("    with priority {}".format(priority))

        # hash the component name
        ckey = self._hash.hash(component)
        # hash the family key
        fkey = self._hash.hash(family)
        # get the deferred event store
        model = self.deferred[(ckey, fkey)]
        # build a slot
        slot = self.recognize(value=value, priority=priority)
        # and add it to the pile
        model.append( (key, slot) )
        # all done
        return slot


    def load(self, source, locator, **kwds):
        """
        Ask the pyre {executive} to load the configuration settings in {source}
        """
        # get the executive to kick start the configuration loading
        self.executive.loadConfiguration(uri=source, locator=locator)
        # and return
        return self


    # factory for my nodes
    def newNode(self, *, value=None, evaluator=None, priority=None, **kwds):
        """
        Create a new node with the given evaluator
        """
        # why is this the right node factory?
        # subclasses should override this to provide their own nodes to host the evaluator
        return self.Slot(value=None, evaluator=evaluator, priority=priority)


    # meta methods
    def __init__(self, executive, **kwds):
        super().__init__(**kwds)
        # record the executive
        self.executive = weakref.proxy(executive)
        # the database of deferred bidings
        self.deferred = collections.defaultdict(list)
        # the configurables that manage theor own namespace
        self.configurables = weakref.WeakValueDictionary()
        # done
        return


    # subscripted access
    def __setitem__(self, name, value):
        """
        Support for programmatic modification of the configuration store
        """
        # build a slot
        slot = self.recognize(value=value)
        # build a locator
        locator = pyre.tracking.here(level=1)
        # register the slot
        self.register(name=name, node=slot)
        # and return
        return


    def dump(self, pattern=None):
        super().dump(pattern)
        if self.configurables:
            print("  configurables:")
            for name in self.configurables:
                print("    {!r}".format(name))
        return


# end of file 
