#! /bin/python
# -*- coding: utf-8 -*-

import SPARQLWrapper as wrap
from SPARQLWrapper import SPARQLWrapper, JSON
import re

class QueryResult ():

	def __init__ (self, uri):

		self.uri = uri

class SemanticObjects ():

	def __init__ (self, addr):

		self.sparql = SPARQLWrapper(addr)
		self.prefixes = ""
		self.ns = {}
		self.namespaces = self.ns
		
		self.bases = {}

		self.ns["owl"] = "http://www.w3.org/2002/07/owl#"
		self.ns["rdfs"] = "http://www.w3.org/2000/01/rdf-schema#"
		self.ns["rdf"] = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"

		for ns in self.ns: self.prefixes += "PREFIX %s: <%s>\n" % (ns, self.ns[ns])

	def get_query (self, query):

		self.sparql.setQuery(self.prefixes + query)

		self.sparql.setReturnFormat(JSON)
		results = self.sparql.query().convert()

		return results

	def print_results (self, results):

		print results

		for result in results["results"]["bindings"]:

			for i in results["head"]["vars"]: print "%s: %s" % (i, result[i]["value"])
			print

	def add_namespace (self, name, namespace):

		self.namespaces[name] = namespace
		self.prefixes += "PREFIX %s: <%s>\n" % (name, namespace)

	def convert (self, properties, schema):

		c = {}

		for name,val in schema:

			if type(val) == str:

				i,j = name,val

#				if i in properties["head"]["vars"] and \
#					j in properties["head"]["vars"]:

				for prop in properties["results"]["bindings"]:

					p = prop[i]
					v = prop[j]

					if p["type"] != "bnode" and v["type"] != "bnode":

						p = p["value"].rsplit ("#")[1]
						v = v["value"].rsplit ("#")[1]
						c[p] = v

			elif type(val) == list:

				c[name] = []

				for p in properties["results"]["bindings"]:

					for n in val:

						if p[n]["type"] != "bnode": c[name].append (p[n]["value"].rsplit("#")[1])

		return c

	def get_class (self, uri):

		t = uri.rsplit ("#")
		name = t[1] if len (t) > 1 else uri.rsplit (":")[1]

		props = {}
		
#		{ 
#							%s a owl:Class ; 
#							?prop ?val
#							FILTER (?prop != rdf:type && 
#									?prop != rdfs:subClassOf)
#						}
						
		queries = ["""
					select ?prop ?val
					where 
					{
						{ 
							%s a owl:Class ; 
							?rel ?sub . 
							?sub owl:onProperty	?prop ;
						 		 owl:hasValue ?val
						}
						union
						{					
							%s a owl:Class ;
							owl:intersectionOf (?f [ owl:onProperty ?prop; owl:hasValue ?val])
						}						
					}
					""" % ((uri,)*2)
					]
					
		for q in queries: 
			#print self.print_results (self.get_query (q))
			props.update (self.convert (self.get_query (q), [("prop", "val",)]))
		
		q = """
				select ?class 
				where 
				{ 
					{
						%s a owl:Class ; 
						rdfs:subClassOf ?class .
						?class a owl:Class
					}
					union
					{					
						%s a owl:Class ;
						owl:intersectionOf (?class [ owl:onProperty ?prop; owl:hasValue ?val]) .
						?class a owl:Class
					}
					union
					{
						%s a owl:Class ;
						owl:intersectionOf ( ?class ?x ) .
						?class a owl:Class .
						?x a owl:Class
					}												
					union
					{
						%s a owl:Class ;
						owl:intersectionOf ( ?x ?class ) .
						?class a owl:Class .
						?x a owl:Class
					}
				}""" % ((uri,)*4)
		
#		print uri
#		self.print_results (self.get_query (q))
		
#		print 
		
		for i in self.convert (self.get_query (q), [("classes", ["class"], )])["classes"]: 
			
			if i not in self.bases:
			
				self.bases[i] = self.get_class ("wines:" + i)
		
		r = type (str(name), tuple (self.bases.values()), props)
		r.uri = uri
		
 		r.__repr__ = lambda self: u"" + self.uri
 		
#		print
#		print r
#		print cd dir(r)
#		print r.__mro__
#		print r.__dict__

#			
		return r
	
	def get_resources (self, class_uri):

		t = self.get_class (class_uri)
				
		q = """
				select ?inst
				where
				{
					?inst a %s
				}
			""" % ((class_uri,)*1)
		
		instances = self.convert (self.get_query (q), [("inst", ["inst"], )])["inst"]
		
		res = []
		
		for inst in instances:
		
			i = t()
			i.uri = inst
			res.append (i)
			
		return res

	def get_resource (self, uri):
	
		q = """
				select ?type
				where
				{
					%s a ?type
				}
			""" % uri
			
		type_name = self.convert (self.get_query (q), [("type", ["type"])])["type"][0]
		
		t = self.get_class ("wines:" + str(type_name))
		
		q = """
				select *
				where
				{
					%s ?p ?o .
					FILTER (?p != rdf:type)
				}
			""" % uri
		
		r = t()
		
		query = self.convert (self.get_query (q), [("p", "o", )])
		
		for i in query: r.__dict__[i] = query[i]
			
		return r
	
	def test (self):
	
		self.add_namespace ("wines", "http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine#")
		
		r = self.get_resources ("wines:Chianti")
		for rr in r: print rr.uri
			

						
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
