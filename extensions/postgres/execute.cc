// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
// 

#include <portinfo>
#include <iostream>

#include <Python.h>
#include <libpq-fe.h>

#include "execute.h"


// establish a new connection
const char * const
pyre::extensions::postgres::
execute__name__ = "execute";

const char * const
pyre::extensions::postgres::
execute__doc__ = "execute a single command";

PyObject * 
pyre::extensions::postgres::
execute(PyObject *, PyObject * args) {
    // the connection specification
    const char * command;
    PyObject * connection;
    // extract the arguments
    if (!PyArg_ParseTuple(args, "O!s:execute", &PyCapsule_Type, &connection, &command)) {
        return 0;
    }

    // all done
    Py_INCREF(Py_None);
    return Py_None;
}

// end of file