#test API for runing some basic tests on the engine
from engine import run_all
from variables import *
from actions import *
import weakref
import json


#input variables
class ProductVariables(BaseVariables):

    def __init__(self, product):
        self.product = product

    @numeric_rule_variable
    def actual(self):
        return self.product.actual

    @numeric_rule_variable
    def expected(self):
        return self.product.expected


#action variables
class ProductActions(BaseActions):

    def __init__(self, product):
        self.product = product

    @rule_action()
    def condition_pass(self):
        print("All expected access points are present")
    
    @rule_action()
    def condition_fail(self) :
        print("NOT all expected access points are present")


#build rules
with open('rules.txt') as json_file:  
    rules = json.load(json_file)

#build database
class Products :
    _instances = set()

    def __init__(self,actual,expected) :
        self.expected = expected
        self.actual = actual
        self._instances.add(weakref.ref(self))
    
    @classmethod
    def getinstances(cls):
        dead = set()
        for ref in cls._instances:
            obj = ref()
            if obj is not None:
                yield obj
            else:
                dead.add(ref)

term1 = Products(23,44)
term2 = Products(89,89)
term3 = Products(94,52)


#run Rules
for product in Products.getinstances():
    run_all(rule_list=rules,
            defined_variables=ProductVariables(product),
            defined_actions=ProductActions(product),
            stop_on_first_trigger=True
           )