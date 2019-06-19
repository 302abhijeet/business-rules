#API for the Rule based engine

from engine import *
from variables import *
from actions import *
from best_case import *
import weakref
import json
import collector
import rules_config


#have to add functionality for multithreading
def run_rules_tuple(tuples) :
    passed = True
    for rule in tuples :

        if type(rule) == type('') :
            if not run(rule = rules[rule],defined_variables = ProductVariables(product),defined_actions = ProductActions(product)) :
                passed = False

        elif type(rule) == type(dict()):
            if not run_rules_dict(rule) :
                passed = False

        elif type(rule) == type(list()):
            if not run_rules_list(rule):
                passed = False
    return passed



def run_rules_list(lists,pass_param = None) :
    passed = 0
    all_pass = True
    if not lists :
        return True
    for rule in lists :

        if type(rule) == type('') :
            if run(rule = rules[rule],defined_variables = ProductVariables(product),defined_actions = ProductActions(product)) :
                passed += 1
            else :
                all_pass = False

        elif type(rule) == type(dict()):
            if run_rules_dict(rule) :
                passed += 1
            else :
                all_pass = False

        elif type(rule) == type(tuple()):
            if run_rules_tuple(rule) :
                passed += 1
            else :
                all_pass = False

    if pass_param and pass_param <= passed:
        return True
    else :
        return  all_pass



def run_rules_dict(dicts) :
    if 'all' in dicts:
        if run_rules_list(dicts['all']) :
            return run_rules_list(dicts['then'])
        else :
            return run_rules_list(dicts['else'])
    else:
        if run_rules_list(dicts['any'][list(dicts['any'].keys())[0]],list(dicts['any'].keys())[0]):
            return run_rules_list(dicts['then'])
        else :
            return run_rules_list(dicts['else'])



#import use cases and rules
use_cases = rules_config.use_cases
rules = rules_config.rules



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
print("Enter use case and rule:")
case = input()
run_rule = input()
if case in use_cases :
    case = use_cases[case]
else  :
    assert Exception(print("use case not found"))
    exit()


#import prodcut variables from UI
variables = []
for rule in case['rule_list'] :
    for var in rules[rule]['variables']:
        variables.append(var)

#populate date from case variables
product = collector.Collector(variables)


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
actions = []
for rule in case['rule_list'] :
    for act in rules[rule]['actions']:
        actions.append(act)


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
if run_rule:
    run(rule = rules[run_rule], defined_variables = ProductVariables(product), defined_actions = ProductActions(product))
else :
    run_rules_list(case['rules'])





