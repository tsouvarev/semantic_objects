# Create your views here.

#from django.db.models import Manager
from django.http import HttpResponse
from one.models import *
from test_usual_db.models import Book
from json import dumps

def test(req):

	w = Chianti()	
	#Book (name = "Discworld", store = "Dom knig", num = 100).save()
#	print type ()
#	print dir (Book.objects.all())
#	
#	
	html = ""
	html += "%s<br><br>" %  Chianti.objects.all()[0]
	print 
	html += "%s<br>" % dir (Book.objects)
#	print dumps (a[0].__dict__)
#	print a[0].hasFlavor

	return HttpResponse (html)
