# -*- coding: utf-8 -*-


def memoize(f):

    cache = {}

    def inner(*args, **kwargs):

        key = args + tuple(kwargs.iteritems())

        if key not in cache:
            cache[key] = f(*args, **kwargs)

        return cache[key]

    return inner
