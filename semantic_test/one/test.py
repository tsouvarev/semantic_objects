#! /bin/python
# -*- coding: utf-8 -*-

from SemanticObjects.SemanticObjects import *
from SemanticObjects.Connection import Connection
from SemanticObjects.DBBackends import *

s = SemanticObjects (Connection (FourstoreSparqlBackend ("http://fourstore.avalon.ru:80")))
s.test ()
