# Create your views here.

#from django.db.models import Manager
from django.http import HttpResponse
from one.models import *

def test(req):

	w = Chianti()	

	return HttpResponse ("yay!<br>res: %s" % Chianti.objects.all())
