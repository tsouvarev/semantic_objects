# -*- coding: utf-8 -*-
import hashlib

from django.test import TestCase
from rdflib import Namespace, RDFS, Literal
from SemanticObjects import Factory, Thing
from Connection import Connection
from DBBackends import AllegroBackend

local = Namespace("http://www.owl-ontologies.com/Ontology1359802755.owl#")


class TestClass(object):

    def __init__(self, *args, **kwargs):

        super(TestClass, self).__init__(*args, **kwargs)

        db = AllegroBackend("http://localhost:10035/repositories/main")
        c = Connection(db)
        self.factory = Factory(c)

    def __enter__(self):

        unique_uuid = hashlib.md5("http://www.owl-ontologies.com/Ontology1359802755.owl#").hexdigest()
        self.class_name = getattr(local, unique_uuid)

        exists_before = self.factory.query.exists(self.class_name)

        if exists_before:
            raise Exception("test class already exists")

        self.cl = self.factory.get_class(self.class_name)

        return self.cl

    def __exit__(self, type, value, traceback):

        res = self.cl.delete_class()

        if not res:
            raise Exception("failed to delete test class")

        exists_after = self.factory.query.exists(self.class_name)

        if exists_after:
            raise Exception("test class still exists")


# 2.1. Отображение классов онтологии на классы Python;
class ClassTest(TestCase):

    def setUp(self):
        db = AllegroBackend("http://localhost:10035/repositories/main")
        c = Connection(db)
        self.factory = Factory(c)

    # 2.1.1. Получение класса по идентификатору;
    def test_get_class(self):
        section = self.factory.get_class(local.Section)

        self.assertEqual(section.uri, local.Section)
        self.assertTrue(issubclass(section, Thing))
        self.assertTrue(hasattr(section, local.subSectionOf))

    # 2.1.2. Получение базовых классов данного класса;
    def test_get_baseclasses(self):
        comment = self.factory.get_class(local.Comment)
        unlike = self.factory.get_class(local.Unlike)

        self.assertTrue(comment in unlike.mro())

    # 2.1.3. Получение дочерних классов данного класса.
    def test_get_subclasses(self):
        comment = self.factory.get_class(local.Comment)
        unlike = self.factory.get_class(local.Unlike)
        like = self.factory.get_class(local.Like)
        free_form_comment = self.factory.get_class(local.FreeFormComment)

        self.assertTrue(issubclass(unlike, comment))
        self.assertItemsEqual(comment.get_subclasses(), [unlike, like, free_form_comment])


# 2.2. Отображение объектов онтологии на объекты Python;
class ObjectTest(TestCase):

    def setUp(self):
        db = AllegroBackend("http://localhost:10035/repositories/main")
        c = Connection(db)
        self.factory = Factory(c)

    # 2.2.1. Получение объекта по идентификатору;
    def test_get_object(self):
        emma = self.factory.get_object(local.Emma)
        user = self.factory.get_class(local.User)
        self.assertEqual(emma.uri, local.Emma)
        self.assertTrue(hasattr(emma, local.knows))
        self.assertTrue(isinstance(emma, user))

    # 2.2.2. Получение всех объектов данного класса;
    def test_get_all(self):
        user = self.factory.get_class(local.User)

        emma = self.factory.get_object(local.Emma)
        elena = self.factory.get_object(local.Elena)
        sarah = self.factory.get_object(local.Sarah)

        self.assertItemsEqual([x.uri for x in user.get_objects()], [x.uri for x in [emma, sarah, elena]])

    # 2.2.3. Получение всех объектов данного класса, обладающих заданным значением некоторого свойства.
    def get_filteres_objects(self):
        kwargs = {local.knows: local.Elena}

        user = self.factory.get_class(local.User)

        emma = self.factory.get_object(local.Emma)
        sarah = self.factory.get_object(local.Sarah)

        self.assertItemsEqual(user.filter(kwargs), [emma, sarah])
        self.assertItemsEqual(user.filter(**kwargs), [emma, sarah])


# 2.3. Отображение связей онтологии на связи между объектами Python:
class PropertyTest(TestCase):

    def setUp(self):
        db = AllegroBackend("http://localhost:10035/repositories/main")
        c = Connection(db)
        self.factory = Factory(c)

    # 2.3.1. Получение самих свойств;
    def test_get_property(self):

        emma = self.factory.get_object(local.Emma)
        sarah = self.factory.get_object(local.Sarah)
        elena = self.factory.get_object(local.Elena)

        self.assertItemsEqual(getattr(emma, local.knows), [sarah, elena])
        self.assertRaises(AttributeError, getattr, emma, local.knowsMe)

        harry = self.factory.get_object(local.HarryPotter)
        self.assertEqual(getattr(harry, local.subSectionOf), None)

    # 2.3.2. Корректная типизация свойств;
    def test_correct_types(self):

        emma = self.factory.get_object(local.Emma)
        user = self.factory.get_class(local.User)

        self.assertItemsEqual([type(x) for x in getattr(emma, local.knows)], [user, user])

        harry = self.factory.get_object(local.HarryPotter)

        self.assertItemsEqual(getattr(harry, RDFS.label), (Literal(u"Гарри Поттер", lang='ru'),
                                                           Literal("Harry Potter", lang='en')))

    # 2.3.3. Получение области значений и определения для свойства (объект/литерал);
    def test_range(self):

        user = self.factory.get_class(local.User)

        self.assertEqual(getattr(user, local.knows), user)

    # 2.3.4. Корректная поддержка множественных значений свойств.
    def test_list_property(self):

        emma = self.factory.get_object(local.Emma)
        sarah = self.factory.get_object(local.Sarah)
        elena = self.factory.get_object(local.Elena)

        self.assertItemsEqual(getattr(emma, local.knows), [sarah, elena])


# 3. Реализовать возможность манипуляции сущностями из онтологии с помощью отображателя:
class CreateDeleteTest(TestCase):

    def setUp(self):
        db = AllegroBackend("http://localhost:10035/repositories/main")
        c = Connection(db)
        self.factory = Factory(c)

    # 3.1. Создание классов в онтологии;
    def test_create_class(self):

        exists_before = self.factory.query.exists(local.test)

        self.assertEqual(exists_before, False)

        cl = self.factory.get_class(local.test)

        exists_after = self.factory.query.exists(local.test)

        self.assertEqual(exists_after, True)

    # 3.2. Удаление классов из онтологии;
    def test_delete_class(self):

        cl = self.factory.get_class(local.test)
        res = cl.delete_class()

        self.assertEqual(res, True)

        exists_after = self.factory.query.exists(local.test)

        self.assertEqual(exists_after, False)

    # 3.3. Создание объектов в онтологии;
    def test_create_object(self):

        with TestClass() as cl:

            exists_before = self.factory.query.exists(local.HarryPotter2)

            self.assertEqual(exists_before, False)
            cl(local.HarryPotter2)

            exists_after = self.factory.query.exists(local.HarryPotter2)

            self.assertEqual(exists_after, True)

    # 3.4. Удаление объектов из онтологии;
    def test_delete_object(self):

        with TestClass() as cl:

            obj = cl(local.HarryPotter2)

            exists_before = self.factory.query.exists(local.HarryPotter2)

            self.assertEqual(exists_before, True)

            res = obj.delete()

            self.assertEqual(res, True)

            exists_after = self.factory.query.exists(local.HarryPotter2)

            self.assertEqual(exists_after, False)






 # 3.5. Создание связей в онтологии;
 # 3.6. Удаление связей из онтологии;
 # 3.7. Изменение связей для объектов из онтологии.