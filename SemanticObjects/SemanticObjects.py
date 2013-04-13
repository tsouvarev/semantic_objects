# -*- coding: utf-8 -*-

from rdflib.namespace import OWL, RDF, RDFS, split_uri
from RDFSQueries import RDFSQueries


class Thing(object):

    def __init__(self, uri):
        self.uri = uri

    @classmethod
    def get_objects(cls):

        resources = cls.query.all_resources(cls.uri)
        return [cls(x) for x in resources]

    def filter(self, **kwargs):
        objects = self.query.get_objects_by_attr_value(**kwargs)
        return objects

    def __getattr__(self, item):

        if not self.query.has_attr(self.uri, item):
            raise AttributeError("Object '%s' has no attribute '%s'" % (self.uri, item))

        return self.query.get_attr(self.uri, item)


class Factory(object):

    def __init__(self, connection, language="RDFS"):

        self.prefixes = {
            "owl": OWL,
            "rdf": RDF,
            "rdfs": RDFS,
        }

        if language == "RDFS":
            self.query = RDFSQueries(connection, self.prefixes)

    def all(self):
        return self.query.all()

    def add_namespace(self, **kwargs):

        for k, v in kwargs.iteritems():
            self.prefixes[k] = v.rstrip("#") + "#"

    def get_class(self, class_uri):

        if self.query.is_class(class_uri):
            properties = self.query.available_properties(class_uri)

            namespace, classname = split_uri(unicode(class_uri))

            kwargs = {
                "uri": class_uri,
                "query": self.query,
                "properties": properties,
                "prefixes": self.prefixes,
            }

            print "properties", properties

            # for prop in properties:
            #     # namespace, prop = split_uri(unicode(prop))
            #     kwargs[prop] = None

            cl = type(str(classname), (Thing,), kwargs)

            return cl

        return None
