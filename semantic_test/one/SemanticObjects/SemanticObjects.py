#! /bin/python
# -*- coding: utf-8 -*-

import SPARQLWrapper as wrap
from DBBackends import FourstoreSparqlBackend
from Connection import Connection
from QueryResultParser import convert    

class Class ():

	def __init__ (self, uri):

		self.uri = uri

class Resource ():

	def __init__ (self, *args, **kwargs):

		raise Exception ("You cannot instantiate resource")

# Класс, отображающий RDF-триплеты в объекты Python
class SemanticObjects ():

    def __init__ (self, connection):

        # запоминаем SPARQL-endpoint
		self.conn = connection
        
        # список базовых классов, понадобится при запросах классов и ресурсов из хранилища
        # также играет роль кэша классов
		self.classes = {}
		self.superclasses = {}

    def get_class_properties (self, uri):
    
        # запрос на определение свойств класса в нем же непосредственно определенных
        # (не из иерархии классов)
        q = """
                select ?val
                where 
                {
                    { 
                        <%s> a owl:Class ; 
                        ?rel ?sub . 
                        ?sub owl:onProperty ?prop ;
                             owl:hasValue ?val
                    }
                    union
                    {                   
                        <%s> a owl:Class ;
                        ?prop ?val .
                        ?prop a rdf:Property
                    }
                    union
                    {                   
                        <%s> a owl:Class ;
                        owl:intersectionOf (?f [ owl:onProperty ?prop; owl:hasValue ?val])
                    }       
                    union
                    {                   
                        <%s> a owl:Class ;
                        owl:intersectionOf ( ?class [ owl:onProperty ?prop; owl:hasValue ?val] ?b ) .
                        ?class a owl:Class
                    }
                }
                """ % ((uri,)*4)
        
        # добавляем найденные свойства в словарь, понадобится при создании класса
        props = convert (self.conn.query (q), [("prop", "val",)])
        
        return props
        
    def get_resource_properties (self, uri):
    
        # запрашиваем свойства ресурса из онтологии
        q = """
                select *
                where
                {
                    <%s> ?prop ?val .
                    filter (?prop != rdf:type)
                }
            """ % uri
        
        props = convert (self.conn.query (q), [("prop", "val", )])
        
        return props
    
    def get_available_properties (self, class_uri):
    
        q_all = """select distinct ?all ?inverse ?domain
            where 
            { 
                { 
                    ?all a owl:ObjectProperty 
                }
                union
                { 
                    ?all a owl:DatatypeProperty 
                }
                union 
                {
                    ?inverse owl:inverseOf ?p 
                    ; a owl:ObjectProperty
                }
                union
                {
                    ?inverse owl:inverseOf ?p
                    ; a owl:DatatypeProperty
                }
                union 
                {
                    ?domain rdfs:domain ?d 
                    ; a owl:ObjectProperty
                }
                union
                {
                    ?domain rdfs:domain ?d
                    ; a owl:DatatypeProperty
                }
            }"""
        
        q = convert (self.conn.query (q_all), [ ("all", ["all"],), 
                                ("inverse", ["inverse"],), 
                                ("domain", ["domain"],)])
        
        s_all = set (q["all"])
        s_inverse = set (q["inverse"])
        s_domain = set (q["domain"])
        
