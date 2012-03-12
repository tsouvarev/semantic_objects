#! /bin/python
# -*- coding: utf-8 -*-

from SPARQLWrapper import SPARQLWrapper, JSON

class Backend (object):

	def query (self, q):
	
		pass

class SparqlBackend (Backend):

	def __init__ (self, address):
	
		self.address = address
		
		self.endpoint = SPARQLWrapper(address)
		
	# выполняет запрос, возвращает результат в виде почти прямого 
	# переноса XML/RDF на списки и объекты в Python
	def query (self, query):

		self.endpoint.setQuery(query)

		self.endpoint.setReturnFormat(JSON)
		results = self.endpoint.query().convert()

		return results
