#API for the Rule based engine

from business_rules.engine import *
from business_rules.variables import *
from business_rules.actions import *
from business_rules.best_case import *
import weakref
import yaml
import business_rules.collector as collector
import threading

log = []

"""
dictionary format for SSH or API source input
parameter_dataSource = {
    'SSH' : {
        'host_name' : '10.137.89.13',
        'user_name' : 'ubuntu',
        'password' : None,
        'key_filename' : 'C:\\Users\\axsingh\\Documents\\Rules-engine.pem',
        'variables' : ["free_mem","total_mem"],
        'multi_thread' : True    
    },
    'API' : {
        'request' : 'get',
        'url' : 'https://ce979fb9-c240-4259-bf6a-6d9de424e291.mock.pstmn.io/get',
        'params' : {},
        'variables' : ["CPU_usage"],
        'multi_thread' : True   
    },
    'API' : {
        'request' : 'post',
        'url' : 'https://50e3b433-59fc-4582-80f2-3d006f1ab57d.mock.pstmn.io/post',
        'params' : {},
        'variables' : ["disk_space"],
        'multi_thread' : True   
    },
    'variables' : ["free_mem","total_mem","CPU_usage","disk_space"]
}
"""

def _run_API(case = "",run_rule = "",parameter_variables = {},parameter_dataSource = {}) :

    global log
    log = []
    def run_rules_tuple(tuples) :
        passed = True

        def run_rules_thread(rule) :
            nonlocal passed

            if type(rule) == type('') :
                if rules[rule]['multi_thread']:
                    if not run(rule = rules[rule],defined_variables = ProductVariables(product),defined_actions = ProductActions(product)) :
                        passed = False
                else:
                    raise Exception("The " + rule + " rule cannot be multi threaded")

            elif type(rule) == type(dict()):
                if not run_rules_dict(rule) :
                    passed = False

            elif type(rule) == type(list()):
                if not run_rules_list(rule):
                    passed = False
                
            else :
                raise Exception("Incorrect rule order in rule: " + rule)

        
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

            else :
                raise Exception("Incorrect rule order in rule: " + rule)

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
        elif 'any' in dicts:
            if run_rules_list(dicts['any'][list(dicts['any'].keys())[0]],list(dicts['any'].keys())[0]):
                return run_rules_list(dicts['then'])
            else :
                return run_rules_list(dicts['else'])
        
        else :
                raise Exception("Incorrect rule order in rule: " + rule)




    #import use cases,rules,variables and actions
    with open("./business_rules/configuration_files/use_cases.yml", 'r') as f:
        use_cases = yaml.load(f, Loader=yaml.FullLoader)
    with open("./business_rules/configuration_files/rules.yml", 'r') as f:
        rules = yaml.load(f, Loader=yaml.FullLoader)
    with open("./business_rules/configuration_files/variables.yml", 'r') as f:
        variables = yaml.load( f, Loader=yaml.FullLoader)
    with open("./business_rules/configuration_files/actions.yml", 'r') as f:
        actions = yaml.load( f, Loader=yaml.FullLoader)

    if case and case in use_cases:
        case = use_cases[case]
    elif case:
        raise Exception("Case not found : " + case)
    if run_rule and run_rule not in rules:
        raise Exception ("Rule not found: " + run_rule)



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
    source_variables = {}
    if run_rule :
        for var in rules[run_rule]['variables']:
            if var not in variables :
                raise Exception("Rule Variable not defined : " + var)
            if var in parameter_dataSource['variables']:
                source_variables[var] = variables[var]
            else:
                variables_list.append(variables[var])
    else :
        for rule in case['rule_list'] :
            for var in rules[rule]['variables'] :
                if variables[var] in variables_list:
                    continue
                if not var in variables :
                    raise Exception("Rule Variable not defined : " + var)
                variables_list.append(variables[var])
    #populate date from case variables
    product = collector.Collector(variables_list,parameter_variables,parameter_dataSource,source_variables)


    #create ruleVariables
    class ProductVariables(BaseVariables):

        def __init__(self, product):
            self.product = product

        try :
            for var in variables_list :
                if var['options'] == 'None' :
                    exec("@" + var['field'] + "(" + var['label'] + ")" + """\ndef """ + var['name'] + """(self): \n\t""" + var['formulae'] + """\n\treturn self.product.""" + var['name'])
                else :
                    exec("@" + var['field'] + "(" + var['label'] + "," + var['options'] + """)\ndef """ + var['name'] + """(self):\n\t""" + var['formulae'] + """\n\treturn self.product.""" + var['name'])
        except Exception as e:
            print("Product Variables couldn't be declared")
            raise e



    #import product actions from UI
    actions_list = []
    if run_rule :
        for act in rules[run_rule]['actions'] :
            if not act in actions :
                    raise Exception("Rule Action not defined : " + act)
            actions_list.append(actions[act])
    else :
        for rule in case['rule_list'] :
            for act in rules[rule]['actions'] :
                if actions[act] in actions_list:
                    continue
                if not act in actions :
                    raise Exception("Rule Action not defined : " + act)
                actions_list.append(actions[act])


    #Create ruleActions
    class ProductActions(BaseActions):

        def __init__(self, product):
            self.product = product

        try :
            for act in actions_list : 
                li = []
                if act['params'] :
                    for args in act['params'] :
                        li.append(args)
                args = "(self" + ','.join(li) + ")"
                exec("@rule_action(params = act['params'])\n" "def " + act['name'] + args + """ :\n\t""" + act["formulae"])
        except Exception as e:
            print("Product Actions couldn't be declared")
            raise e



    #run rules
    try :
        if run_rule:
            run(rule = rules[run_rule], defined_variables = ProductVariables(product), defined_actions = ProductActions(product))
        else :
            run_rules_list(case['rules'])
    except Exception as e:
        print("Couldn't Run Rules Successfully")
        raise e

    return log