#       print "s_all: ", s_all 
        
        obj = self.classes[class_uri]
        
        q = "select distinct ?prop where {"
        
        for cls in obj.__mro__:
        
            if hasattr (cls, "uri"):
        
                q += """
                    {
                    ?prop rdfs:domain <%s> 
                    ; a owl:ObjectProperty
                    }
                    union
                    {
                    ?prop rdfs:domain <%s> 
                    ; a owl:DatatypeProperty
                    }
                    union
                    """ % ((cls.uri,)*2)

        q += """
            {
            ?prop rdfs:domain owl:Thing 
            ; a owl:ObjectProperty 
            }
            union
            {
            ?prop rdfs:domain owl:Thing 
            ; a owl:DatatypeProperty
            }}"""
        
        props = convert (self.conn.query (q), [("props", ["prop"],)])["props"] + list (s_all-s_domain-s_inverse)
        
        return props
        
    
    # если несколько разных значений одного атрибута, то возьмется последнее
    def get_property (self, uri, name):
    
        obj = self.classes[uri]
        
        if name not in obj.__dict__: 
            
            t = self.__get_property (obj.uri, name)
            if t is not None: return t
        
        else: return obj.__dict__[name]     
        
        for base in obj.__class__.__mro__:
            
            #print "base:", base
            
            if hasattr (base, name):
            
                return getattr (base, name)
            
            else:
            
                if hasattr (base, "uri"):
                    t = self.__get_property (base.uri, name)
                    if t is not None: return t              
            
        raise AttributeError ("Key '" + name + "' not in '" + uri + "'")
    
    def __get_property (self, uri, name):
    
        c = {}
        
        q = """
                select ?val
                where 
                {
                    { 
                        <%s> a owl:Class ; 
                        ?rel ?sub . 
                        ?sub owl:onProperty <%s> ;
                             owl:hasValue ?val
                    }
                    union
                    {                   
                        <%s> a owl:Class ;
                        owl:intersectionOf (?f [ owl:onProperty <%s>; owl:hasValue ?val])
                    }       
                    union
                    {                   
                        <%s> a owl:Class ;
                        owl:intersectionOf ( ?class [ owl:onProperty <%s>; owl:hasValue ?val] ?b ) .
                        ?class a owl:Class
                    }
                    union
                    {
                        <%s> rdfs:subClassOf [  rdf:type owl:Restriction ;
                                                owl:onProperty <%s>;
                                                owl:hasValue ?val ]
                    }
                    union
                    {                   
                        <%s> a owl:Class ;
                        <%s> ?val .
                        <%s> a rdf:Property
                    }
                }
                """ % ((uri, name, )*5 + (name,))
        
        # добавляем найденные свойства в словарь, понадобится при создании класса
        
        val = convert (self.conn.query (q), [("val",)])
        
        if "val" in val: 
        
            setattr (classes[uri], name, val["val"])
            return val["val"]
        
        return None

    def get_class_superclasses (self, uri):
    
        bases = []
    
        # запрос на определение родительских классов
        q = """
                select ?class 
                where 
                { 
                    {
                        <%s> a owl:Class ; 
                        rdfs:subClassOf ?class .
                        ?class a owl:Class
                    }
                    union
                    {                   
                        <%s> a owl:Class ;
                        owl:intersectionOf ( ?class ?a ) .
                        ?class a owl:Class
                    }
                    union
                    {                   
                        <%s> a owl:Class ;
                        owl:intersectionOf ( ?class ?a ?b ) .
                        ?class a owl:Class
                    }
                    union
                    {
                        <%s> a owl:Class ;
                        owl:intersectionOf ( ?class ?x ) .
                        ?class a owl:Class .
                        ?x a owl:Class
                    }                                               
                    union
                    {
                        <%s> a owl:Class ;
                        owl:intersectionOf ( ?x ?class ) .
						class a owl:Class .
                        ?x a owl:Class
                    }
                }""" % ((uri,)*5)
        
        a = convert (self.conn.query (q), [("classes", ["class"], )])["classes"]
        
        # сразу заполняем кэш классов, если класс еще не встречался
        for i in a: 
            
            if i not in self.classes: 
            
                self.classes[i] = self.get_class (i)
        
            bases.append (self.classes[i])
        
        return bases

    # функция создания классов по URI
    def get_class (self, uri):

        if uri in self.classes: return self.classes[uri]
        
        t = uri.rsplit ("#")
        name = t[1] if len (t) > 1 else uri.rsplit (":")[1]
        
        props = {} #self.get_class_properties (uri)
        bases = {} #self.get_class_superclasses (uri)
        
        # создаем новый тип, который потом и вернем
        r = type (str(name), tuple (bases), props)
        r.uri = uri
        
        r.__repr__ = lambda self: u"" + self.uri
        r.__str__ = lambda self: u"" + self.uri

        def get_attr (s, key):

            return self.get_property (s.uri, key)

        def set_attr (s, key, val):

			print "key '%s' to '%s'" % (key, val)
			if key not in s.available_properties:
            
				raise KeyError (key)

				base = self.classes[s.uri].__class__
				print "class name: ", base.uri
				
				self.conn.insert (self.prefixes + 
                        "insert {<%s> a owl:ObjectProperty . \
                        <%s> rdfs:domain <%s> . \
                        <%s> <%s> <%s>}" % (key, key, base.uri, s.uri, key, val))
                        # <%s> rdfs:domain <%s> . \ (key, key, base.uri, s.uri, key, val))
                        
			else: 
				try: 
					
					old_val = getattr (s,key)
					print "old: ", old_val
					self.conn.delete (self.prefixes + "delete where {<%s> <%s> <%s>}" % (s.uri, key, old_val))
                
				except: pass                    
                
				self.conn.insert (self.prefixes + "insert {<%s> <%s> <%s>}" % (s.uri, key, val))
				print "inserted: ", val
				
				s.__dict__[key] = val

        def del_attr (s, key):
        
            del s.__dict__[key]
            
            self.conn.delete (self.prefixes + "delete {<%s> <%s> ?v}" % (s.uri, key))

        def create_instance (s, name):

            q = """select ?class
                    where
                    {
                        <%s> a ?class
                    }
                    """ % name

            q = convert (self.conn.query (q), [("class", ["class"], )])["class"]

            if not q: 

                self.conn.insert (self.prefixes + "insert {<%s> a <%s>}" % (name, s.uri, ))
                print "created instance: '%s' of class '%s'" % (name, s.uri,)
            else: print "instance exists: ", name

            s.uri = name

        r.__getitem__ = get_attr
        r.__delitem__ = del_attr
        r.__setitem__ = set_attr

        r.__getattr__ = get_attr
        r.__init__ = create_instance 
    #       r.__setattr__ = set_attr

        r.available_properties = property (lambda x: self.get_available_properties (r.uri))
            # r.__getattribute__ = get

        self.classes[uri] = r
        return r

    # функция получения экземпляров 
    # class_uri - идентификатор класса экземпляров
    def get_resources (self, class_uri):

        #t = self.get_class (class_uri)
        
        q = """
                select ?inst
                where
                {
                    ?inst a <%s>
                }
            """ % class_uri
        
        # список названий всех экземпляров из онтологии
        
        instances = convert (self.conn.query (q), [("inst", ["inst"], )])["inst"]
        
        res = []
        
        for inst in instances:
            
            res.append (self.get_resource (inst, class_uri))
            
        return res
    
    # функция получения конкретного ресурса 
    # uri - идентификатор ресурса
    def get_resource (self, uri, type_name = None):
    
        t = None
        
        if type_name is None:
    
            q = """
                    select ?type
                    where
                    {
                        <%s> a ?type
                    }
                """ % uri
        
            t = convert (self.conn.query (q), [("type",)])
        
        else:
        
            t = self.get_class (type_name)
        
        r = t(uri)
        #r.uri = uri
        
        self.classes[uri] = r
        
        # добавляем в созданный экземпляр найденные свойства
        
#       props = self.get_resource_properties (uri)
#       
#       for i in props: r.__dict__[i] = props[i]        
        
        return r
    
    def test (self):
    
#       self.insert ("insert {<http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine#test> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#Class>}")
    
#       self.delete ("delete where {<http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine#test> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#Class>}")
        
#       self.get_class ("http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine#Chardonnay")
#       
#       print self.get_properties ("http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine#Chardonnay")

		q = "ask {<http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine#test> a <http://www.w3.org/2002/07/owl#Class>}"
		print convert (self.conn.query (q), [("")])
		
		pass
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
