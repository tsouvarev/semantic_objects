from django.db.models import Model, CharField, IntegerField

# Create your models here.

class Book (Model):

	name = CharField (max_length = 20)
	store = CharField (max_length = 20)
	num = IntegerField ()
