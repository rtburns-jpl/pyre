# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#

# my metaclass: defined in the package initialization file
from . import _metaclass_Node

# my base class
from ..algebraic.AbstractNode import AbstractNode
# access to the node algebra mix-ins
from ..algebraic.Number import Number
# access to the structural mix-ins
from ..algebraic.Leaf import Leaf
from ..algebraic.Composite import Composite
# access to the functional mix-ins
from ..algebraic.Literal import Literal
from ..algebraic.Variable import Variable
from ..algebraic.Operator import Operator
from ..algebraic.Expression import Expression
from ..algebraic.Reference import Reference
from ..algebraic.Unresolved import Unresolved
# evaluation strategies
from ..algebraic.Memo import Memo
# local operators
from .Average import Average
from .Count import Count
from .Maximum import Maximum
from .Minimum import Minimum
from .Product import Product
from .Sum import Sum


# declaration of the base node
class Node(AbstractNode, Memo, Number, metaclass=_metaclass_Node):
    """
    The base class for lazily evaluated nodes. It employs the memoized evaluation strategy so
    that nodes have their values recomputed on demand.
    """


    # types: hooks for implementing the expression graph construction
    # structural
    leaf = Leaf
    composite = Composite
    # functional; they will be patched below with my subclasses
    literal = None
    variable = None
    operator = None
    expression = None
    reference = None
    unresolved = None


# literals
class literal(Node, Literal, Node.leaf):
    """
    Concrete class for representing foreign values
    """

# variables
class variable(Node, Variable, Node.leaf):
    """
    Concrete class for encapsulating the user accessible nodes
    """

# operators
class operator(Node, Operator, Node.composite):
    """
    Concrete class for encapsulating operations among nodes
    """

# expressions
class expression(Node, Expression, Node.composite):
    """
    Concrete class for encapsulating macros
    """

# references
class reference(Node, Reference, Node.composite):
    """
    Concrete class for encapsulating references to other nodes
    """

# unresolved nodes
class unresolved(Node, Unresolved, Node.leaf):
    """
    Concrete class for representing unknown nodes
    """

# local operators
class average(Node, Average, Node.composite):
    """
    Concrete class for representing the average value of a set of nodes
    """

class count(Node, Count, Node.composite):
    """
    Concrete class for representing the count of a set of nodes
    """

class max(Node, Maximum, Node.composite):
    """
    Concrete class for representing the maximum value of a set of nodes
    """

class min(Node, Minimum, Node.composite):
    """
    Concrete class for representing the minimum value of a set of nodes
    """

class product(Node, Product, Node.composite):
    """
    Concrete class for representing the product of nodes
    """

class sum(Node, Sum, Node.composite):
    """
    Concrete class for representing the sum of nodes
    """


# patch the base class
Node.literal = literal
Node.variable = variable
Node.operator = operator
Node.expression = expression
Node.reference = reference
Node.unresolved = unresolved


# end of file 
