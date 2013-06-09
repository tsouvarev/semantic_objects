# -*- coding: utf-8 -*-

from pprint import pformat
from django.utils.html import escape
from rdflib.term import XSDToPython, URIRef, _XSD_PFX


cache = {} #dict(XSDToPython)


def memoize(f):

    def inner(self, uri):

        uri = URIRef(uri)
        
        if uri not in cache:
            cache[uri] = f(self, uri)

        return cache[uri]

    return inner


def get_results(results, for_html=False):
    res = ""

    res += pformat(results)

    if for_html:
        res = "<pre>" + escape(res) + "</pre>"

    return res