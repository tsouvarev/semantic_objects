# -*- coding: utf-8 -*-
from collections import defaultdict, namedtuple
from rdflib import Literal, URIRef

from rdflib.namespace import OWL, RDF, RDFS, split_uri
from RDFSQueries import RDFSQueries
from utils import cache, memoize


class ClassCreator(type):

    def __repr__(cls):
        return "class " + split_uri(cls.uri)[1]

    def __new__(cls, name, bases, dict):

        factory = dict["factory"]
        uri = URIRef(dict["uri"])

        klass = type.__new__(cls, name, bases, dict)

        cache[uri] = klass

        klass.factory = factory

        p = factory.get_properties(uri, mode="class")

        for property in p:
            for x in p[property]:
                cl = factory.get_class(URIRef(x["prop_type"]["value"]))
                setattr(klass, URIRef(property), cl)

        return klass


class Thing(object):

    def __init__(self, uri):
        if not self.factory.query.exists(uri):
            if not self.factory.query.create_object(uri, self.__class__.uri):
                raise Exception("Could not create such object")

        self.uri = URIRef(uri)

    @classmethod
    def get_objects(cls):

        objects = cls.factory.query.all_resources(cls.uri)
        return [cls.factory.get_object(x) for x in objects]

    @classmethod
    def filter(cls, *args, **kwargs):
        if args:
            assert isinstance(args[0], dict)
            kwargs.update(args[0])

        objects = cls.factory.query.get_class_objects_by_attr_value(cls.uri, **kwargs)
        return [cls.factory.get_object(x) for x in objects]

    @classmethod
    def get_subclasses(cls):
        results = cls.factory.query.get_subclasses_of_class(cls.uri)

        return [cls.factory.get_class(x) for x in results]

    def __repr__(self):
        return "object " + split_uri(self.uri)[1]

    def __eq__(self, other):
        return self.uri == other.uri


class Factory(object):

    def __init__(self, connection, language="RDFS"):

        # so fucking bad.. or sad? well, it's too much for me to decide
        Thing.factory = self

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

    def get_properties(self, uri, mode):

        uri = URIRef(uri)

        if mode == "object":
            raw_properties = self.query.available_object_properties(uri)
        elif mode == "class":
            raw_properties = self.query.available_class_properties(uri)

        p = defaultdict(list)
        for property in raw_properties:
            p[property["prop"]["value"]].append(property)

        return p

    @memoize
    def get_class(self, class_uri):

        class_uri = URIRef(class_uri)

        if self.query.is_class(class_uri):

            base_class_uris = self.query.get_base_classes(class_uri)
            if base_class_uris:
                base_classes = [self.get_class(cl) for cl in base_class_uris]
            else:
                base_classes = [Thing]

            namespace, classname = split_uri(unicode(class_uri))

            cl = ClassCreator(str(classname), tuple(base_classes),
                              {
                                  "uri": class_uri,
                                  "factory": self,
                              })

            return cl
        # нет такого класса? создадим!
        else:
            if self.query.create_class(class_uri):
                return self.get_class(class_uri)
            else:
                return None

    @memoize
    def get_object(self, obj_uri):

        obj_uri = URIRef(obj_uri)

        if self.query.is_object(obj_uri):
            parent_class = self.query.get_parent_class(obj_uri)
            if parent_class is None:
                cl = Thing
            else:
                cl = self.get_class(parent_class)

            obj = cl(obj_uri)
            cache[obj_uri] = obj

            raw_properties = self.get_properties(obj.uri, mode="object")

            for key, values in raw_properties.items():
                res = []

                for value in values:
                    uri = URIRef(value["val"]["value"])
                    if value["val"]["type"] == "uri":
                        if self.query.is_object(uri):
                            val = self.get_object(uri)
                        elif self.query.is_class(uri):
                            val = self.get_class(uri)
                    elif value["val"]["type"] == "literal":  # plain literal
                        v = value["val"]["value"]
                        l = value["val"].get("xml:lang", "en")
                        val = Literal(v, lang=l)
                    elif value["val"]["type"] == "literal-typed":  # typed literal
                        v = value["val"]["value"]
                        d = value["val"].get("datatype")
                        val = Literal(v, datatype=d).toPython()

                    res.append(val)

                if key == unicode(RDFS.label): # all(map(lambda x: isinstance(x, Literal), res)) and all([x.language for x in res]):
                    langs = [x.language for x in res]
                    res = namedtuple("Label", langs)(*res)

                setattr(obj, URIRef(key), res)

            return obj

        return None

