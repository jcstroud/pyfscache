pyfscache
=========

A simple filesystem cache for python.

Home Page & Repository
----------------------

The phyles home page is at http://pyfscache.bravais.net
and the source code is maintained at github:
https://github.com/jcstroud/pyfscache/\.


Introduction
------------

Pyfscache (python filesystem cache) is a filesystem cache
that is easy to use. The principal class is
`FSCache`,
instances of which may be used as decorators to create cached
functions with very little coding overhead:

.. code-block:: python

    import pyfscache
    cache_it = pyfscache.FSCache('some/cache/directory',
                                 days=13, hours=4, minutes=2.5)
    @cache_it
    def cached_doit(a, b, c):
      return [a, b, c]

And that's it!

Now, every time the function `cached_doit` is called with a
particular set of arguments, the cache ``cache_it`` is inspected
to see if an identical call has been made before. If it has, then
the return value is retrieved from the ``cache_it`` cache. If not,
the return value is calculated with `cached_doit`, stored in
the cache, and then returned.


Expiration
----------

In the code above, the expiration for the ``cache`` is set to
1137750 seconds (13 days, 4 hours, and 2.5 minutes). Values
may be provided for ``years``, ``months``, ``weeks``, ``days``,
``hours``, ``minutes``, and ``seconds``. The time is the
total for all keywords.  

If these optional keyword arguments are not included, then items
added by the :`FSCache` object never expire:


.. code-block:: python

    no_expiry_cache = pyfscache.FSCache('some/cache/directory')

.. note::

    Several instances of `FSCache` objects
    can use the same cache directory. Each will honor
    the expirations of the items therein. Thus, it is possible
    to have a cache mixed with objects of many differening
    lifetimes, made by many instances of
    `FSCache`.


Decorators
----------

It is not necessary to use decorators, although their convenience
is manifest in the example above:

.. code-block:: python

    import pyfscache
    cache = pyfscache.FSCache('some/cache/directory',
                              days=13, hours=4, minutes=2.5)

    def uncached_doit(a, b, c):
      return [a, b, c]

    cached_doit = cache(uncached_doit)
