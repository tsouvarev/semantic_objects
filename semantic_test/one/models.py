from django.db.models import *
from django.db.models.query import QuerySet
from SemanticObjects import *
# Create your models here.

class SemanticQuerySet (QuerySet):

	def __init__(self):

		super(SemanticQuerySet, self).__init__()
		
	def filter (self, **kwargs):
	
		return None
		
	def exclude (self, **kwargs):
	
		return None
		
	def annotate (self, *args, **kwargs):
	
		return None
		
	def order_by (self, *fields):
	
		return None
		
	def reverse (self):
	
		return None
		
	def distinct (self, *fields):
	
		return None

class SemanticManager (Manager):

	def __init__(self, namespace, ns, uri):

		super(SemanticManager, self).__init__()
		self.namespace = namespace
		self.ns = ns
		self.uri = uri
		self.qs = SemanticQuerySet()
		self.s = SemanticObjects ("http://fourstore.avalon.ru/sparql/")
		self.s.add_namespace (ns, namespace)
         
	def get_query_set(self):
	
		return self.qs

	def all (self):

		return self.s.get_resources (self.ns + ":" + self.uri)

class Chianti (Model):

	uri = "Chianti"
	namespace = "http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine#"
	ns = "wines"
	hasMaker = CharField (max_length = 20)
	objects = SemanticManager(namespace, ns, uri)
	
