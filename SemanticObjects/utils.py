# -*- coding: utf-8 -*-

# one ring to rule them all
from pprint import pformat
from django.utils.html import escape

cache = {}


def memoize(f):

    def inner(*args, **kwargs):

        key = args[1:] + tuple(kwargs.iteritems())

        if key not in cache:
            cache[key] = f(*args, **kwargs)

        return cache[key]

    return inner


def get_results(results, for_html=False, do_print=False):
    res = ""

    res += pformat(results)

    if for_html:
        res = "<pre>" + escape(res) + "</pre>"

    return res