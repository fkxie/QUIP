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

import unittest
from numpy import all, unravel_index, loadtxt
from quippy import frange, farray, FortranArray
from StringIO import StringIO

def string_to_array(s):
   return loadtxt(StringIO(s)).T


class QuippyTestCase(unittest.TestCase):

   def assertDictionariesEqual(self, d1, d2):
      if d1 != d2:
         if sorted(d1.keys()) != sorted(d2.keys()):
             self.fail('Dictionaries differ: d1.keys() (%r) != d2.keys() (%r)'  % (d1.keys(), d2.keys()))
         for key in d1:
            v1, v2 = d1[key], d2[key]
            if isinstance(v1, FortranArray):
               try:
                  self.assertArrayAlmostEqual(v1, v2)
               except AssertionError:
                  print key, v1, v2
                  raise
            else:
               if v1 != v2:
                  self.fail('Dictionaries differ: key=%s value1=%r value2=%r' % (key, v1, v2))
      

   def assertAtomsEqual(self, at1, at2, tol=1e-10):
      if at1 == at2: return

      if at1.n != at2.n:
         self.fail('Atoms objects differ: at1.n(%d) != at2.n(%d)' % (at1.n, at2.n))

      if abs(at1.lattice - at2.lattice).max() > tol:
         self.fail('Atoms objects differ: at1.lattice(%r) != at.lattice(%r)' % (at1.lattice, at2.lattice))

      self.assertDictionariesEqual(at1.params, at2.params)
      self.assertDictionariesEqual(at1.properties, at2.properties)
      
      # Catch all case
      self.fail('Atoms objects at1 and at2 differ')
   
   def assertArrayAlmostEqual(self, a, b, tol=1e-7):
      a = farray(a)
      b = farray(b)
      self.assertEqual(a.shape, b.shape)

      if a.dtype.kind != 'f':
         self.assert_((a == b).all())
      else:
         absdiff = abs(a-b)
         if absdiff.max() > tol:
            loc = [x+1 for x in unravel_index(absdiff.argmax()-1, absdiff.shape) ]
            print 'a'
            print a
            print
            print 'b'
            print b
            print
            print 'Absolute difference'
            if hasattr(a, 'transpose_on_print') and a.transpose_on_print:
               print absdiff.T
            else:
               print absdiff
            print

            self.fail('Maximum abs difference between array elements is %e at location %r' % (absdiff.max(), loc))
   
