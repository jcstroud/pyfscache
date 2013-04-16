import os
import time
import shutil
import unittest


from pyfscache.fscache import *
from pyfscache.fscache import LifetimeError


TESTCACHE = 'test-cache'

state = {'abort' : False}


class C(object):
  def __init__(self):
    f = FSCache(TESTCACHE)
    self.doit = f(self.doit)
  def doit(self, a, r, g, s):
    if state['abort']:
      raise Exception
    return [a, r, g, s]

class FSCacheTestCase(unittest.TestCase):
  def setUp(self):
    # class C(object): pass
    path_name = TESTCACHE
    self.path_name = os.path.abspath(path_name)
    self.f = FSCache(self.path_name)
    self.x = FSCache(self.path_name, seconds=0.3)
    self.f.purge()
    self.names = ['ETajeDeuWH9cB2alMEOUaBPQ2by_gf_IMb=gU5B3Tz',
                  'zGa=5yeyE6wYkE9pVICruCO_JG5cBjWYNJNOPZnXQa']
    self.names.sort()
    self.first = 'abcd'
    self.second = 'efgh'
    self.f[1] = self.first
    self.f[2] = self.second
  def tearDown(self):
    shutil.rmtree(self.path_name)
  def test_001_names(self):
    self.assertEqual(self.f.get_names(), self.names)
  def test_002_purge(self):
    self.f.purge()
    self.assertEqual(self.f.get_names(), [])
    # print "f.names should be []. They are:", f.names()
  def test_003_setitem_getitem_with_int(self):
    adict = dict(zip('abcdef',range(6)))
    bdict = adict.copy()
    # print 'adict is:', adict
    self.f[3] = adict
    self.assertEqual(self.f[3], bdict)
  def test_004_setitem_getitem_with_list(self):
    adict = dict(zip('abcdef',range(6)))
    bdict = adict.copy()
    self.f[[2,3,4]] = adict
    self.assertEqual(self.f[[2,3,4]], bdict)
  def test_005_delitem(self):
    self.assertTrue(self.f.is_loaded(2))
    del self.f[2]
    self.assertFalse(self.f.is_loaded(2))
  def test_006_expire(self):
    self.assertTrue(self.f.is_loaded(2))
    self.f.expire(2)
    self.assertFalse(self.f.is_loaded(2))
  def test_007_loaded_unload_isloaded(self):
    self.assertEquals(sorted(self.f.get_loaded()), self.names)
    self.f.unload(2)
    self.assertTrue(self.f.is_loaded(1))
    self.assertFalse(self.f.is_loaded(2))
  def test_008_contains(self):
    self.assertTrue(1 in self.f)
    self.f.unload(1)
    self.assertFalse(self.f.is_loaded(1))
    self.assertTrue(1 in self.f)
  def test_009_clear_load(self):
    self.f.clear()
    self.assertEquals(self.f.get_loaded(), [])
    self.assertEquals(sorted(self.f.get_names()), self.names)
    self.f.load(1)
    self.assertTrue(self.f.is_loaded(1))
  def test_010_update_item(self):
    new_second = 'ijkl'
    self.assertEqual(self.f[2], self.second)
    self.f.update_item(2, new_second)
    self.assertEquals(self.f[2], new_second)
  def test_011_path(self):
    self.assertEquals(self.f.path, self.path_name)
  def test_012_negative_lifetime(self):
    self.assertRaises(LifetimeError, FSCache,
                      self.path_name, seconds=60, minutes=-2)
    self.assertRaises(LifetimeError, FSCache,
                      self.path_name, seconds=180, minutes=-3)
  def test_100_make_key(self):
    digest = 'a2VKynHgDrUIm17r6BQ5QcA5XVmqpNBmiKbZ9kTu0A'
    adict = {'a' : {'b':1}, 'f': []}
    self.assertEquals(make_digest(adict), digest)
  def test_101_cache_function(self):
    abort = False
    def fun(a, b=2):
      if abort:
        raise
      return a + b
    def keyer(*args, **kwargs):
      return (args[0], kwargs['b'])
    a = 3
    b = 5
    key = keyer(a, b=b)
    result = fun(a, b=b)
    cfun = cache_function(fun, keyer, self.f)
    call_cfun = lambda: cfun(a, b=b)
    call_cfun()
    abort = True
    self.assertTrue(key in self.f)
    self.assertEquals(result, call_cfun())
  def test_102_auto_cache_function(self):
    abort = False
    def fun(a, b=2):
      if abort:
        raise
      return a + b
    a = 3
    b = 5
    result = fun(a, b=b)
    acfun = auto_cache_function(fun, self.f)
    call_acfun = lambda: acfun(a, b=b)
    call_acfun()
    abort = True
    self.assertEquals(result, call_acfun())
  def test_103_expiration(self):
    self.x['Bob'] = 18
    time.sleep(0.1)
    self.assertTrue('Bob' in self.x)
    time.sleep(0.21)
    self.assertTrue('Bob' not in self.f)
  def test_104_decorator(self):
    abort = False
    def fun(a, b=2):
      if abort:
        raise
      return a + b
    @self.f
    def acfun(a, b=2):
      if abort:
        raise
      return a + b
    a = 3
    b = 5
    result = fun(a, b=b)
    call_acfun = lambda: acfun(a, b=b)
    call_acfun()
    abort = True
    self.assertEquals(result, call_acfun())
  def test_105_instancemethod(self):
    state['abort'] = False
    c = C()
    c.doit(1, 2, 3, 4)
    state['abort'] = True
    self.assertEquals([1, 2, 3, 4], c.doit(1, 2, 3, 4))
  def test_106_ctype(self):
    cached_list = self.f(list)
    alist = cached_list((1, 2, 3))
    self.assertTrue(alist is cached_list((1, 2, 3)))
  def test_200_to_seconds(self):
    s = to_seconds(years=2.1, months=4.2, weeks=1.9, days=2,
                   hours=3.5, minutes=8,
                             seconds=10.87)
    self.assertEquals(s, 78649408.87)
    s = to_seconds(seconds=15, minutes=20)
    self.assertEquals(s, 1215.0)
    s = to_seconds(seconds=15.42, hours=10, minutes=18, years=2)
    self.assertEquals(s, 63150895.42)

    
def test_suite():
  tl = unittest.TestLoader()
  return tl.loadTestsFromTestCase(FSCacheTestCase)
