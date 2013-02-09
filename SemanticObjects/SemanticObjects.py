# -*- coding: utf-8 -*-

import SPARQLWrapper as wrap
from rdflib import URIRef
from DBBackends import FourstoreSparqlBackend
from Connection import Connection
from QueryResultParser import convert
from rdflib.namespace import Namespace, split_uri, OWL, RDF, RDFS
from Queries import RDFSQueries

class PropertyResolver(object):

    def __init__(self, conn, queries, prop_uri, resource_uri, class_uri):
        self.uri = prop_uri
        self.resource_uri = resource_uri
        self.class_uri = class_uri
        self.conn = conn
        self.queries = queries

    def __get__(self, obj, type=None):
        print 111111
        q = self.queries.get_property_value(self.uri, obj.uri)
        return convert(self.conn.query(q), (("value", ["val"]), ))["value"]

    def __set__(self, obj, value):
        pass

    def __delete__(self, obj):
        pass


class Thing(object):

    def __init__(self, resource_uri):
        self.uri = resource_uri
        self.parent_class_loaded = False
        self.properties_loaded = False
        self.conn = self.__class__.conn

        q = self.queries.get_available_properties(self.__class__.uri)
        properties = convert(self.conn.query(q), (("prop", ["prop"]),))["prop"]

        for prop in properties:
            namespace, name = split_uri(prop)
            setattr(self, name, None)

#    def __getattribute__(self, item):
#
#        q = self.queries.get_property_value(item)
#        return convert(self.conn.query(q), (("value", ["val"]), ))["value"]

    def __get_property_value(self, resource_uri, prop_uri):
        q = self.queries.get_property_value(prop_uri, resource_uri)
        return convert(self.conn.query(q), (("value", ["val"]), ))["value"][0]


    @classmethod
    def all(cls):
        q = cls.queries.get_resources(cls.uri)

        return [cls(uri)
                for uri in convert(cls.conn.query(q), (("resources", ["cl"]),))["resources"]]

class RDFSClass(object):

    def __init__(self, connection, lang = None):

        # запоминаем SPARQL-endpoint
        self.conn = connection
        if lang is not None:
            self.queries = {"rdfs": RDFSQueries}[lang]
        else:
            self.queries = None


        # список базовых классов, понадобится при запросах классов и ресурсов из хранилища
        # также играет роль кэша классов
        self.classes = {}
        self.superclasses = {}


    def get(self, uri):
        namespace, name = split_uri(uri)
        q = self.queries.is_class(uri)
        is_class = self.conn.ask(q)

        if is_class:
            return type(str(name), (Thing,), {"uri": uri, "conn": self.conn, "queries": self.queries})
        else:
            raise Exception("URI not for class")



