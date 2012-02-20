# Create your views here.

#from django.db.models import Manager
from django.http import HttpResponse
from one.models import *
from json import dumps

def test(req):

	w = Chianti()	
	
	a = Chianti.objects.all()
	print dumps (a[0].__dict__)
	print a[0].hasFlavor

	return HttpResponse ("yay!<br>res: %s" % a)
