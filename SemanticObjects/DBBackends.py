#! /bin/python
# -*- coding: utf-8 -*-

from SPARQLWrapper import SPARQLWrapper, JSON, POST, SELECT
from urllib2 import urlopen, URLError
from urllib import urlencode


# общий интерфейс для различных хранилищ
class Backend(object):
    def query(self, query):
        raise NotImplementedError

    def ask(self, query):
        raise NotImplementedError

    def insert(self, query):
        raise NotImplementedError

    def update(self, query):
        raise NotImplementedError

    def delete(self, query):
        raise NotImplementedError


class AllegroBackend(Backend):

    def __init__(self, address):
        self.endpoint = SPARQLWrapper(address)

    def query(self, query):

        self.endpoint.setQuery(query)
        self.endpoint.setReturnFormat(JSON)
        results = self.endpoint.query().convert()

        return results

    def insert(self, query):

        self.endpoint.setQuery(query)
        self.endpoint.setMethod(POST)
        self.endpoint.setReturnFormat(JSON)
        self.endpoint.queryType = SELECT
        results = self.endpoint.query().convert()

        return results


class VirtuosoBackend(Backend):
    def __init__(self, address):
        self.endpoint = SPARQLWrapper(address + "/sparql/")

    def query(self, query):
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

        self.endpoint.setQuery(query)
        self.endpoint.setReturnFormat(JSON)
        results = self.endpoint.query().convert()

        return results

    def ask(self, query):

        self.endpoint.setQuery(query)
        self.endpoint.setReturnFormat(JSON)
        results = self.endpoint.query().convert()

        return results["boolean"]

    def insert(self, query):

        values = {"update": q}

        try:
            res = urlopen(self.address, urlencode(values))
        except URLError as e:
            raise Exception(e.reason)
        else:
            return res.read()

    def delete(self, query):

        values = {"update": query}

        try:
            res = urlopen(self.address, urlencode(values))
        except URLError as e:
            raise Exception(e.reason)

        else:
            return res.read()
