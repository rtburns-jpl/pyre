# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#


PROJECT = pyre

#--------------------------------------------------------------------------
#

all: test

test: sanity

sanity:
	${PYTHON} ./sanity.py
	${PYTHON} ./extension.py
	${PYTHON} ./manager.py


# end of file
