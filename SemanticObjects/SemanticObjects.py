#! /bin/python
# -*- coding: utf-8 -*-

import SPARQLWrapper as wrap
from SPARQLWrapper import SPARQLWrapper, JSON

class QueryResult ():

	def __init__ (self, uri):
	
		self.uri = uri

class SemanticObjects ():

	def __init__ (self, addr):
	
		self.sparql = SPARQLWrapper(addr)
		self.prefixes = ""
		self.ns = {}
		self.namespaces = self.ns
		
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
				
		for result in results["results"]["bindings"]:
		
			for i in results["head"]["vars"]: print "%s: %s" % (i, result[i]["value"])
			print
	
	def add_namespace (self, name, namespace):
	
		self.namespaces[name] = namespace
		self.prefixes += "PREFIX %s: <%s>\n" % (name, namespace)
	
	def convert (self, properties):
	
		c = {}
		
		if "prop" in properties["head"]["vars"] and \
			"val" in properties["head"]["vars"]:
		
			for prop in properties["results"]["bindings"]:
			
				p = prop["prop"]
				v = prop["val"]
			
				if p["type"] != "bnode" and v["type"] != "bnode":
			
					p = p["value"].rsplit ("#")[1]
					v = v["value"].rsplit ("#")[1]
					c[p] = v
		
		elif "class" in properties["head"]["vars"]:
		
			c["classes"] = []
			print properties["results"]["bindings"]
			
			for p in properties["results"]["bindings"]:
			
				if p["class"]["type"] != "bnode":
				
					c["classes"].append (p["class"]["value"].rsplit("#")[1])
		
		return c
	
	def get_class (self, uri):
		
		t = uri.rsplit ("#")
		name = t[1] if len (t) > 1 else uri.rsplit (":")[1]
		
		c = {}
		
		queries = [
					"""	
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
							?prop ?val
							FILTER (?prop != rdf:type && 
									?prop != rdfs:subClassOf)
						}
						union
						{ 
							%s a owl:Class ;
							owl:intersectionOf (?f ?ff ?r) .
							?r owl:onProperty ?prop ;
							owl:hasValue ?val
						}
					}
					""" % ((uri,)*3)
					]
					
		for q in queries: 
			print self.print_results (self.get_query (q))
			c.update (self.convert (self.get_query (q)))
		
		q = """
				select *
				where 
				{ 
					%s a owl:Class ; 
					rdfs:subClassOf ?class
				}""" % uri
		
		c.update (self.convert (self.get_query (q)))
		
		return type (name, (), c) #tuple (c["classes"]) нужно, чтобы все базовые классы были уже созданы
		# видимо, нужен рекурсивный обход
	
	def test (self):
	
		self.add_namespace ("wines", "http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine#")
		
		r = self.get_class ("wines:Chianti")
		
		#self.print_results (r)
		print r, r.__dict__
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
