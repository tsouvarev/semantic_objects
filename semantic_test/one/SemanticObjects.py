#! /bin/python
# -*- coding: utf-8 -*-

import SPARQLWrapper as wrap
from SPARQLWrapper import SPARQLWrapper, JSON

# Класс, отображающий RDF-тройки в объекты Python
class SemanticObjects ():

	def __init__ (self, addr):

		# запоминаем SPARQL-endpoint
		self.sparql = SPARQLWrapper(addr)
		
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

	# выполняет запрос, возвращает результат в виде почти прямого 
	# переноса XML/RDF на списки и объекты в Python
	def get_query (self, query):

		self.sparql.setQuery(self.prefixes + query)

		self.sparql.setReturnFormat(JSON)
		results = self.sparql.query().convert()

		return results

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

	# конвертация результатов от get_query в более удобный вид
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
	def convert (self, properties, schemas, split = False):

		c = {}
		
		for schema in schemas:
		
			if len (schema) == 1:
		
				i, = schema
		
				for prop in properties["results"]["bindings"]:

					p = prop[i]

					if p["type"] != "bnode":

						p = p["value"]
				
						if split: p = p.rsplit ("#")[1]
					
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
							v = v["value"]
					
							if split:
								p = p.rsplit ("#")[1]
								v = v.rsplit ("#")[1]
						
							c[p] = v

				elif type(val) == list:

					c[name] = []

					for p in properties["results"]["bindings"]:

						for n in val:

							if p[n]["type"] != "bnode": 
					
								v = p[n]["value"]
					
								if split: v = v.rsplit("#")[1]
						
								c[name].append (v)

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
				
		props = self.convert (self.get_query (q), [("prop", "val", )])
		
		return props
	
	# если несколько разных значений одного атрибута, то возьмется последнее
	def get_property (self, uri, name):
	
		val = self.__get_property (uri, name)
		if val is not None: return val
			
		if uri in self.classes:
		
			print "mro: ", self.classes[uri].__mro__
		
			for cls in self.classes[uri].__mro__:
			
				print cls.__name__
			
				if hasattr (cls, name): return getattr(cls, name)
				
				elif hasattr (cls, "uri"): 
				
					t = self.__get_property (cls.uri, name)  
					
					if t is not None: return t
		
		return None
		
	
	def __get_property (self, uri, name):
	
		if hasattr (self.classes[uri], name): return getattr (self.classes[uri], name)
		
		c = {}
				
			#print "in: %s" % ([self.classes[uri]] +self.superclasses[self.classes[uri].uri])
			
#			if uri not in self.superclasses:

#				if name not in dir(self.classes[uri]): val = self.get_property (self.classes[uri].uri, name)
#				else: val = self.classes[uri].__getattribute__ (name)
#			
#				for b in self.superclasses[self.classes[uri].uri]: # properties for resource
#				
#					print b
#				
#					if name not in dir(b): val = self.get_property (b.uri, name)
#					else: val = b.__getattribute__ (name)
#				
#					if val is not None: return val
	
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
		
		print self.get_query (q)
		
		val = self.convert (self.get_query (q), [("val",)])	
		
		print "type: ", type(self.classes[uri])
		if "val" in val: setattr (self.classes[uri], name, val)
		
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
		
		# сразу заполняем кэш классов, если класс еще не встречался
		# TODO: если кэш не сбрасывается между запросами, 
		# то почему в иерархии наследования для конкретного класса нет лишних классов?
		for i in self.convert (self.get_query (q), [("classes", ["class"], )])["classes"]: 
			
			if i not in self.classes: 
				self.classes[i] = self.get_class (i)
		
			bases.append (self.classes[i])
		
		#self.superclasses[uri] = bases
#		print "b: %s" % bases
		
		return bases

	# функция создания классов по URI
	def get_class (self, uri):

		if uri in self.classes: return self.classes[uri]
		
		# выделяем название класса из URI
		# может быть в виде smth#name или smth:name
		# первое есть традиционная форма записи, вторая принята в SPARQL-запросах
		t = uri.rsplit ("#")
		name = t[1] if len (t) > 1 else uri.rsplit (":")[1]
		
		props = {} #self.get_class_properties (uri)
		bases = self.get_class_superclasses (uri)
		
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
# 		r.__getattribute__ = get
 		
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
		instances = self.convert (self.get_query (q), [("inst", ["inst"], )])["inst"]
		
		res = []
		
		for inst in instances:
		
			res.append (self.get_resource (inst, class_uri))
			
		return res
	
	# функция получения конкретного ресурса 
	# uri - идентификатор ресурса
	def get_resource (self, uri, type_name = None):
	
		if type_name is None:
	
			q = """
					select ?type
					where
					{
						<%s> a ?type
					}
				""" % uri
		
			type_name = self.convert (self.get_query (q), [("type", ["type"])])["type"][0]
				
		t = self.get_class (type_name)
				
		self.classes[uri] = t
		
		r = t()
		r.uri = uri
		
		# добавляем в созданный экземпляр найденные свойства
		
#		props = self.get_resource_properties (uri)
#		
#		for i in props: r.__dict__[i] = props[i]		
		
		return r
	
			

						
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
