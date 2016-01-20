# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# externals
import itertools
# support
from .. import primitives
# base class
from .Node import Node


# declaration
class Folder(Node):
    """
    The base class for filesystem entries that are containers of other entries

    {Node} and {Folder} are the leaf and container types for the composite that enables the
    representation of the hierarchical structure of filesystems.
    """


    # constants
    isFolder = True


    # types
    # my metadata
    from .metadata import FolderInfo as metadata
    # exceptions
    from .exceptions import (
        FolderInsertionError, NotRootError, FolderError, IsFolderError, NotFoundError)


    # interface
    def open(self):
        """
        Return an iterable over my contents
        """
        # return my contents
        return self.contents.items()


    # searching for specific contents
    def find(self, pattern):
        """
        Generate pairs ({node}, {name}) that match the given pattern

        By default, {find} will create a generator that visits the entire contents of the tree
        rooted at this folder. In order to restrict the set of matching names, provide a
        regular expression as the optional argument {pattern}
        """
        # access the finder factory
        from . import finder
        # to build one
        f = finder()
        # and start the search
        return f.explore(folder=self, pattern=pattern)


    # populating filesystems
    def discover(self, **kwds):
        """
        Fill my contents by querying whatever external resource my filesystem represents
        """
        # punt to the implementation in my filesystem
        return self.filesystem().discover(root=self, **kwds)


    # making entire filesystems available through me
    def mount(self, uri, filesystem):
        """
        Make the root of {filesystem} available as {uri} within my filesystem
        """
        # easy enough: just insert {filesystem} at {uri}
        return self._insert(uri=primitives.path(uri), node=filesystem)


    # node factories
    def node(self):
        """
        Build a new node within my filesystem
        """
        # easy enough
        return Node(filesystem=self.filesystem())


    def folder(self):
        """
        Build a new folder within my filesystem
        """
        # also easy
        return Folder(filesystem=self.filesystem())


    # meta methods
    def __init__(self, **kwds):
        """
        Build a folder. See {pyre.filesystem.Node} for construction parameters
        """
        # chain up
        super().__init__(**kwds)
        # initialize my contents
        self.contents = {}
        # and return
        return


    def __iter__(self):
        """
        Return an iterator over my {contents}
        """
        # easy enough
        return iter(self.contents)


    def __getitem__(self, uri):
        """
        Retrieve a node given its {uri} as the subscript
        """
        # invoke the implementation and return the result
        return self._retrieve(uri=primitives.path(uri))


    def __setitem__(self, uri, node):
        """
        Attach {node} at {uri}
        """
        # invoke the implementation and return the result
        return self._insert(node=node, uri=primitives.path(uri))


    def __contains__(self, uri):
        """
        Check whether {uri} is one of my children
        """
        # convert
        uri = primitives.path(uri)
        # starting with me
        node = self
        # attempt to
        try:
            # iterate over the names
            for name in uri.names: node = node.contents[name]
        # if node is not a folder, report failure
        except AttributeError: return False
        # if {name} is not among the contents of node, report failure
        except KeyError: return False
        # if we get this far, report success
        return True


    # implementation details
    def _retrieve(self, uri):
        """
        Locate the entry with address {uri}
        """
        # starting with me
        node = self
        # attempt to
        try:
            # hunt down the target node
            for name in uri.names: node = node.contents[name]
        # if any of the folder lookups fail
        except KeyError:
            # notify the caller
            raise self.NotFoundError(
                filesystem=self.filesystem(), node=self, uri=uri, fragment=name)
        # if one of the intermediate nodes is not a folder
        except AttributeError:
            # notify the caller
            raise self.FolderError(
                filesystem=self.filesystem(), node=self, uri=uri, fragment=node.uri)
        # otherwise, return the target node
        return node


    def _insert(self, node, uri, metadata=None):
        """
        Attach {node} at the address {uri}, creating all necessary intermediate folders.
        """
        # starting with me
        current = self
        # make an iterator over the directories in the parent of {uri}
        names = uri.parent.names
        # visit all the levels in {uri}
        for name in names:
            # attempt to
            try:
                # get the node associated with this name
                current = current.contents[name]
            # if not there
            except KeyError:
                # we have reached the edge of the contents of the filesystem; from here on,
                # every access to the contents of {current} will raise an exception and send us
                # here; so all we have to do is build folders until we exhaust {name} and
                # {names}
                for name in itertools.chain((name,), names):
                    # make a folder
                    folder = current.folder()
                    # attach it
                    current.contents[name] = folder
                    # inform the filesystem
                    current.filesystem().attach(node=folder, uri=(current.uri / name))
                    # and advance the cursor
                    current = folder
                # we should have exhausted the loop iterator so there should be no reason
                # to break out of the outer loop; check anyway
                assert tuple(names) == ()
            # if the {current} node doesn't have {contents}
            except AttributeError:
                # complain
                raise self.FolderError(
                    filesystem=current.filesystem(), node=current, uri=uri, fragment=name)

        # at this point, {current} points to the folder that should contain our {node}; get its
        # name by asking the input {uri}
        name = uri.name
        # attempt to
        try:
            # insert it into the contents of the folder
            current.contents[name] = node
        # if the {current} node doesn't have {contents}
        except AttributeError:
            # complain
            raise self.FolderInsertionError(
                filesystem=current.filesystem(), node=node, target=current.uri.name, uri=uri)
        # inform the filesystem
        current.filesystem().attach(node=node, uri=(current.uri / name), metadata=metadata)
        # and return the {node}
        return node


    # private data
    __slots__ = 'contents',


# end of file
