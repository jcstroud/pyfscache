pyfscache
=========

A simple filesystem cache for python.

Home Page, Documentation, & Repository
--------------------------------------

- **Home Page**: http://pyfscache.bravais.net
- **Online Documentation**: http://pythonhosted.org/pyfscache/
- **Code Repository**: https://github.com/jcstroud/pyfscache/


Introduction
------------

Pyfscache (python filesystem cache) is a filesystem cache
that is easy to use. The principal class is `FSCache`,
instances of which may be used as decorators to create cached
functions with very little coding overhead:

.. code-block:: python

    import pyfscache
    cache_it = pyfscache.FSCache('some/cache/directory',
                                 days=13, hours=4, minutes=2.5)
    @cache_it
    def cached_doit(a, b, c):
      return [a, b, c]

It's that simple!

Now, every time the function ``cached_doit`` is called with a
particular set of arguments, the cache ``cache_it`` is inspected
to see if an identical call has been made before. If it has, then
the return value is retrieved from the ``cache_it`` cache. If not,
the return value is calculated with ``cached_doit``, stored in
the cache, and then returned.


Expiration
----------

In the code above, the expiration for ``cache_it`` is set to
1,137,750 seconds (13 days, 4 hours, and 2.5 minutes),
which means that every item created by ``cache_it`` has a lifetime
of 1,137,750 seconds, beginning when the item is made (*not*
beginning when ``cache_it`` is made). Values specifying lifetime
may be provided with the keywords ``years``, ``months``, ``weeks``,
``days``, ``hours``, ``minutes``, and ``seconds``. The lifetime is
the total for all keywords.

If these optional keyword arguments are not included, then items
added by the `FSCache` object never expire:

.. code-block:: python

    no_expiry_cache = pyfscache.FSCache('some/cache/directory')

.. note::

    Several instances of `FSCache` objects
    can use the same cache directory. Each will honor
    the expirations of the items therein. Thus, it is possible
    to have a cache mixed with objects of many differening
    lifetimes, made by many instances of
    `FSCache`.


Works Like a Map
----------------

Instances of `FSCache` work like mapping objects, supporting
item getting and setting:

.. code-block:: python

    >>> cache_it[('some', ['key'])] = {'some': 'value'}
    >>> cache_it[('some', ['key'])]
    {'some': 'value}

However, deletion with the ``del`` statement only works on memory.
To erase an item in the cache directory, use ``expire``:

.. code-block:: python

    >>> cache_it.get_loaded()
    ['LIlWpBZL68MBJaXouRjFBL3fzScyxh5q56hqSZ3DBK']
    >>> del cache_it[('some', ['key'])]
    >>> cache_it.get_loaded()
    []
    >>> ('some', ['key']) in cache_it
    True
    >>> cache_it[('some', ['key'])]
    {'some': 'value}
    >>> cache_it.expire(('some', ['key']))
    >>> ('some', ['key']) in cache_it
    False

Decorators
----------

What if you didn't write the function you want to cache?
Although their convenience is manifest in the example above,
it is not necessary to use decorators:

.. code-block:: python

    import pyfscache
    cache = pyfscache.FSCache('some/cache/directory',
                              days=13, hours=4, minutes=2.5)

    def uncached_doit(a, b, c):
      return [a, b, c]

    cached_doit = cache(uncached_doit)


Versatility
-----------

`FSCache` objects should work on the vast majority of python
"callables", including instance methods and even built-ins:

.. code-block:: python

    # a cached built-in
    cached_list = cache_it(list)

    # a cached instance method
    class AClass(object):
      @cahe_it
      def some_cached_instance_method(self, a, r, g, s):
        return (a + r) / (g * s)

.. note::

           The rule of thumb is that if python's *cPickle* module
           can handle the expected arguments to the cached function,
           then so can pyfscache.
