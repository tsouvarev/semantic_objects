#! /bin/python
# -*- coding: utf-8 -*-

def print_results (results):

    #print results

    for result in results["results"]["bindings"]:

        for i in results["head"]["vars"]: print "%s: %s" % (i, result[i]["value"])
        print

# конвертация результатов от get_query в более удобный вид (description is obsoleted)
# properties - результаты от get_query
# schema - схема преобразования
#
# schema состоит из кортежей соответствия нового названия, которое хотим дать, и свойств из properties
#
# каждый кортеж преобразовывается в атрибут итогового объекта
#
# первый параметр в кортеже есть название для атрибута в итоговом объекте
# если в кортеже второй параметр строка, то атрибут будет строковым
# если в кортеже второй параметр список, то множество значений из properties
# попадут в один и тот же список. в списке может быть произвольное число элементов, из них и будет 
# формироваться атрибут в итоговом объекте
# 
# например, кортеж ("a", "b") означает взять из properties свойство "b" и 
# записать его в итоговый объект как атрибут "a"
# кортеж ("a", ["b","c"]) означает взять из properties все свойства под названиями "b" и "c" и
# записать их в один список под названием "a"
def convert (properties, schemas, split = False, create = False):

    c = {}
    
    for schema in schemas:
    
        if len (schema) == 1:
    
            i, = schema
    
            for prop in properties["results"]["bindings"]:

                p = prop[i]

                if "type" in p and p["type"] != "bnode":
                    
#                       if p["type"] == "uri": p = self.get_resource (p["value"])
#                       else: p = p["value"]
                    p = p["value"]
                
                    c[i] = p
    
        else:
    
            name,val = schema

            if type(val) == str:

                i,j = name,val

                for prop in properties["results"]["bindings"]:

                    p = prop[i]
                    v = prop[j]

                    if "type" in p and p["type"] != "bnode" and \
                        "type" in v and v["type"] != "bnode":

                        p = p["value"]
                        
#                           if v["type"] == "uri": v = self.get_resource (v["value"])
#                           else: v = v["value"]
                        v = v["value"]
                
                        c[p] = v

            elif type(val) == list:

                c[name] = []

                for p in properties["results"]["bindings"]:

                    for n in val:

                        if "type" in p[n] and p[n]["type"] != "bnode": 
                            
#                               if p[n]["type"] == "uri": v = self.get_resource (p[n]["value"])
#                               else: v = p[n]["value"]
                            v = p[n]["value"]
            
                            c[name].append (v)

    return c


