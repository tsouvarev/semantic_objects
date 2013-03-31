#! /bin/python
# -*- coding: utf-8 -*-

# from SPARQLWrapper import SPARQLWrapper, JSON, RDF, XML, TURTLE, N3
from urllib2 import urlopen, URLError
from urllib import urlencode


class Backend(object):
    def query(self, query):
        raise NotImplementedError("Method '%s' was not implemented for '%s'" % ("query", self.__class__.__name__))

    def ask(self, query):
        raise NotImplementedError("Method '%s' was not implemented for '%s'" % ("ask", self.__class__.__name__))

    def insert(self, query):
        raise NotImplementedError("Method '%s' was not implemented for '%s'" % ("insert", self.__class__.__name__))

    def update(self, query):
        raise NotImplementedError("Method '%s' was not implemented for '%s'" % ("update", self.__class__.__name__))

    def delete(self, query):
        raise NotImplementedError("Method '%s' was not implemented for '%s'" % ("delete", self.__class__.__name__))


class AllegroBackend(Backend):

    def __init__(self, address):
        self.endpoint = SPARQLWrapper(address)

    def query(self, query):
        self.endpoint.setQuery(query)

        self.endpoint.setReturnFormat(JSON)
        results = self.endpoint.query().convert()

        return results


class VirtuosoBackend(Backend):

    def __init__(self, address):
        self.endpoint = SPARQLWrapper(address + "/sparql/")

    def query(self, query):
        super(VirtuosoBackend, self).query(query)

        self.endpoint.setQuery(query)

        self.endpoint.setReturnFormat(JSON)
        results = self.endpoint.query().convert()

        return results


class FourstoreSparqlBackend(Backend):
    def __init__(self, address):

        self.address = address + "/update/"
        self.endpoint = SPARQLWrapper(address + "/sparql/")

    # выполняет запрос, возвращает результат в виде почти прямого
    # переноса XML/RDF на списки и словари в Python
    def query(self, query):

        super(FourstoreSparqlBackend, self).query(query)

        self.endpoint.setQuery(query)
        self.endpoint.setReturnFormat(JSON)
        results = self.endpoint.query().convert()

        return results

    def ask(self, query):

        super(FourstoreSparqlBackend, self).ask(query)

        self.endpoint.setQuery(query)
        self.endpoint.setReturnFormat(JSON)
        results = self.endpoint.query().convert()

        return results["boolean"]

    def insert(self, query):

        super(FourstoreSparqlBackend, self).insert(query)

        values = {"update": q}
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

        try:
            res = urlopen(self.address, urlencode(values))
        except URLError, e:

            raise Exception(e.reason)
        else:
            return res.read()

    def delete(self, query):

        super(FourstoreSparqlBackend, self).delete(query)

        values = {"update": query}
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

        try:
            res = urlopen(self.address, urlencode(values))
        except URLError, e:

            print e.reason
            return False

        else:
            return res.read()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
