#! /bin/python
# -*- coding: utf-8 -*-

import SPARQLWrapper as wrap
from DBBackends import FourStoreBackend

class Thing (object):

	def __repr__ (self): 
	
		return u"" + self.uri
		
 	def __str__ (self):
 	
 		return u"" + self.uri
 	
 	def __unicode__ (self):
 	
 		return u"" + self.uri

	def __getattr__ (self, key):		
		
		print "demanded: ", key
		return self.get_property (s.uri, key)
		
	def __setattr__ (self, key, val):
	
		self.__dict__[key] = val
 			
	__getitem__ = __getattr__
	__setitem__ = __setattr__

# Класс, отображающий RDF-тройки в объекты Python
class SemanticObjects ():

	def __init__ (self, addr):

		# запоминаем SPARQL-endpoint
		#self.sparql = SPARQLWrapper(addr)
		self.db = FourStoreBackend (addr)
		
		# строка, содержащая в итоге все нужные запросам 
		# префиксы для более короткого написания URI ресурсов
		self.prefixes = ""
		
		# пространства имен 
		self.namespaces = {}
		# сокращение для self.namespaces
		self.ns = self.namespaces
		
		# список базовых классов, понадобится при запросах классов и ресурсов из хранилища
		# также играет роль кэша классов
		self.classes = {}
		self.superclasses = {}

		# заранее добавляем пространства, которые точно понадобятся
		self.ns["owl"] = "http://www.w3.org/2002/07/owl#"
		self.ns["rdfs"] = "http://www.w3.org/2000/01/rdf-schema#"
		self.ns["rdf"] = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"

		# формируем сразу шапку запросов из префиксов
		for ns in self.ns: self.prefixes += "PREFIX %s: <%s>\n" % (ns, self.ns[ns])

	def get_query (self, query):
	
		return self.db.query (self.prefixes + query)

	# красивая печать результатов
	def print_results (self, results):

		print results

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

					if p["type"] != "bnode":
						
						print "to create (single): ", p
						
#						if p["type"] == "uri": p = self.get_resource (p["value"])
#						else: p = p["value"]
						p = p["value"]
				
						print "created (single): ", type (p), p
									
						c[i] = p
		
			else:
		
				name,val = schema

				if type(val) == str:

					i,j = name,val

					for prop in properties["results"]["bindings"]:

						p = prop[i]
						v = prop[j]

						if p["type"] != "bnode" and v["type"] != "bnode":

							p = p["value"]
							
							print "to create (str): ", v
							
#							if v["type"] == "uri": v = self.get_resource (v["value"])
#							else: v = v["value"]
							v = v["value"]
					
							print "created (str): ", type (v), v
					
							c[p] = v

				elif type(val) == list:

					c[name] = []

					for p in properties["results"]["bindings"]:

						for n in val:

							if p[n]["type"] != "bnode": 
								
								print "to create (list): ", p[n]
								
#								if p[n]["type"] == "uri": v = self.get_resource (p[n]["value"])
#								else: v = p[n]["value"]
								v = p[n]["value"]
					
								print "created (list): ", type (v), v
					
								c[name].append (v)

		print "done!"
		
		return c

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
						?sub owl:onProperty	?prop ;
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
		
		print "q in get_class_property"
		
		# добавляем найденные свойства в словарь, понадобится при создании класса
		props = self.convert (self.get_query (q), [("prop", "val",)])
		
		return props
		
	def get_resource_properties (self, uri):
	
		# запрашиваем свойства ресурса из онтологии
		q = """
				select *
				where
				{
					<%s> ?prop ?val .
					FILTER (?prop != rdf:type)
				}
			""" % uri
		
		print "q in get_resource_property"
		
		props = self.convert (self.get_query (q), [("prop", "val", )])
		
		return props
	
	# если несколько разных значений одного атрибута, то возьмется последнее
	def get_property (self, uri, name):
	
		print "get: ", uri, name
	
		obj = self.classes[uri]
	
		if name not in obj.__dict__: raise AttributeError ("Key '" + name + "' not in '" + uri + "'")
		else: return obj.__dict__[name]
		
	def __get_property (self, uri, name):
	
		c = {}
		
		q = """
				select ?val
				where 
				{
					{ 
						<%s> a owl:Class ; 
						?rel ?sub . 
						?sub owl:onProperty	<%s> ;
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
						<%s> rdfs:subClassOf [ 	rdf:type owl:Restriction ;
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
		
		print "q in get_property"
		
		val = self.convert (self.get_query (q), [("val",)])
		
		print "val: ", val
		print "type: ", self.classes[uri]
		if "val" in val: 
		
			setattr (self.classes[uri], name, val)
			return val["val"]
		
		return val

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
						?class a owl:Class .
						?x a owl:Class
					}
				}""" % ((uri,)*5)
		
		print "q in get_superclasses"
		
		a = self.convert (self.get_query (q), [("classes", ["class"], )])["classes"]
		print "met: ", a
		
		# сразу заполняем кэш классов, если класс еще не встречался
		for i in a: 
			
			print "getting ", i
			
			if i not in self.classes: 
			
				self.classes[i] = self.get_class (i)
		
			bases.append (self.classes[i])
		
		return bases

	# функция создания классов по URI
	def get_class (self, uri):

		print "cache: ", self.classes

		if uri in self.classes: return self.classes[uri]
		
		print "uri in gc: ", type (uri)
		
		t = uri.rsplit ("#")
		name = t[1] if len (t) > 1 else uri.rsplit (":")[1]
		
		props = {} #self.get_class_properties (uri)
		bases = [object] #self.get_class_superclasses (uri)
		
		# создаем новый тип, который потом и вернем
		r = type (str(name), tuple (bases), props)
		r.uri = uri
		
		r.__repr__ = lambda self: u"" + self.uri
		r.__str__ = lambda self: u"" + self.uri

		def get_attr (s, key):

			return self.get_property (s.uri, key)

		def set_attr (s, key, val):

			s.__dict__[key] = val

		r.__getitem__ = get_attr
		r.__getattr__ = get_attr
		r.__setitem__ = set_attr
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
		
		print "q in get_resources"
		
		instances = self.convert (self.get_query (q), [("inst", ["inst"], )])["inst"]
		
		res = []
		
		print "instances: ", instances
		
		for inst in instances:
			
			print "inst type: ", type (inst)
			res.append (self.get_resource (inst, class_uri))
			
		return res
	
	# функция получения конкретного ресурса 
	# uri - идентификатор ресурса
	def get_resource (self, uri, type_name = None):
	
		print "resource: ", uri
		print "type in get_resource: ", type (type_name)
	
		t = None
		
		if uri == "http://www.w3.org/2002/07/owl#Class": 
		
			print "-1"
			return None
			
		if type_name is None:
	
			q = """
					select ?type
					where
					{
						<%s> a ?type
					}
				""" % uri
		
			print "q in get_resource", uri, self.get_query (q)
		
			t = self.convert (self.get_query (q), [("type",)])
		
			print "!!type: ", t
#			print
		
		else:
		
			print "!!!!!!! ", type (type_name)
			t = self.get_class (type_name)
		
		print "??type: ", t
		
		r = t()
		r.uri = uri
		
		self.classes[uri] = r
		
		print "mem: ", uri, r
		
		# добавляем в созданный экземпляр найденные свойства
		
#		props = self.get_resource_properties (uri)
#		
#		for i in props: r.__dict__[i] = props[i]		
		
		return r
	
			

						
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
