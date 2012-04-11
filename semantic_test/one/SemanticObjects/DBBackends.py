#! /bin/python
# -*- coding: utf-8 -*-

from SPARQLWrapper import SPARQLWrapper, JSON
from urllib2 import urlopen, HTTPError
from urllib import urlencode
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

		self.endpoint.setQuery(query)

		self.endpoint.setReturnFormat(JSON)
		results = self.endpoint.query().convert()

		return results
		
	def insert (self, q):
	
		values = {"update": q}
		headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
		
		try: res = urlopen (self.address, urlencode (values))
		except URLError, e: 
			
			raise Exception (e.reason)
		else:
			return res.read()
	
	
	def delete (self, q):
	
		values = {"update": q}
		headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
		
		try: res = urlopen (self.address, urlencode (values))
		except URLError, e: 
			
			print e.reason
			return False
		else:
			return res.read()
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
