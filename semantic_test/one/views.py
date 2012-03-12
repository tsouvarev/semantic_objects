#! /bin/python
# -*- coding: utf-8 -*-


#from django.db.models import Manager
from django.http import HttpResponse
from one.models import Factory
from test_usual_db.models import Book
from json import dumps
from django.utils.html import escape

def test(req):

#	w = Chianti()	
	#Book (name = "Discworld", store = "Dom knig", num = 100).save()
#	print type ()
#	print dir (Book.objects.all())
#	
#	
	Chardonnay = Factory ("http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine#Region")
	t = Chardonnay.objects.all ()
	html = ""
#	html = "m: %s<br><br>" % escape (type (Chardonnay.objects))
	html = "get: %s<br><br>" % escape (t.get(uri="http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine#FrenchRegion"))
#	html = "dir: %s<br><br>" % escape (dir (Chardonnay.objects))
#	html += "len: %s<br><br>" % len (t)

#	if type (t) is list:
	for obj in t:

		x = obj
	
		#html += "%s<br>" % (escape (x["http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine#locatedIn"]))
		html += "%s<br>" % (x.uri)
#		html += "%s<br>" % (escape (type(x)))
#		html += "%s<br><br>" % (escape (x.__class__.__mro__))
#	
#		for p in x.__dict__:
#		
#			html += "%s: <br>" % (x[p])
	
		html += "<br>"
			
#	else:
#	
#		html += "%s<br><br>" % t.uri
#	print dumps (a[0].__dict__)
#	print a[0].hasFlavor

	return HttpResponse (html)
