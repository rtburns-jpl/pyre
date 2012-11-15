// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2012 all rights reserved
// 

#include <portinfo>
#include <Python.h>

#include "metadata.h"


// copyright
const char * const
mpigsl::
copyright__name__ = "copyright";

const char * const
mpigsl::
copyright__doc__ = "the module copyright string";

PyObject * 
mpigsl::
copyright(PyObject *, PyObject *)
{
    const char * const copyright_note = "mpigsl: (c) 1998-2012 Michael A.G. Aïvázis";
    return Py_BuildValue("s", copyright_note);
}
    

// version
const char * const
mpigsl::
version__name__ = "version";

const char * const 
mpigsl::
version__doc__ = "the module version string";

PyObject * 
mpigsl::
version(PyObject *, PyObject *)
{
    const char * const version_string = "0.0";
    return Py_BuildValue("s", version_string);
}

    
// end of file