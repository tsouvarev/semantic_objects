# -*- coding: utf-8 -*-

from rdflib.namespace import OWL, RDF, RDFS, split_uri
from RDFSQueries import RDFSQueries


class Thing(object):

    def __init__(self, uri):
        self.uri = unicode(uri)

    @classmethod
    def get_objects(cls):

        objects = cls.query.all_resources(cls.uri)
        return [cls(x) for x in objects]

    @classmethod
    def filter(cls, *args, **kwargs):
        if args:
            assert isinstance(args[0], dict)
            kwargs.update(args[0])

        objects = cls.query.get_objects_by_attr_value(cls.uri, **kwargs)
        return [cls(x) for x in objects]

    def __repr__(self):
        return split_uri(self.uri)[1]

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

    def get_class(self, class_uri, check_class=True):

        if not check_class or self.query.is_class(class_uri):

            base_class_uris = self.query.get_base_classes(class_uri)
            if base_class_uris:
                base_classes = [self.get_class(cl, check_class=False) for cl in base_class_uris]
            else:
                base_classes = [Thing]

            properties = self.query.available_class_properties(class_uri)

            namespace, classname = split_uri(unicode(class_uri))

            kwargs = {
                "uri": class_uri,
                "query": self.query,
                "properties": properties,
                "prefixes": self.prefixes,
            }

            cl = type(str(classname), tuple(base_classes), kwargs)

            return cl

        return None

    def get_object(self, obj_uri):

        if self.query.is_object(obj_uri):
            cl = self.get_class(self.query.get_parent_class(obj_uri))

            obj = cl(obj_uri)
            obj.properties = self.query.available_object_properties(obj_uri)

            return obj
        return None

