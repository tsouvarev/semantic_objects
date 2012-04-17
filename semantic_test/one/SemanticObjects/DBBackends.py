#! /bin/python
# -*- coding: utf-8 -*-

from SPARQLWrapper import SPARQLWrapper, JSON
from urllib2 import urlopen, HTTPError
from urllib import urlencode
from abc import abstractmethod as abstract

class Backend (object):

    @abstract
    def query (self, query): return
    
    @abstract
    def insert (self, query): return

    @abstract
    def update (self, query): return    

    @abstract
    def delete (self, query): return


class FourstoreSparqlBackend (Backend):

    def __init__ (self, address):
    
        self.address = address + "/update/"
        
        self.endpoint = SPARQLWrapper(address+"/sparql/")
        
        #self.conn = urlopen (addr)#HTTPConnection(self.address)
        
    def __del__ (self):
    
        pass#self.conn.close()
    
    # выполняет запрос, возвращает результат в виде почти прямого 
    # переноса XML/RDF на списки и объекты в Python
    def query (self, query):

        super(FourstoreSparqlBackend, self).query(query)

        self.endpoint.setQuery(query)

        self.endpoint.setReturnFormat(JSON)
        results = self.endpoint.query().convert()

        return results
        
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
    
        values = {"update": q}
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        
        try: res = urlopen (self.address, urlencode (values))
        except URLError, e: 
            
            print e.reason
            return False
        
        else:
            return res.read()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
