#! /bin/python
# -*- coding: utf-8 -*-

import surf
import surf.namespace as ns
from rdflib import *
import SPARQLWrapper as wrap
from SPARQLWrapper import SPARQLWrapper, JSON
from surf.rdf import URIRef
#from SPARQLWrapper.Wrapper import POST

#f = open ("moodle.rdf", "w")

#g = Graph ()
#g.parse ("moodle.owl")

#for s,p,o in g: f.write ("%s\n%s\n%s\n\n" % (s.encode("utf-8"), p.encode("utf-8"), o.encode("utf-8")))

#f.close()

store = surf.Store(	reader = 'sparql_protocol',
			writer = 'sparql_protocol',
                   	endpoint = 'http://fourstore.avalon.ru/sparql/'
                   	)

ns.register (wines = "http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine#")
session = surf.Session(store)

#q = session.default_store.add_triple(*map (URIRef, ("http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine#Test",
#									  "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
#									  "http://www.w3.org/2002/07/owl#Class")))
# q = session.default_store.add_triple(*map (URIRef, ("WINES:Test", "RDF:type", "OWL:Class")))
#"""
#INSERT DATA 
#{ <http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine#Test> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#Class> }""")# % (ns.WINES + "Chianti"))

#print q#["results"]["bindings"]

#for r in q["results"]["bindings"]: print r["s"]["value"]

c = session.get_class (ns.WINES + "Burgundy")
#for i in c.all(): print i

r = session.get_resource (ns.WINES+"WhiteBurgundy", c)
#r.load()
#r.hasSugar = "Yes"
#print r.hasSugar
#r.save ()
r.remove()

#for rr in r.rdfs_subClassOf: 

#	rr.load()
#	print rr.__dict__

#years = session.get_class(ns.WINES+ "VintageYear")
#years_insts = years.all()
#print 'all years'
#for y in years_insts: print y
#print 'first year'
#fy = years_insts.order().first()
#print fy
#print 'years count: %s' % len(years_insts)
#print 'test get_by'
#print fy.wines_yearValue
#print len(years.filter(wines_yearValue = "1998"))

























