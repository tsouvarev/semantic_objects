#! /bin/python
# -*- coding: utf-8 -*-

from SPARQLWrapper import SPARQLWrapper, JSON

class Backend (object):

	def query (self, q):
	
		pass

class FourStoreBackend (Backend):

	def __init__ (self, address):
	
		self.address = address
		
		self.sparql = SPARQLWrapper(address)
		
	# выполняет запрос, возвращает результат в виде почти прямого 
	# переноса XML/RDF на списки и объекты в Python
	def query (self, query):

		self.sparql.setQuery(query)

		self.sparql.setReturnFormat(JSON)
		results = self.sparql.query().convert()

		return results
