#API for the Rule based engine

from business_rules.engine import *
from business_rules.variables import *
from business_rules.actions import *
from business_rules.best_case import *
import weakref
import yaml
import threading

log = []

import business_rules.collector as collector

"""
#have to delete later
    parameter_dataSource = [
        {
            'method' : 'SSH',
            'host_name' : '10.137.89.13',
            'user_name' : 'ubuntu',
            'password' : None,
            'key_filename' : 'C:\\Users\\axsingh\\Documents\\Rules-engine.pem',
            'variables' : ["free_mem","total_mem"],
            'multi_thread' : True    
        },
        {
            'method' : "API",
            'request' : 'get',
            'url' : 'https://ce979fb9-c240-4259-bf6a-6d9de424e291.mock.pstmn.io/get',
            'params' : {},
            'variables' : ["CPU_usage"],
            'multi_thread' : True   
        },
        {
            'method' : "API",
            'request' : 'post',
            'url' : 'https://50e3b433-59fc-4582-80f2-3d006f1ab57d.mock.pstmn.io/post',
            'params' : {},
            'data' : { "method" : "POST", "value" : 13},
            'variables' : ["disk_space"],
            'multi_thread' : True   
        }
    ]
"""

def _run_API(case = "",run_rule = "",parameter_variables = {},parameter_dataSource = []) :
    global log
    log = []
    def run_rules_tuple(tuples) :
        passed = True

        def run_rules_thread(rule) :
            nonlocal passed

            if type(rule) == type('') :
                if rule in kill_rule:
                    passed = False
                else:
                    if rules[rule]['multi_thread']:
                        try:
                            if not run(rule = rules[rule],defined_variables = ProductVariables(product),defined_actions = ProductActions(product)) :
                                passed = False
                        except Exception as e:
                            log.append({
                                "Error" : "Rule: " + rule + "Cannot be run on engine!",
                                "Exception" : str(e)
                            })
                            passed = False
                    else:
                        log.append({"Error" : "The (" + rule + ") rule cannot be multi threaded"})
                        passed = False

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
                if rule in kill_rule:
                    all_pass = False
                    continue
                try:
                    if run(rule = rules[rule],defined_variables = ProductVariables(product),defined_actions = ProductActions(product)) :
                        passed += 1
                    else :
                        all_pass = False
                except Exception as e:
                    log.append({
                        "Error" : "Rule: " + rule + " couldn't be run on engine!",
                        "Exception": str(e)
                    })
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
                log.append({"Error" : "Incorrect rule order in rule: " + rule})
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
            log.append({"Error" : "Incorrect rule order in rule: " + rule})
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
    with open("./business_rules/configuration_files/DataSource.yml", 'r') as f:
        DataSource = yaml.load( f, Loader=yaml.FullLoader)

    if case and case in use_cases:
        case = use_cases[case]
    elif case:
        log.append({"Error" : "Case not found: " + case})
        raise Exception("Case not found : " + case)
    if run_rule and run_rule not in rules:
        log.append({"Error" : "Rule not found: " + run_rule})
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

    kill_rule = []    #variable for storing rules to be killed

    #import prodcut variables from UI
    variables_list = []
    source_variables_list = []
    extra_variables = []
    variable_source = {}
    #To make a list of source variables and check for duplication
    for source in parameter_dataSource:
        var_set = set(source['variables'])
        if var_set.intersection(source_variables_list) :
            log.append({"Error" : str(var_set.intersection(source_variables_list)) + " variables have been declared again! First source selected"})
            var_set.difference_update(source_variables_list)
            source['variables'] = list(var_set)
        source_variables_list.extend(var_set)
        for var in var_set:
            variable_source[var] = source

    #Prepare list of variable needed for rules
    if run_rule :
        for var in rules[run_rule]['variables']:
            if var not in variables :
                log.append({"Error" : "Rule Variable not defined : " + var})
                raise Exception("Rule Variable not defined : " + var)
            variables_list.append(variables[var])
            if var in parameter_variables:
                if var in source_variables_list:
                    log.append({"Error": "Variable: "+var+" decalred n parameters as well as given a source by user!"})
                continue
            if var not in source_variables_list:
                if "DataSource" in variables[var]["input_method"]:
                    DataSource[variables[var]["input_method"]["DataSource"]]["variables"].append(var)
            else :
                source_variables_list.remove(var)
    else :
        for rule in case['rule_list'] :
            if rule not in rules:
                log.append({"Error" : "Rule not defined : " + var})
                raise Exception("Rule not defined : " + rule)
            for var in rules[rule]['variables'] :
                if var not in variables:
                    log.append({"Error" : var + " variable not declared hence rule ("+rule+") cannot run"})
                    kill_rule.append(rule)
                    break
                if variables[var] in variables_list:
                    continue
                variables_list.append(variables[var])
                if var in parameter_variables:
                    if var in source_variables_list:
                        log.append({"Error": "Variable: "+var+" decalred n parameters as well as given a source by user!"})
                    continue
                if var not in source_variables_list:
                    if "DataSource" in variables[var]["input_method"]:
                        DataSource[variables[var]["input_method"]["DataSource"]]["variables"].append(var)
                else :
                    source_variables_list.remove(var)

    #To check for extra variables in parameter_Sources
    for var in source_variables_list:
        extra_variables.append(var)
        variable_source[var]['variables'].remove(var)
        if not variable_source[var]['variables'] :
            parameter_dataSource.remove(variable_source[var])
    if extra_variables:
        log.append({"Extra Variables given :" : extra_variables})

    for source in DataSource:
        if DataSource[source]["variables"] :
            parameter_dataSource.append(DataSource[source])
    #populate data from case variables
    product = collector.Collector(parameter_variables,parameter_dataSource,variables)

    #For killing rules whose variables couldn't be fetched
    for var in collector.kill_variable:
        for rule in case["rule_list"]:
            if var in rules[rule]['variables']:
                log.append({"Error" : "Rule: "+rule+" will not run because variable: "+var+" couldn't be fetched!"})
                kill_rule.append(rule)
                

    #create ruleVariables
    class ProductVariables(BaseVariables):

        def __init__(self, product):
            self.product = product

        for var in variables_list :
            try:
                if var['options'] == 'None' :
                    exec("@" + var['field'] + "(" + var['label'] + ")" + """\ndef """ + var['name'] + """(self): \n\t""" + var['formulae'] + """\n\treturn self.product.""" + var['name'])
                else :
                    exec("@" + var['field'] + "(" + var['label'] + "," + var['options'] + """)\ndef """ + var['name'] + """(self):\n\t""" + var['formulae'] + """\n\treturn self.product.""" + var['name'])
            except Exception as e:
                if run_rule:
                    log.append({
                        "Error" : "Product Variable: " + var['name'] + " could not be defined hence rule:" + run_rule + " cannot run!",
                        "Exception" : e
                    })
                    raise e
                for rule in case['rule_list']:
                    if var['name'] in rules[rule]['variables']:
                        kill_rule.append(rule)
                        log.append({
                            "Error": "Product Variable: "+var['name']+" couldn't be declared hence rule: "+rule+"will not run and return false output",
                            "Exception": str(e)
                        })



    #import product actions from UI
    actions_list = []
    if run_rule :
        for act in rules[run_rule]['actions'] :
            if not act in actions :
                log.append("Cannot run rule:" + run_rule + 'because action: ' + act)
                raise Exception("Rule Action not defined : " + act)
            actions_list.append(actions[act])
    else :
        for rule in case['rule_list'] :
            for act in rules[rule]['actions'] :
                if not act in actions :
                    log.append({"Error" : "Cannot run rule:" + rule + 'because action: ' + act})
                    kill_rule.append(rule)
                    break
                if actions[act] in actions_list:
                    continue
                actions_list.append(actions[act])


    #Create ruleActions
    class ProductActions(BaseActions):

        def __init__(self, product):
            self.product = product

        for act in actions_list : 
            try:
                li = []
                if act['params'] :
                    for args in act['params'] :
                        li.append(args)
                args = "(self," + ','.join(li) + ")"
                exec("@rule_action(params = act['params'])\n" "def " + act['name'] + args + """ :\n\t""" + act["formulae"])
            except Exception as e:
                if run_rule:
                    log.append({
                        "Error" : "Product Action: " + act['name'] + " could not be defined hence rule:" + run_rule + " cannot run!",
                        "Exception" : e
                    })
                    raise e
                for rule in case['rule_list']:
                    if act['name'] in rules[rule]['actions']:
                        for act_true in rules[rule]['actions_true']:
                            if act['name'] == act_true['name']:
                                rules[rule]['actions_true'].remove(act_true)
                        for act_false in rules[rule]['actions_false']:
                            if act['name'] == act_false['name']:
                                rules[rule]['actions_false'].remove(act_false)
                        log.append({
                            "Error": "Product Action: "+act['name']+" couldn't be declared hence rule: "+rule+" will not run that action!",
                            "Exception": str(e)
                        })



    #run rules
    try :
        if run_rule:
            run(rule = rules[run_rule], defined_variables = ProductVariables(product), defined_actions = ProductActions(product))
        else :
            run_rules_list(case['rules'])
    except Exception as e:
        log.append({
            "Error " : "Couldn't run rules in engine",
            "Exception" : str(e)
        })

    return log





