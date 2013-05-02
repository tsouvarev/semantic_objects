# -*- coding: utf-8 -*-


def memoize(f):

    cache = {}

    def inner(*args, **kwargs):

        key = args + tuple(kwargs.iteritems())

        if key not in cache:
            cache[key] = f(*args, **kwargs)
            print "new cache", key
        else:
            print "from cache", key

        return cache[key]

    return inner
