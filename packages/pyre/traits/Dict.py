# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
import collections
from .. import schemata
from .. import tracking

# superclass
from ..framework.Client import Client


# the helper container class
class Map(dict, Client):
    """
    Helper class that coerces values according to a supplied schema before storing them
    """

    # public data
    schema = None
    strategy = None # information necessary to make slots 

    # interface
    update = collections.abc.MutableMapping.update # forwards to __setitem__

    # meta-methods
    def __init__(self, schema, strategy, *args, **kwds):
        # chain up; careful to avoid bypassing the value coercion
        super().__init__()
        # set my schema
        self.schema = schema
        # and my strategy
        self.strategy = strategy
        # initialize my contents
        self.update(*args, **kwds)
        # all done
        return

    def __setitem__(self, name, value):
        """
        Store {value} in the map under {key}
        """
        # build a priority
        priority = self.pyre_nameserver.priority.explicit()
        # and a locator
        locator = tracking.here(1)
        # delegate
        return self.store(name=name, value=value, priority=priority, locator=locator)

    def __getitem__(self, key):
        """
        Retrieve the value associated with {key} and convert according to my schema
        """
        # get the slot
        node = super().__getitem__(key)
        # and return its value
        return node.value

    def store(self, name, value):
        super().__setitem__(name, value)
        return


class KeyMap(Map):
    """
    A storage strategy that is appropriate when a client has public inventory
    """

    # public data
    key = None

    # meta-methods
    def __init__(self, key, **kwds):
        # chain  up
        super().__init__(**kwds)
        # save my client's key
        self.key = key
        # all done
        return

    # slot access
    def store(self, name, value, priority, locator):
        """
        Build a slot to hold {value} and place it in the map
        """
        # straight out of {PublicInventory}
        # build the key
        key = self.key[name]
        # get the nameserver
        nameserver = self.pyre_nameserver
        # unpack the slot part
        macro, converter = self.strategy(model=nameserver)
        # build a slot to hold value
        new = macro(key=key, converter=converter, value=value, priority=priority, locator=locator)
        # adjust the model
        nameserver.insert(name=None, key=key, node=new)
        # and my map
        super().store(name, new)
        # all done
        return



class NameMap(Map):
    """
    A storage strategy for nameless clients
    """

    # meta-methods
    def store(self, name, value, priority, locator):
        """
        Build a slot to hold {value} and place it in the map
        """
        # straight out of {PrivateInventory}
        # get the nameserver
        ns = self.pyre_nameserver
        # unpack the slot part
        macro, converter = self.strategy(model=ns)
        # build the slot
        new = macro(key=None, converter=converter, value=value, locator=locator, priority=priority)
        # get the old slot 
        old = self[name]
        # pick the winner of the two
        winner = ns.node.select(model=ns, existing=old, replacement=new)
        # if the new slot is the winner
        if new is winner:
            # update the map
            super().store(name, new)
        # all done
        return


# superclass
from .Property import Property
# declaration
class Dict(Property):
    """
    A property that maps strings to components
    """


    # public data
    default = {} # a meaningless place holder; it gets coerced into some kind of map
    schema = schemata.identity


    # interface
    def identify(self, value, node, **kwds):
        """
        Walk {value} through the casting procedure
        """
        # make sure we build class slots and delegate
        return self.catalog(strategy=self.schema.classSlot, value=value, node=node)


    def coerce(self, value, node, **kwds):
        """
        Walk {value} through the casting procedure
        """
        # make sure we build instance slots and delegate
        return self.catalog(strategy=self.schema.instanceSlot, value=value, node=node)


    # configuration
    def classConfigured(self, component, **kwds):
        """
        Notification that the component class I am being attached to is configured
        """
        # chain up
        super().classConfigured(**kwds)
        # configure the component class record
        self.configureClient(
            client=component, myStrategy=self.classSlot, traitStrategy=self.schema.classSlot)
        # all done
        return self


    def instanceConfigured(self, instance, **kwds):
        """
        Notification that the component instance I am being attached to is configured
        """
        # chain up
        super().instanceConfigured(**kwds)
        # configure the component instance
        self.configureClient(
            client=instance, myStrategy=self.instanceSlot, traitStrategy=self.schema.instanceSlot)
        # all done
        return self


    # support for constructing slots
    def classSlot(self, model):
        """
        Hook registered with the nameserver that informs it of my macro preference and the
        correct converter to attach to new slots for component classes
        """
        # my schema knows
        return self.macro(model=model), self.identify


    def instanceSlot(self, model):
        """
        Hook registered with the nameserver that informs it of my macro preference and the
        correct converter to attach to new slots for component classes
        """
        # my schema knows
        return self.macro(model=model), self.coerce


    def macro(self, model):
        """
        Return my preferred macro processor
        """
        # ask my schema
        return self.schema.macro(model=model)


    # implementation details
    # configuration
    def configureClient(self, client, myStrategy, traitStrategy):
        # access the nameserver
        nameserver = self.pyre_nameserver
        # and the configurator
        configurator = self.pyre_configurator
        # get my schema
        schema = self.schema
        # find my slot
        slot = client.pyre_inventory[self]
        # this gets called only for public inventory items, so I am guaranteed a key
        key = slot.key
        # get my name
        tag = nameserver.getName(key)

        # make a key based map
        catalog = KeyMap(schema=schema, strategy=traitStrategy, key=key)

        # grab all direct assignments to this key
        for name, node in configurator.retrieveDirectAssignments(key):
            # extract the item key
            name = nameserver.split(name)[-1]
            # and store them
            catalog[name] = node.value

        # grab all deferred assignments to this key
        for assignment,priority in configurator.retrieveDeferredAssignments(key):
            # store them
            catalog[assignment.key[0]] = assignment.value

        # get the my current slot value
        current = slot.value
        # if non-trivial, use it to initialize my catalog; i expect it to be a dictionary
        # this must happen after direct and indirect assignments to avoid changing the
        # nameserver model while the update is taking place
        if current: catalog.update(current)

        # make a locator
        here = tracking.simple('while configuring {.pyre_name!r}'.format(client))

        # attach my new value
        client.pyre_inventory.setTrait(
            trait=self, strategy=myStrategy, 
            value=catalog, priority=nameserver.priority.user(), locator=here)
        
        # all done
        return


    # catalog initialization
    def catalog(self, strategy, value, node):
        """
        Instantiate and initialize an appropriate map
        """
        # {None} is special; leave it alone
        if value is None: return None

        # get the node key
        key = node.key
        # grab my schema
        schema = self.schema

        # decide which mapping strategy to use: if the {node} has no key
        if key is None:
            #  make a {NameMap}
            catalog = NameMap(schema=schema, strategy=strategy)
        # otherwise
        else:
            # make a key based map
            catalog = KeyMap(schema=schema, strategy=strategy, key=key)

        # populate the new map
        catalog.update(value)
        # and return it
        return catalog


    # meta-methods
    def __init__(self, schema=schema, default=default, **kwds):
        # chain up with a potentially adjusted default value
        super().__init__(default=default, **kwds)
        # record my schema
        self.schema = schema
        # all done
        return


# end of file 