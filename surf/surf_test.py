#! /bin/python
# -*- coding: utf-8 -*-

import surf
import surf.namespace as ns
from rdflib import *

#f = open ("moodle.rdf", "w")

#g = Graph ()
#g.parse ("moodle.owl")

#for s,p,o in g: f.write ("%s\n%s\n%s\n\n" % (s.encode("utf-8"), p.encode("utf-8"), o.encode("utf-8")))

#f.close()

#ns.register (wines = "http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine#")

#c = session.get_class (ns.WINES + "VintageYear")
#r = c (ns.WINES + "Year1998")

#print r["yearValue"]#["http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine_YearValue"]

store = surf.Store(reader = "rdflib",writer = "rdflib",rdflib_store = "IOMemory")
store.load_triples(source = "moodle.owl")#"http://www.w3.org/People/Berners-Lee/card.rdf")
session = surf.Session(store)


print session.default_store.size()

ns.register (base = "http://www.semanticweb.org/ontologies/2011/10/Ontology1322456044761.owl")

s = "Форум"

c = session.get_class (ns.BASE + "Hot_Potatoes_Quiz")#s.encode('utf-8'))
print c.all().first()

print session.default_store.size()

store.close()





























