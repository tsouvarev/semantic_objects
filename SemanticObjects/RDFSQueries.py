# -*- coding: utf-8 -*-
from SPARQLWrapper.SPARQLExceptions import QueryBadFormed
from rdflib import URIRef


def default_to(default=None):
    def outer(f):
        def inner(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except:
                return default
        return inner
    return outer


class RDFSQueries(object):

    def __init__(self, connection, prefixes):
        self.connection = connection
        self.prefixes = prefixes

    def query(self, q):
        return self.connection.query("\n".join("prefix %s: <%s>" % (k, v) for (k, v) in self.prefixes.iteritems())+q)

    def insert(self, q):
        return self.connection.insert("\n".join("prefix %s: <%s>" % (k, v) for (k, v) in self.prefixes.iteritems())+q)

    @default_to(None)
    def all(self):

        q = """
                select ?s ?p ?o
                where
                {
                    ?s ?p ?o
                }
            """

        results = self.query(q)["results"]["bindings"]
        return [(x["s"]["value"], x["p"]["value"], x["o"]["value"]) for x in results]

    @default_to(None)
    def is_class(self, uri):

        q = """
                ask
                where
                {
                    <%(uri)s> a rdfs:Class
                }
            """ % {
            "uri": uri,
        }

        return self.query(q)["boolean"]

    @default_to(None)
    def is_property(self, uri):

        q = """
                ask
                where
                {
                    {
                        <%(uri)s> a owl:ObjectProperty
                    }
                    union
                    {
                        <%(uri)s> a rdf:Property
                    }
                }
            """ % {
            "uri": uri,
        }

        return self.query(q)["boolean"]

    @default_to(None)
    def is_object(self, uri):

        return not self.is_class(uri) and not self.is_property(uri)

    @default_to(None)
    def exists(self, uri):

        q = """
                ask
                where
                {
                    <%(uri)s> ?p ?o
                }
            """ % {
            "uri": uri,
        }

        return self.query(q)["boolean"]

    @default_to(None)
    def has_attr(self, object_uri, attr_uri):

        q = """
                ask
                where
                {
                    <%(object_uri)s> <%(attr_uri)s> ?val
                }
            """ % {
            "object_uri": object_uri,
            "attr_uri": attr_uri,
        }

        return self.query(q)["boolean"]

    @default_to([])
    def available_class_properties(self, class_uri):

        q = """
                select distinct ?prop ?prop_type ?val
                where
                {
                    {
                        ?prop rdfs:domain <%(class_uri)s> .
                        ?prop rdfs:range ?prop_type
                    }
                    union
                    {
                        {
                            ?prop rdfs:range ?prop_type
                        }
                        minus
                        {
                            ?prop rdfs:domain ?tmp
                        }
                    }
                }
            """ % {
            "class_uri": class_uri,
        }

        results = self.query(q)["results"]["bindings"]
        return results

    @default_to([])
    def available_object_properties(self, object_uri):

        q = """
                select distinct *
                where
                {
                    <%(object_uri)s> ?prop ?val .
                    filter (?prop != rdf:type) .
                    optional {?val a ?prop_type .}
                }
            """ % {
            "object_uri": object_uri,
        }

        results = self.query(q)["results"]["bindings"]
        return results

    @default_to([])
    def all_resources(self, class_uri):

        q = """
                select *
                where
                {
                    ?obj_uri a <%(type)s>
                }
            """ % {
            "type": class_uri,
        }

        results = self.query(q)["results"]["bindings"]

        return [URIRef(x["obj_uri"]["value"]) for x in results]

    @default_to(None)
    def get_attr(self, object_uri, attr_uri):

        q = """
                select *
                where
                {
                    <%(object_uri)s> <%(attr_uri)s> ?value
                }
            """ % {
            "object_uri": object_uri,
            "attr_uri": attr_uri,
        }

        results = self.query(q)["results"]["bindings"]

        return [x["value"] for x in results]

    @default_to([])
    def get_class_objects_by_attr_value(self, class_uri, **kwargs):

        q = """
                select *
                where
                {
                    ?obj a <%(class_uri)s> ;
                    %(propeties)s
                }
            """ % {
            "class_uri": class_uri,
            "propeties": ";\n".join("<%s> <%s>" % (k, v) for (k, v) in kwargs.iteritems()),
        }

        results = self.query(q)["results"]["bindings"]

        return [URIRef(x["obj"]["value"]) for x in results]

    @default_to([])
    def get_subclasses_of_class(self, class_uri):

        q = """
                select *
                where
                {
                    ?subcl a rdfs:Class ;
                    rdfs:subClassOf <%(class_uri)s>
                }
            """ % {
            "class_uri": class_uri,
        }

        results = self.query(q)["results"]["bindings"]

        return [URIRef(x["subcl"]["value"]) for x in results]

    @default_to(None)
    def get_parent_class(self, object_uri):

        q = """
                select ?class_uri
                where
                {
                    <%(object_uri)s> a ?class_uri
                }
            """ % {
            "object_uri": object_uri,
        }

        results = self.query(q)["results"]["bindings"]

        return [URIRef(x["class_uri"]["value"]) for x in results][0]

    @default_to([])
    def get_base_classes(self, class_uri):
        q = """
                select ?class_uri
                where
                {
                    <%(class_uri)s> rdfs:subClassOf ?class_uri
                }
            """ % {
            "class_uri": class_uri,
        }

        results = self.query(q)["results"]["bindings"]

        return [URIRef(x["class_uri"]["value"]) for x in results]

    @default_to(None)
    def insert_data(self, data):
        q = """
                insert data
                {
                    %(data)s
                }
            """ % {
            "data": ["<%s> <%s> <%s> ." % triplet for triplet in data]
        }

        return self.insert(q)["boolean"]

    @default_to(None)
    def create_object(self, object_uri, class_uri):
        q = """
                insert data
                {
                    <%(object_uri)s> a <%(class_uri)s>
                }
            """ % {
            "object_uri": object_uri,
            "class_uri": class_uri,
        }

        return self.insert(q)["boolean"]

    @default_to(None)
    def create_class(self, class_uri):
        q = """
                insert data
                {
                    <%(class_uri)s> a rdfs:Class
                }
            """ % {
            "class_uri": class_uri,
        }

        return self.insert(q)["boolean"]

    def delete_data(self, data):
        q = """
                delete data
                {
                    %(data)s
                }
            """ % {
            "data": ["<%s> <%s> <%s> ." % triplet for triplet in data]
        }

        return self.insert(q)["boolean"]

    @default_to(None)
    def delete_object(self, object_uri, class_uri):
        q = """
                dalete data
                {
                    <%(object_uri)s> a <%(class_uri)s>
                }
            """ % {
            "object_uri": object_uri,
            "class_uri": class_uri,
        }

        return self.insert(q)["boolean"]

    @default_to(None)
    def delete_class(self, class_uri):
        q = """
                delete data
                {
                    <%(class_uri)s> a rdfs:Class
                }
            """ % {
            "class_uri": class_uri,
        }

        return self.insert(q)["boolean"]