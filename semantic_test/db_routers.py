class Router ():

	def db_for_read(self, model, **hints):
		
		if model._meta.app_label == "test_usual_db": return "default"
		#else: return "semantic"

	def db_for_write(self, model, **hints):

		if model._meta.app_label == "test_usual_db": return "default"
		#else: return "semantic"

	def allow_relation(self, obj1, obj2, **hints):

		return False

	def allow_syncdb(self, db, model):
		
		if model._meta.app_label == "test_usual_db": return True
		#else: return False
