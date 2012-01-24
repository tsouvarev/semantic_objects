#! /bin/python
# -*- coding: utf-8 -*-

import surf
import surf.namespace as ns
from rdflib import *
import SPARQLWrapper as wrap
from SPARQLWrapper import SPARQLWrapper, JSON

#f = open ("moodle.rdf", "w")

#g = Graph ()
#g.parse ("moodle.owl")

#for s,p,o in g: f.write ("%s\n%s\n%s\n\n" % (s.encode("utf-8"), p.encode("utf-8"), o.encode("utf-8")))

#f.close()

#ns.register (wines = "http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine#")

#c = session.get_class (ns.WINES + "VintageYear")
#r = c (ns.WINES + "Year1998")

#print r["yearValue"]#["http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine_YearValue"]

#store = surf.Store(reader = "rdflib",writer = "rdflib",rdflib_store = "IOMemory")
#store = surf.Store(reader = 'sparql_protocol',
#					writer = 'sparql_protocol',
#                   endpoint = 'http://fourstore.avalon.ru:80/sparql'
#                   #default_graph = 'wine'
#                   )

#store.load_triples()
#store.load_triples(source = "moodle.owl")#"http://www.w3.org/People/Berners-Lee/card.rdf")
#session = surf.Session(store)
#q = session.default_store.execute_sparql("SELECT ?s ?p ?o WHERE { ?s ?p ?o }")

#print list(q)#session.default_store.size()

#ns.register (wine = "http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine#")

#c = session.get_class (ns.WINE + "Wine")#s.encode('utf-8'))
#print c.all().first()

#print session.default_store.size()

#store.close()

##########sparql = SPARQLWrapper("http://dbpedia.org/sparql")
##########sparql.setQuery("""
##########    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
##########    SELECT ?label
##########    WHERE { <http://dbpedia.org/resource/Asturias> rdfs:label ?label }
##########""")
##########sparql.setReturnFormat(JSON)
##########results = sparql.query().convert()

##########for result in results["results"]["bindings"]:
##########    print result["label"]["value"].encode ("utf-8")

#wget fourstore.avalon.ru/sparql --post-data 'query=SELECT+%2A+WHERE+%7B+%3Fs+%3Fp+%3Fo+%7D'

sparql = SPARQLWrapper("http://fourstore.avalon.ru:80/sparql") # fourstore.avalon.ru:80
sparql.setQuery("SELECT * WHERE { ?s ?p ?o }")
sparql.setReturnFormat(JSON)
results = sparql.query()

print results

for result in results:#["results"]["bindings"]:
    print result#["s"]["value"].encode ("utf-8")


























