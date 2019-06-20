#API for the Rule based engine

from business_rules.engine import *
from business_rules.variables import *
from business_rules.actions import *
from business_rules.best_case import *
import weakref
import yaml
import business_rules.collector as collector
import threading

def _run_API(case = "case2",run_rule = None,parameter_variables = {}) :
    #have to add functionality for multithreading
    def run_rules_tuple(tuples) :
        passed = True

        def run_rules_thread(rule) :
            nonlocal passed

            if type(rule) == type('') :
                if rules[rule]['multi_thread']:
                    if not run(rule = rules[rule],defined_variables = ProductVariables(product),defined_actions = ProductActions(product)) :
                        passed = False
                else:
                    raise Exception(print("Rule cannot be multi threaded"))
                    exit()

            elif type(rule) == type(dict()):
                if not run_rules_dict(rule) :
                    passed = False

            elif type(rule) == type(list()):
                if not run_rules_list(rule):
                    passed = False

        
        threads = []
        for rule in tuples :
            thread = threading.Thread(target = run_rules_thread, args = (rule,))
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()
            
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




    #import use cases,rules,variables and actions
    with open("./business_rules/configuration_files/use_cases.yml", 'r') as f:
        use_cases = yaml.load(f)
    with open("./business_rules/configuration_files/rules.yml", 'r') as f:
        rules = yaml.load(f)
    with open("./business_rules/configuration_files/variables.yml", 'r') as f:
        variables = yaml.load( f)
    with open("./business_rules/configuration_files/actions.yml", 'r') as f:
        actions = yaml.load( f)
    if case :
        case = use_cases[case]



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


    #import prodcut variables from UI
    variables_list = []
    if run_rule :
        for var in rules[run_rule]['variables'] :
            variables_list.append(variables[var])
    else :
        for rule in case['rule_list'] :
            for var in rules[rule]['variables'] :
                variables_list.append(variables[var])
    #populate date from case variables
    product = collector.Collector(variables_list,parameter_variables)


    #create ruleVariables
    class ProductVariables(BaseVariables):

        def __init__(self, product):
            self.product = product

        for var in variables_list :
            if var['options'] == 'None' :
                exec("@" + var['field'] + "(" + var['label'] + ")" + """\ndef """ + var['name'] + """(self): \n\treturn """ + var['formulae'])
            else :
                exec("@" + var['field'] + "(" + var['label'] + "," + var['options'] + """)\ndef """ + var['name'] + """(self):\n\treturn """ + var['formulae'])



    #import product actions from UI
    actions_list = []
    if run_rule :
        for act in rules[run_rule]['actions'] :
            actions_list.append(actions[act])
    else :
        for rule in case['rule_list'] :
            for act in rules[rule]['actions'] :
                actions_list.append(actions[act])


    #Create ruleActions
    class ProductActions(BaseActions):

        def __init__(self, product):
            self.product = product

        for act in actions_list : 
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





