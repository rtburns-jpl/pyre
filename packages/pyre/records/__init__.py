# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#

# externals
from .. import descriptors

# access to the descriptor parts
field = descriptors.stem
measure = descriptors.descriptor
derivation = descriptors.operator
literal = descriptors.literal

# access to the typed field declarators
# basic
bool = descriptors.bool
decimal = descriptors.decimal
float = descriptors.float
inet = descriptors.inet
int = descriptors.int
identity = descriptors.identity
str = descriptors.str
# complex
date = descriptors.date
dimensional = descriptors.dimensional
time = descriptors.time
uri = descriptors.uri

# the decorators
converter = descriptors.converter
normalizer = descriptors.normalizer
validator = descriptors.validator


# the base class for field selectors
from .Selector import Selector as selector
# the record metaclass
from .Templater import Templater as templater
# access to the record class
from .Record import Record as record

# record extraction from formatted streams
from .CSV import CSV as csv


# end of file 
