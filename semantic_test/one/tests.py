from django.test import TestCase
from models import Factory

class SimpleTest(TestCase):

	def test_class_creation (self):
	
		c = Factory ("http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine#Chardonnay")
		
		self.assertEqual ("Chardonnay", c.__name__)
