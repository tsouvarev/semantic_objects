# -*- coding: utf-8 -*-


def normalize_uri(f):

    def inner(self, *args, **kwargs):
        newargs = []
        for uri in args:
            if uri.find("#") > 0:  # full name
                newargs.append("<%s>" % uri)
            else:
                newargs.append(uri)

        newkwargs = {}
        for key, uri in kwargs.iteritems():
            if uri.find("#") > 0:  # full name
                newkwargs[key] = "<%s>" % uri
            else:
                newkwargs[key] = uri

        return f(self, *newargs, **newkwargs)

    return inner


class RDFSQueries(object):

    def __init__(self, connection, prefixes):
        self.connection = connection
        self.prefixes = prefixes

    def query(self, q):
        return self.connection.query("\n".join("prefix %s: <%s>" % (k, v) for (k, v) in self.prefixes.iteritems())+q)

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

    @normalize_uri
    def is_class(self, uri):

        q = """
                ask
                where
                {
                    %(uri)s a rdfs:Class
                }
            """ % {
            "uri": uri,
        }

        return self.query(q)["boolean"]


    @normalize_uri
    def has_attr(self, object_uri, attr_uri):

        q = """
                ask
                where
                {
                    %(object_uri)s %(attr_uri)s ?val
                }
            """ % {
            "object_uri": object_uri,
            "attr_uri": attr_uri,
        }

        return self.query(q)["boolean"]


    @normalize_uri
    def available_properties(self, uri):

        q = """
                select *
                where
                {
                    ?prop rdfs:domain %(parent)s
                }
            """ % {
            "parent": uri,
        }

        results = self.query(q)["results"]["bindings"]

        return [x["prop"]["value"] for x in results]


    @normalize_uri
    def all_resources(self, class_uri):

        q = """
                select *
                where
                {
                    ?cl a %(type)s
                }
            """ % {
            "type": class_uri,
        }

        results = self.query(q)["results"]["bindings"]

        return [x["cl"]["value"] for x in results]


    @normalize_uri
    def get_attr(self, object_uri, attr_uri):

        q = """
                select *
                where
                {
                    %(object_uri)s %(attr_uri)s ?value
                }
            """ % {
            "object_uri": object_uri,
            "attr_uri": attr_uri,
        }

        results = self.query(q)["results"]["bindings"]

        return [x["value"]["value"] for x in results]

    @normalize_uri
    def get_objects_by_attr_value(self, **kwargs):

        q = """
                select *
                where
                {
                    %(propeties)s
                }
            """ % {
            "propeties": ". \n".join("?obj %s %s" % (k, v) for (k, v) in kwargs.iteritems()),
        }

        print q

        results = self.query(q)["results"]["bindings"]

        return [x["obj"]["value"] for x in results]