#! /bin/python
# -*- coding: utf-8 -*-

#import SPARQLWrapper as wrap
from DBBackends import *

class Connection ():

    def __init__ (self, backend):
    
        if not isinstance (backend, Backend): raise Exception ("Given wrong backend for connection: %s" % backend)

        self.db = backend

    def query (self, query):

#        print "q"
        return self.db.query (query)

    def insert (self, query):
    
        return self.db.insert (query)
        
    def delete (self, query):
    
        return self.db.delete (query)






















































