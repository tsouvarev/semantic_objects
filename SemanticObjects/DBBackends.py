#! /bin/python
# -*- coding: utf-8 -*-

from SPARQLWrapper import SPARQLWrapper, JSON, RDF, XML, TURTLE, N3
from urllib2 import urlopen, HTTPError, URLError
from urllib import urlencode
from abc import abstractmethod as abstract

class Backend(object):

    @abstract
    def query(self, query):
        return

    @abstract
    def ask(self, query):
        return
    
    @abstract
    def insert(self, query):
        return

    @abstract
    def update(self, query):
        return

    @abstract
    def delete(self, query):
        return

class VirtuosoBackend(Backend):

    def __init__(self, address):

        self.endpoint = SPARQLWrapper(address+"/sparql/")

    def query(self, query):
        super(VirtuosoBackend, self).query(query)

        self.endpoint.setQuery(query)

        self.endpoint.setReturnFormat(JSON)
        results = self.endpoint.query().convert()

        return results


class FourstoreSparqlBackend(Backend):

    def __init__(self, address):
    
        self.address = address + "/update/"
        self.endpoint = SPARQLWrapper(address+"/sparql/")
        
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
        
    def insert (self, query):

        super(FourstoreSparqlBackend, self).insert(query)

        values = {"update": q}
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        
        try: res = urlopen (self.address, urlencode (values))
        except URLError, e: 
            
            raise Exception (e.reason)
        else:
            return res.read()
    
    
    def delete (self, query):

        super(FourstoreSparqlBackend, self).delete (query)
    
        values = {"update": query}
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        
        try: res = urlopen (self.address, urlencode (values))
        except URLError, e: 
            
            print e.reason
            return False
        
        else:
            return res.read()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
