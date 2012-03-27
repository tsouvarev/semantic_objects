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
#	# "http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine#Chardonnay"
	Chardonnay = Factory ("http://www.w3.org/2002/07/owl#Class")
	t = Chardonnay.objects.all ()
	html = ""
#	html = "m: %s<br><br>" % escape (type (Chardonnay.objects))
#	html = "get: %s<br><br>" %  (t.filter(uri="http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine#BancroftChardonnay"))
#	html = "dir: %s<br><br>" % escape (dir (Chardonnay.objects))
#	html += "len: %s<br><br>" % len (t)
	
#	if type (t) is list:
	obj = t.get (uri = "http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine#test")
	
	html += "<br><br>%s<br><br>" % (obj.available_properties)
	
	obj["http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine#test_property"] = "http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine#one"
	obj ["http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine#test_property5"] = "http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine#two"
	
#	del obj["http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine#test_property2"]
	
	#print obj["http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine#test_property"]
	
	for prop in obj.available_properties:

#		x = obj
#	
#		#html += "%s<br>" % (escape (x["http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine#locatedIn"]))
		#html += "%s: %s<br>" % (prop, getattr (obj, prop))
		try:
			html += "%s: %s<br>" % (prop, getattr (obj, prop))
		except: 
			html += "%s: %s<br>" % (prop, None)
##		html += "%s<br>" % (x.available_properties)
#		
##		html += "%s<br><br>" % (x["http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine#hasFlavor"])

##		html += "%s<br><br>" % (escape (x.__class__.__mro__))
##	
##		for p in x.__dict__:
##		
##			html += "%s: <br>" % (x[p])
#	
#		html += "<br>"
			
	obj = t.get (uri = "http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine#Chianti")
	
	html += "%s: %s<br>" % (obj.uri, obj.available_properties)
	
#	else:
#	
#		html += "%s<br><br>" % t.uri
#	print dumps (a[0].__dict__)
#	print a[0].hasFlavor

	return HttpResponse (html)
