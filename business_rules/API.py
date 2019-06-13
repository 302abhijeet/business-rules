#API for the Rule based engine

from engine import run_all
from variables import *
from actions import *
from best_case import *
import weakref
import json
import collector

#import prodcut variables from UI
with open('variables.txt') as f:
    variables = json.load(f)


#create ruleVariables
class ProductVariables(BaseVariables):

    def __init__(self, product):
        self.product = product

    for var in variables :
        if var['options'] == 'None' :
            exec("@" + var['field'] + "(" + var['label'] + ")" + """\ndef """ + var['name'] + """(self): \n\treturn """ + var['formulae'])
        else :
            exec("@" + var['field'] + "(" + var['label'] + "," + var['options'] + """)\ndef """ + var['name'] + """(self):\n\treturn """ + var['formulae'])



#import product actions from UI
with open('actions.txt') as f:
    actions = json.load(f)


#Create ruleActions
class ProductActions(BaseActions):

    def __init__(self, product):
        self.product = product

    for act in actions : 
        li = []
        if act['params'] :
            for args in act['params'] :
                li.append(args)
        args = "(self" + ','.join(li) + ")"
        exec("@rule_action(params = act['params'])\n" "def " + act['name'] + args + """ :\n\t""" + act["formulae"])


#take the input rules (common to all)
with open('rules.txt') as f:
    rules = json.load(f)


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

term1 = Products(23,500)
term2 = Products(89,89)
term3 = Products(94,52)


#run Rules (common to all)
for product in Products.getinstances():
    run_all(rule_list=rules,
            defined_variables=ProductVariables(product),
            defined_actions=ProductActions(product),
            stop_on_first_trigger=True
           )


#import use_cases
with open('use_cases.txt') as f:
    use_cases = json.load(f)



"""
To be added later for parameter matching to use case
#load parameters
parameters = {}
#input set of uses cases
with open('use_cases.txt') as f:
    use_cases = json.load(f)
#find the best case and run it's rule
use_case = case_rules(use_cases,parameters):
for case in use_case:
    rules = case['rules']
    #run rules
"""


#take input on which use case to run
case = input()
for x in use_cases :
    if x['name'] == case :
        case = x
        break
if(type(case) == type('')) :
    assert Exception("case not found")
    
#populate date from case variables
class Product :
    def __init__(self) :
        product = collector.Collector()
        self = product.create(case['variables'])

product = Product()

#import prodcut variables from UI
variables = case['variables']


#create ruleVariables
class ProductVariables(BaseVariables):

    def __init__(self, product):
        self.product = product

    for var in variables :
        if var['options'] == 'None' :
            exec("@" + var['field'] + "(" + var['label'] + ")" + """\ndef """ + var['name'] + """(self): \n\treturn """ + var['formulae'])
        else :
            exec("@" + var['field'] + "(" + var['label'] + "," + var['options'] + """)\ndef """ + var['name'] + """(self):\n\treturn """ + var['formulae'])



#import product actions from UI
actions = case['actions']


#Create ruleActions
class ProductActions(BaseActions):

    def __init__(self, product):
        self.product = product

    for act in actions : 
        li = []
        if act['params'] :
            for args in act['params'] :
                li.append(args)
        args = "(self" + ','.join(li) + ")"
        exec("@rule_action(params = act['params'])\n" "def " + act['name'] + args + """ :\n\t""" + act["formulae"])

#run rules
rules = case['rules']
run_all(rule_list=rules,
            defined_variables=ProductVariables(product),
            defined_actions=ProductActions(product),
            stop_on_first_trigger=True
           )
