#! /bin/python
# -*- coding: utf-8 -*-

#import SPARQLWrapper as wrap
from DBBackends import *

class Connection ():

    def __init__ (self, backend):
    
        if not isinstance (backend, Backend): raise Exception ("Given wrong backend for connection: %s" % backend)

        self.db = backend

    def query (self, query):

#        print "q"
        return self.db.query (query)

    def insert (self, query):
    
        return self.db.insert (query)
        
    def delete (self, query):
    
        return self.db.delete (query)

class QueryResultsParser ():

    def __init__ (self):

#        if not isinstance (conn, Connection): raise Exception ("Given wrong connection for QueryParser: %s" % conn)

        # запоминаем SPARQL-endpoint
#        self.conn = conn

        # строка, содержащая в итоге все нужные запросам 
        # префиксы для более короткого написания URI ресурсов
        self.prefixes = ""
        
        # пространства имен 
        self.namespaces = {}
        # сокращение для self.namespaces
        self.ns = self.namespaces
        
        # заранее добавляем пространства, которые точно понадобятся
        self.ns["owl"] = "http://www.w3.org/2002/07/owl#"
        self.ns["rdfs"] = "http://www.w3.org/2000/01/rdf-schema#"
        self.ns["rdf"] = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"

        # формируем сразу шапку запросов из префиксов
        for ns in self.ns: self.prefixes += "PREFIX %s: <%s>\n" % (ns, self.ns[ns])     

#    def get_query (self, query):
    
#        return self.conn.query (self.prefixes + query)

    # красивая печать результатов
    def print_results (self, results):

        #print results

        for result in results["results"]["bindings"]:

            for i in results["head"]["vars"]: print "%s: %s" % (i, result[i]["value"])
            print

    # добавление пространства имен
    def add_namespace (self, name, namespace):

        self.namespaces[name] = namespace
        
        # сразу обновляем шапку запросов
        self.prefixes += "PREFIX %s: <%s>\n" % (name, namespace)

    # конвертация результатов от get_query в более удобный вид (description is obsoleted)
    # properties - результаты от get_query
    # schema - схема преобразования
    #
    # schema состоит из кортежей соответствия нового названия, которое хотим дать, и свойств из properties
    #
    # каждый кортеж преобразовывается в атрибут итогового объекта
    #
    # первый параметр в кортеже есть название для атрибута в итоговом объекте
    # если в кортеже второй параметр строка, то атрибут будет строковым
    # если в кортеже второй параметр список, то множество значений из properties
    # попадут в один и тот же список. в списке может быть произвольное число элементов, из них и будет 
    # формироваться атрибут в итоговом объекте
    # 
    # например, кортеж ("a", "b") означает взять из properties свойство "b" и 
    # записать его в итоговый объект как атрибут "a"
    # кортеж ("a", ["b","c"]) означает взять из properties все свойства под названиями "b" и "c" и
    # записать их в один список под названием "a"
    def convert (self, properties, schemas, split = False, create = False):

        c = {}
        
        for schema in schemas:
        
            if len (schema) == 1:
        
                i, = schema
        
                for prop in properties["results"]["bindings"]:

                    p = prop[i]

                    if "type" in p and p["type"] != "bnode":
                        
#                       if p["type"] == "uri": p = self.get_resource (p["value"])
#                       else: p = p["value"]
                        p = p["value"]
                    
                        c[i] = p
        
            else:
        
                name,val = schema

                if type(val) == str:

                    i,j = name,val

                    for prop in properties["results"]["bindings"]:

                        p = prop[i]
                        v = prop[j]

                        if "type" in p and p["type"] != "bnode" and \
                            "type" in v and v["type"] != "bnode":

                            p = p["value"]
                            
#                           if v["type"] == "uri": v = self.get_resource (v["value"])
#                           else: v = v["value"]
                            v = v["value"]
                    
                            c[p] = v

                elif type(val) == list:

                    c[name] = []

                    for p in properties["results"]["bindings"]:

                        for n in val:

                            if "type" in p[n] and p[n]["type"] != "bnode": 
                                
#                               if p[n]["type"] == "uri": v = self.get_resource (p[n]["value"])
#                               else: v = p[n]["value"]
                                v = p[n]["value"]
                
                                c[name].append (v)

        return c






















































