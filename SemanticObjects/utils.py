# -*- coding: utf-8 -*-

# one ring to rule them all
cache = {}


def memoize(f):

    def inner(*args, **kwargs):

        key = args[1:] + tuple(kwargs.iteritems())

        if key not in cache:
            cache[key] = f(*args, **kwargs)

        return cache[key]

    return inner
