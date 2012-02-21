#! /bin/python
# -*- coding: utf-8 -*-


#from django.db.models import Manager
from django.http import HttpResponse
from one.models import *
from test_usual_db.models import Book
from json import dumps
from django.utils.html import escape

def test(req):

	w = Chianti()	
	#Book (name = "Discworld", store = "Dom knig", num = 100).save()
#	print type ()
#	print dir (Book.objects.all())
#	
#	

	
	html = "m: %s<br><br>" % escape (type (Chianti.objects))
	
	for obj in Chianti.objects.all():
	
		html += "%s " % obj

#	print dumps (a[0].__dict__)
#	print a[0].hasFlavor

	return HttpResponse (html)
