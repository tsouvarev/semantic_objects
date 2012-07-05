# -*- coding: utf-8 -*-
from collections import defaultdict
from rdflib import Literal

from rdflib.namespace import OWL, RDF, RDFS, split_uri
from RDFSQueries import RDFSQueries
from one.SemanticObjects.utils import memoize


class Property(object):

    def __init__(self, factory, property_raw):

        self.name = property_raw["prop"]["value"]
        self.value = property_raw["val"]["value"]
        self.type = property_raw["val"]["type"]
        self.lang = property_raw["val"].get("xml:lang")
        self.datatype = property_raw["val"].get("datatype")
        self.factory = factory

    def to_python(self):

        if self.type == "uri":
            if self.factory.query.is_class(self.value):
                val = self.factory.get_class(self.value)
            elif self.factory.query.is_object(self.value):
                val = self.factory.get_object(self.value)
            # если не объект и не класс, то свойство
            else:
                val = None
        elif self.type in ["literal", "literal-typed"]:
            val = Literal(self.value, datatype=self.datatype, lang=self.lang).toPython()

        return val


class Thing(object):

    def __init__(self, uri):
        if not self.factory.query.exists(uri):
            if not self.factory.query.create_object(uri, self.__class__.uri):
                raise Exception("Could not create such object")

        self.uri = unicode(uri)

    @classmethod
    def get_objects(cls):

        objects = cls.factory.query.all_resources(cls.uri)
        return [cls(x) for x in objects]

    @classmethod
    def filter(cls, *args, **kwargs):
        if args:
            assert isinstance(args[0], dict)
            kwargs.update(args[0])

        objects = cls.factory.query.get_class_objects_by_attr_value(cls.uri, **kwargs)
        return [cls(x) for x in objects]

    @classmethod
    def get_subclasses(cls):
        results = cls.factory.query.get_subclasses_of_class(cls.uri)

        return [cls.factory.get_class(x) for x in results]

    def __repr__(self):
        return "object " + split_uri(self.uri)[1]

    def __getattr__(self, item):

        if not self.factory.query.has_attr(self.uri, item):
            return None

        if item not in self.properties:
            return None

        if item == unicode(RDFS.label):
            return {x.lang: x.to_python() for x in self.properties[item]}

        return [x.to_python() for x in self.properties[item]]


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

    @memoize
    def get_class(self, class_uri):

        if self.query.is_class(class_uri):

            base_class_uris = self.query.get_base_classes(class_uri)
            if base_class_uris:
                base_classes = [self.get_class(cl) for cl in base_class_uris]
            else:
                base_classes = [Thing]

            properties = self.query.available_class_properties(class_uri)

            p = defaultdict(list)
            for prop in properties:
                p[prop["prop"]["value"]].append(Property(self, prop))

            namespace, classname = split_uri(unicode(class_uri))

            kwargs = {
                "uri": class_uri,
                "factory": self,
                "properties": p,
            }

            cl = type(str(classname), tuple(base_classes), kwargs)

            return cl
        # нет такого класса? создадим!
        else:
            if self.query.create_class(class_uri):
                return self.get_class(class_uri)
            else:
                return None

    @memoize
    def get_object(self, obj_uri):

        if self.query.is_object(obj_uri):
            parent_class = self.query.get_parent_class(obj_uri)
            cl = self.get_class(parent_class)

            obj = cl(obj_uri)

            raw_properties = self.query.available_object_properties(obj_uri)

            p = defaultdict(list)
            for property in raw_properties:
                p[property["prop"]["value"]].append(Property(self, property))
            obj.properties = p

            return obj

        return None

