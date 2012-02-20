# Create your views here.

#from django.db.models import Manager
from django.http import HttpResponse
from one.models import *
from test_usual_db.models import Book
from json import dumps

def test(req):

	w = Chianti()	
	#Book (name = "Discworld", store = "Dom knig", num = 100).save()
	print Book.objects.all()[0]
	
	
	a = Chianti.objects.all()
	print dumps (a[0].__dict__)
	print a[0].hasFlavor

	return HttpResponse ("yay!<br>res: %s" % a)
