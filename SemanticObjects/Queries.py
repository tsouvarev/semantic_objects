# -*- coding: utf-8 -*-
from rdflib import OWL, RDF, RDFS

class Query(object):

    def get_classes(self):
        pass

    def get_properties(self):
        pass

    def get_objects(self):
        pass

class RDFSQueries(object):

    @staticmethod
    def prefixes():
        ns = {
            "owl": OWL,
            "rdf": RDF,
            "rdfs": RDFS
        }

        return "\n".join(["prefix %s: <%s>" % (k, ns[k]) for k in ns])+"\n"

    @staticmethod
    def is_class(uri):
        q = "ask where {<%(uri)s> a rdfs:Class }" % {"uri": uri}
        return RDFSQueries.prefixes()+q

    @staticmethod
    def get_available_properties(parent_uri):
        q = "select * "\
            "where { "\
            "?prop rdfs:domain <%(parent)s> ."\
                "{ ?prop a owl:ObjectProperty . } "\
                "union "\
                "{ ?prop a owl:DatatypeProperty . }"\
            "}" % {"parent": parent_uri}
        return RDFSQueries.prefixes()+q

    @staticmethod
    def get_resources(class_uri):
        q = "select * "\
            "where { "\
            "?cl a <%(type)s>"\
            "}" % {"type": class_uri}
        return RDFSQueries.prefixes()+q

    @staticmethod
    def get_property_value(property_uri, resource_uri):
        q = "select * " \
            "where { " \
            "<%(res_uri)s> <%(prop_uri)s> ?val" \
            "}" % {"res_uri": resource_uri, "prop_uri": property_uri}
        return RDFSQueries.prefixes()+q

class OWLQuery(Query):
    pass