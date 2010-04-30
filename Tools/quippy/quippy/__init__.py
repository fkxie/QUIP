# HQ XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# HQ X
# HQ X   quippy: Python interface to QUIP atomistic simulation library
# HQ X
# HQ X   Copyright James Kermode 2010
# HQ X
# HQ X   These portions of the source code are released under the GNU General
# HQ X   Public License, version 2, http://www.gnu.org/copyleft/gpl.html
# HQ X
# HQ X   If you would like to license the source code under different terms,
# HQ X   please contact James Kermode, james.kermode@gmail.com
# HQ X
# HQ X   When using this software, please cite the following reference:
# HQ X
# HQ X   http://www.jrkermode.co.uk/quippy
# HQ X
# HQ XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

"""quippy package

James Kermode <james.kermode@kcl.ac.uk>

Contains python bindings to the libAtoms/QUIP Fortran 95 codes
<http://www.libatoms.org>. """

import sys
assert sys.version_info >= (2,4,0)

import cPickle, atexit, os, numpy, logging
from numpy import *

logging.root.setLevel(logging.WARNING)

AtomsReaders = {}
AtomsWriters = {}

import _quippy

# Reference values of .true. and .false. from Fortran
QUIPPY_TRUE = _quippy.qp_reference_true()
QUIPPY_FALSE = _quippy.qp_reference_false()

from oo_fortran import FortranDerivedType, FortranDerivedTypes, fortran_class_prefix, wrap_all

# Read spec file generated by f90doc and construct wrappers for classes
# and routines found therein.

def quippy_cleanup():
   _quippy.qp_verbosity_pop()
   _quippy.qp_system_finalise()

_quippy.qp_system_initialise(-1)
_quippy.qp_verbosity_push(0)
atexit.register(quippy_cleanup)

trial_spec_files = [os.path.join(os.path.dirname(__file__),'quippy.spec'),
                    os.path.join(os.getcwd(), 'quippy.spec')]
                    
for spec_file in trial_spec_files:
   try:
      spec = cPickle.load(open(spec_file))
      break
   except IOError:
      continue
else:
   raise IOError('quippy.spec file not found in locations %s' % trial_spec_files)

classes, routines, params = wrap_all(_quippy, spec, spec['wrap_modules'], spec['short_names'], prefix='qp_')

for name, cls in classes:
   setattr(sys.modules[__name__], name, cls)

for name, routine in routines:
   setattr(sys.modules[__name__], name, routine)

sys.modules[__name__].__dict__.update(params)

import extras
for name, cls in classes:
   try:
      new_cls = getattr(extras, name[len(fortran_class_prefix):])
   except AttributeError:
      new_cls = type(object)(name[len(fortran_class_prefix):], (cls,), {})

   setattr(sys.modules[__name__], name[len(fortran_class_prefix):], new_cls)
   FortranDerivedTypes['type(%s)' % name[len(fortran_class_prefix):].lower()] = new_cls

del classes
del routines
del params
del wrap_all
del fortran_class_prefix

import farray;      from farray import *
import atomslist;   from atomslist import *
import periodic;    from periodic import *
import xyz_netcdf;  from xyz_netcdf import *
import util;        from util import *

try:
   import atomeye
except ImportError:
   logging.warning('_atomeye extension module not available - atomeye interface disabled')

import sio2, povray, aseinterface, cube

try:
   import castep
except ImportError:
   logging.warning('quippy.castep import failed.')

