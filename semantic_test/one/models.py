from django.db.models import *
from django.db.models.query import QuerySet
from SemanticObjects import *

# Create your models here.

class SemanticQuerySet (QuerySet):

	def __init__(self, model, uri, ns, namespace):
		
		super(SemanticQuerySet, self).__init__(model)
		
		self.s = SemanticObjects ("http://fourstore.avalon.ru/sparql/")
		self.s.add_namespace (ns, namespace)
		
		self.ns = ns
		self.uri = uri
		
		self.resources = self.s.get_resources (self.ns + ":" + self.uri)
		print type (self.resources[0])
		
	def __repr__ (self):
	
		return str (self.resources)
		
	def __iter__ (self):
	
		return iter (self.resources)
		
	def __getitem__ (self, k):
	
		if -1 < k < len (self.resources): return self.resources[k]
		else: return None
	
#	def filter (self, **kwargs):
#	
#		return None
#		
#	def exclude (self, **kwargs):
#	
#		return None
#		
#	def annotate (self, *args, **kwargs):
#	
#		return None
#		
#	def order_by (self, *fields):
#	
#		return None
#		
#	def reverse (self):
#	
#		return None
#		
#	def distinct (self, *fields):
#	
#		return None

class SemanticManager (Manager):

	def __init__(self, namespace, ns, uri):

		super(SemanticManager, self).__init__()
		
		self.namespace = namespace
		self.ns = ns
		self.uri = uri	
		
	def get_query_set (self):
	
		return SemanticQuerySet (self.model, self.uri, self.ns, self.namespace)
	
	def all (self):

		return SemanticQuerySet (self.model, self.uri, self.ns, self.namespace)
		
class Chianti (Model):

	uri = "Winery"
	namespace = "http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine#"
	ns = "wines"
	hasMaker = CharField (max_length = 20)
	objects = SemanticManager(namespace, ns, uri)
	
