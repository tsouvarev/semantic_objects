#! /bin/python
# -*- coding: utf-8 -*-

from SPARQLWrapper import SPARQLWrapper, JSON
from urllib import urlencode, urlopen
from httplib import HTTPConnection

class Backend (object):

	def query (self, query):
	
		raise Exception ("Not implemented")
	
	def insert (self, query):
	
		raise Exception ("Not implemented")
		
	def update (self, query):
	
		raise Exception ("Not implemented")
		
	def delete (self, query):
	
		raise Exception ("Not implemented")

class SparqlBackend (Backend):

	def __init__ (self, address):
	
		self.address = address
		
		self.endpoint = SPARQLWrapper(address+"/sparql/")
		
		self.conn = HTTPConnection(self.address)
	
	def __del__ (self):
	
		self.conn.close()
	
	# выполняет запрос, возвращает результат в виде почти прямого 
	# переноса XML/RDF на списки и объекты в Python
	def query (self, query):

		self.endpoint.setQuery(query)

		self.endpoint.setReturnFormat(JSON)
		results = self.endpoint.query().convert()

		return results
		
	def insert (self, q):
	
		values = {"update": q}
		headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
		
		self.conn.request("POST", "/update/", urlencode (values), headers)
		
		res = self.conn.getresponse()
				
		print res.read()		
	
	def delete (self, q):
	
		values = {"update": q}
		headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
		
		self.conn.request("POST", "/update/", urlencode (values), headers)
		
		res = self.conn.getresponse()
				
		print res.read()
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
