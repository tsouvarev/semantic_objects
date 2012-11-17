#! /bin/python
# -*- coding: utf-8 -*-

import SPARQLWrapper as wrap
from DBBackends import FourstoreSparqlBackend
from Connection import Connection
from QueryResultParser import convert

class Class ():

    def __init__ (self, uri):

        self.uri = uri


class Resource ():

    def __init__ (self, *args, **kwargs):

        raise Exception ("You cannot instantiate resource")


# Класс, отображающий RDF-триплеты в объекты Python
class SemanticObjects ():

    def __init__ (self, connection, queries):

        # запоминаем SPARQL-endpoint
        self.conn = connection

        self.ns = {}
        self.ns["owl"] = "http://www.w3.org/2002/07/owl#"
        self.ns["rdf"] = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
        self.ns["rdfs"] =  "http://www.w3.org/2000/01/rdf-schema#"

        self.prefixes = "\n".join (["prefix %s: <%s>" % (k, self.ns[k]) for k in self.ns])

        # список базовых классов, понадобится при запросах классов и ресурсов из хранилища
        # также играет роль кэша классов
        self.classes = {}
        self.superclasses = {}

    def get_resources(self, uri):

