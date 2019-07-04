#API for the Rule based engine

from business_rules.engine import *
from business_rules.variables import *
from business_rules.actions import *
from business_rules.best_case import *
from datetime import datetime
import business_rules.collector as collector
import weakref
import yaml
import threading
import logging
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString

def _run_API(case = "",run_rule = "",parameter_variables = {},parameter_dataSource = []) :
    """Initiate variables and actions and run Rule/Use-Case
    
    Keyword Arguments:
        case {str} -- case name to be run (default: {""})
        run_rule {str} -- rule ame to be run (default: {""})
        parameter_variables {dict} -- user given values for variables (default: {{}})
        parameter_dataSource {list} -- user given data sources for variables (default: {[]})
    
    Raises:
        NameError: case name not found
        NameError: rule name not found
        RuntimeError: variable for run_rule couldn't take input
        RuntimeError: product variable for run rule couldn't be defined
    
    Returns:
        [dictionary,string] -- output dictionary, detailed xml_report string
    """
    global root 
    global logger
    file_name = "./logs/"+(run_rule or case)+"_"+str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))+".log"
    logging.basicConfig(filename=file_name,format='%(asctime)s %(levelname)s %(message)s',filemode='w')
    logger = logging.getLogger()
    logger.setLevel(20)
    root = ET.Element("Rules_engine")
    error = ET.SubElement(root,"Errors")
    warning = ET.SubElement(root,"Warning")
    rules_report = ET.SubElement(root,"Rules_status")
    logger.info("Starting _run_API")

    global output
    output = []

    def run_rules_tuple(tuples) :
        """run rules in tuples on different threads
        
        Arguments:
            tuples {tuple} -- list of rules to be run on multi-threads
        
        Returns:
            [boolean] -- return weather all rules failed or passed
        """
        passed = True

        def run_rules_thread(rule) :
            """running each element
            
            Arguments:
                rule {str/list/dict} -- rule to be run
            """
            nonlocal passed

            if type(rule) == type('') :
                if rule in kill_rule:
                    passed = False
                else:
                    if rules[rule]['multi_thread']:
                        try:
                            if not run(rule = rules[rule],defined_variables = ProductVariables(product),defined_actions = ProductActions(product)) :
                                logger.info("Rule: {} returned false".format(rule))
                                ET.SubElement(rules_report,rule).text = str("Rule returned false!")
                                passed = False
                            else:
                                logger.info("Rule: {} returned true".format(rule))
                                ET.SubElement(rules_report,rule).text = str("Rule returned true!")
                        except Exception as e:
                            logger.error("Rule: " + rule + " couldn't be run on engine!Error: {}".format(e))
                            ET.SubElement(error,"RuntimeError").text = str("Rule: " + rule + " couldn't be run on engine!Error: {}".format(e))
                            passed = False
                    else:
                        logger.error("The (" + rule + ") rule cannot be multi threaded")
                        ET.SubElement(error,"RuntimeError").text = str("The (" + rule + ") rule cannot be multi threaded")
                        passed = False

            elif type(rule) == type(dict()):
                if not run_rules_dict(rule) :
                    logger.info("Dictionary: {} returned false".format(rule))
                    passed = False
                else:
                    logger.info("Dictionary: {} returned true".format(rule))

            elif type(rule) == type(list()):
                if not run_rules_list(rule):
                    passed = False

        
        threads = []
        for rule in tuples :
            thread = threading.Thread(target = run_rules_thread, args = (rule,),name = rule)
            thread.start()
            logger.info("Started thread: {} for rule: {}!".format(thread.getName(),rule))
            threads.append(thread)
        
        for thread in threads:
            thread.join()
            logger.info("Joined thread: {}!".format(thread.getName()))
            
        return passed



    def run_rules_list(lists,pass_param = None,stop_on_first_success = False, stop_on_first_failure = False) :
        """runs all the rules in the list-lists
        
        Arguments:
            lists {list} -- list of rules to be run
        
        Keyword Arguments:
            pass_param {int} -- number of rules to consider list passed (default: {all})
            stop_on_first_success {bool} -- if list should stop after first rule passes (default: {False})
            stop_on_first_failure {bool} -- if list should stop after first rule fails (default: {False})
        
        Returns:
            [bool] -- retrurns if list passed or failed
        """
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
                        logger.info("Rule: {} returned true".format(rule))
                        ET.SubElement(rules_report,rule).text = str("Rule returned true!")

                        passed += 1
                        if stop_on_first_success:
                            return all_pass
                    else :
                        logger.info("Rule: {} returned false".format(rule))
                        ET.SubElement(rules_report,rule).text = str("Rule returned false!")
                        all_pass = False
                        if stop_on_first_failure:
                            return all_pass
                except Exception as e:
                    logger.error("Rule: " + rule + " couldn't be run on engine!Error: {}".format(e))
                    ET.SubElement(error,"RuntimeError").text = str("Rule: " + rule + " couldn't be run on engine!Error: {}".format(e))
                    all_pass = False


            elif type(rule) == type(dict()):
                if run_rules_dict(rule) :
                    logger.info("Rule conditional: {} returned true!".format(rule))
                    passed += 1
                    if stop_on_first_success:
                        return all_pass
                else :
                    logger.info("Rule conditional: {} returned false!".format(rule))
                    all_pass = False
                    if stop_on_first_failure:
                        return all_pass

            elif type(rule) == type(tuple()):
                if run_rules_tuple(rule) :
                    logger.info("Rule multithread: {} returned true!".format(rule))
                    passed += 1
                    if stop_on_first_success:
                        return all_pass
                else :
                    logger.info("Rule multithread: {} returned false!".format(rule))
                    all_pass = False
                    if stop_on_first_failure:
                        return all_pass

        if pass_param and pass_param <= passed:
            logger.info("List: {} has returned true".format(lists))
            return True
        else :
            logger.info("List: {} has returned {}".format(lists,all_pass))
            return  all_pass



    def run_rules_dict(dicts) :
        """run onditional format rules
        
        Arguments:
            dicts {dict} -- containing conditional rule format
        
        Returns:
            [bool] -- returns weather rule passed or failed
        """
        if 'all' in dicts:
            if run_rules_list(dicts['all']) :
                logger.info("All conditions were satisfied: {}!Running all then rules: {}".format(dicts['all'],dicts['then']))
                ET.SubElement(rules_report,"Dictionary").text = str("All conditions were satisfied: {}!Running all then rules: {}".format(dicts['all'],dicts['then']))
                return run_rules_list(dicts['then'])
            else :
                logger.info("All conditions were NOT satisfied: {}!Running all else rules: {}".format(dicts['all'],dicts['else']))
                ET.SubElement(rules_report,"Dictionary").text = str("All conditions were NOT satisfied: {}!Running all else rules: {}".format(dicts['all'],dicts['else']))
                return run_rules_list(dicts['else'])
        elif 'any' in dicts:
            if run_rules_list(dicts['any'][list(dicts['any'].keys())[0]],pass_param = list(dicts['any'].keys())[0]):
                logger.info("Any condition was satisfied: {}!Running all then rules: {}".format(dicts['any'],dicts['then']))
                ET.SubElement(rules_report,"Dictionary").text = str("Any condition was satisfied: {}!Running all then rules: {}".format(dicts['any'],dicts['then']))
                return run_rules_list(dicts['then'])
            else :
                logger.info("Any condition was satisfied: {}!Running all else rules: {}".format(dicts['any'],dicts['else']))
                ET.SubElement(rules_report,"Dictionary").text = str("Any condition was satisfied: {}!Running all else rules: {}".format(dicts['any'],dicts['else']))
                return run_rules_list(dicts['else'])

    #import use cases,rules,variables and actions
    with open("./business_rules/configuration_files/use_cases.yml", 'r') as f:
        logger.info("Importing use_cases.yml")
        use_cases = yaml.load(f, Loader=yaml.FullLoader)
    with open("./business_rules/configuration_files/rules.yml", 'r') as f:
        logger.info("Importing rules.yml")
        rules = yaml.load(f, Loader=yaml.FullLoader)
    with open("./business_rules/configuration_files/variables.yml", 'r') as f:
        logger.info("Importing variables.yml")
        variables = yaml.load( f, Loader=yaml.FullLoader)
    with open("./business_rules/configuration_files/actions.yml", 'r') as f:
        logger.info("Importing actions.yml")
        actions = yaml.load( f, Loader=yaml.FullLoader)
    with open("./business_rules/configuration_files/DataSource.yml", 'r') as f:
        logger.info("Importing DataSource.yml")
        DataSource = yaml.load( f, Loader=yaml.FullLoader)

    #check if use_case and run_rule defined in config
    if case and case in use_cases:
        logger.info("Use_case created")
        case = use_cases[case]
    elif case:
        logger.critical("Case not defined in config")
        ET.SubElement(error,'NameError').text = str("Case: " + case +" not defined in config!")
        raise NameError(parseString(ET.tostring(root)).toprettyxml())
    if run_rule and run_rule not in rules:
        logger.critical("Rule not defined in config")
        ET.SubElement(error,'NameError').text = str("Rule: " + case +" not defined in config!")
        raise NameError(parseString(ET.tostring(root)).toprettyxml())



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
        try:
            var_set = set(source['variables'])
            if var_set.intersection(source_variables_list) :
                logger.warning(str(var_set.intersection(source_variables_list)) + " variables have been declared again! First source selected")
                ET.SubElement(warning,'MultipleDeclaration').text = str(var_set.intersection(source_variables_list)) + " variables have been declared again! First source selected"
                var_set.difference_update(source_variables_list)
                source['variables'] = list(var_set)
            source_variables_list.extend(var_set)
            for var in var_set:
                variable_source[var] = source
        except Exception as e:
            logger.warning("Data Source by user: {} has error taking variables from default!Error: {}".format(source,e))
            ET.SubElement(warning,"ValueError").text = str("Data Source by user: {} has error taking variables from default!Error: {}".format(source,e))
    logger.info("source_variable_list made :"+str(source_variables_list))

    #Prepare list of variable needed for rules
    if run_rule :
        for var in rules[run_rule]['variables']:
            logger.info("adding variable: "+var)
            variables_list.append(variables[var])
            if var in parameter_variables:
                logger.info("Variable: {} in parameter_variables".format(var))
                if var in source_variables_list:
                    logger.warning("Variable: "+var+" declared in parameters as well as given a source by user!Source selected")
                    ET.SubElement(warning,'RuntimeError').text = str("Variable: "+var+" decalred n parameters as well as given a source by user!Source selected")
                continue
            if var not in source_variables_list:
                if "DataSource" in variables[var]["input_method"]:
                    DataSource[variables[var]["input_method"]["DataSource"]]["variables"].append(var)
            else :
                #to check for unused variables left in defined source variables 
                source_variables_list.remove(var)
    else :
        for rule in case['rule_list'] :
            logger.info("Adding rule: {} variables".format(rule))
            for var in rules[rule]['variables'] :
                logger.info("Adding variable: {} ".format(var))
                if variables[var] in variables_list:
                    logger.info("Variable: {} already in list".format(var))
                    continue
                variables_list.append(variables[var])
                if var in parameter_variables:
                    logger.info("Variable: {} in parameter_variables".format(var))
                    if var in source_variables_list:
                        logger.warning("Variable: "+var+" declared in parameters as well as given a source by user!Source selected")
                        ET.SubElement(warning,'RuntimeError').text = str("Variable: "+var+" decalred n parameters as well as given a source by user!Source selected")
                    continue
                if var not in source_variables_list:
                    if "DataSource" in variables[var]["input_method"]:
                        DataSource[variables[var]["input_method"]["DataSource"]]["variables"].append(var)
                else :
                    #to check for unused variables left in defined source variables
                    source_variables_list.remove(var)

    #To check for extra variables in parameter_Sources
    for var in source_variables_list:
        logger.info("Adding variable: {} to extra!".format(var))
        extra_variables.append(var)
        variable_source[var]['variables'].remove(var)
        if not variable_source[var]['variables'] :
            parameter_dataSource.remove(variable_source[var])
    if extra_variables:
        logger.warning("Extra Variables given :" + str(extra_variables))
        ET.SubElement(warning,'RuntimeError').text = str("Extra Variables given :" + str(extra_variables))

    #Adding datasource to be accessed by collector
    for source in DataSource:
        if DataSource[source]["variables"] :
            logger.info("Addin data source: {} to be populated!".format(source))
            parameter_dataSource.append(DataSource[source])

    #populate data from case variables
    product = collector.Collector(parameter_variables,parameter_dataSource,variables)
    logger.info("variables input taken from collector!")

    #For killing rules whose variables couldn't be fetched
    for var in collector.kill_variable:
        if run_rule:
            logger.critical("Rule cannot run bacause variable: "+var+" not defined!")
            ET.SubElement(error,"RuntimeError").text = str("Rule cannot run bacause variable: "+var+" not defined!")
            raise RuntimeError(parseString(ET.tostring(root)).toprettyxml())
        for rule in case["rule_list"]:
            if var in rules[rule]['variables']:
                logger.error("Rule: "+rule+" will not run because variable: "+var+" couldn't be fetched!")
                ET.SubElement(error,"RuntimeError").text = str("Rule: "+rule+" will not run because variable: "+var+" couldn't be fetched!")
                kill_rule.append(rule)
                

    #create ruleVariables
    class ProductVariables(BaseVariables):

        def __init__(self, product):
            """initialise class object with product variables
            
            Arguments:
                product {object} -- object with variables to be assigned
            """
            self.product = product

        for var in variables_list :
            try:
                if var['options'] == 'None' :
                    exec("@" + var['field'] + "(" + var['label'] + ")" + """\ndef """ + var['name'] + """(self): \n\t""" + var['formulae'] + """\n\treturn self.product.""" + var['name'])
                else :
                    exec("@" + var['field'] + "(" + var['label'] + "," + var['options'] + """)\ndef """ + var['name'] + """(self):\n\t""" + var['formulae'] + """\n\treturn self.product.""" + var['name'])
                logger.info("Product Vriable: {} has been created!".format(var['name']))
            except Exception as e:
                if run_rule:
                    logger.error("Product Variable: " + var['name'] + " could not be defined hence rule:" + run_rule + " cannot run!Error: {}".format(e))
                    ET.SubElement(error,"RuntimeError").text = str("Product Variable: " + var['name'] + " could not be defined hence rule:" + run_rule + " cannot run!Error: {}".format(e))
                    raise RuntimeError(parseString(ET.tostring(root)).toprettyxml())
                for rule in case['rule_list']:
                    if var['name'] in rules[rule]['variables']:
                        kill_rule.append(rule)
                        logger.error("Product Variable: " + var['name'] + " could not be defined hence rule:" +rule+" cannot run and will return false!Error: {}".format(e))
                        ET.SubElement(error,"RuntimeError").text = str("Product Variable: " + var['name'] + " could not be defined hence rule:" + rule + "  cannot run and will return false!Error: {}".format(e))



    #import product actions from UI
    actions_list = []
    if run_rule :
        for act in rules[run_rule]['actions'] :
            logger.info("Adding action : {} to list!".format(act))
            actions_list.append(actions[act])
    else :
        for act in case["actions"]:
            logger.info("Adding action : {} to list!".format(act))
            if actions[act] in actions_list:
                logger.info("Action : {} already in list!".format(act))
                continue
            actions_list.append(actions[act])
        for rule in case['rule_list'] :
            for act in rules[rule]['actions'] :
                logger.info("Adding action : {} to list!".format(act))
                if actions[act] in actions_list:
                    logger.info("Action : {} already in list!".format(act))
                    continue
                actions_list.append(actions[act])


    #Create ruleActions
    class ProductActions(BaseActions):

        def __init__(self, product):
            """initialise class object with product actions
            
            Arguments:
                product {object} -- product with input variables
            """
            self.product = product

        for act in actions_list : 
            try:
                li = []
                if act['params'] :
                    for args in act['params'] :
                        li.append(args+"=None")
                args = "(self," + ','.join(li) + ")"
                exec("@rule_action(params = act['params'])\n" "def " + act['name'] + args + """ :\n\t""" + act["formulae"])
                logger.info("Creater Product action : {} successfully!".format(act['name']))
            except Exception as e:
                if run_rule:
                    logger.warning("Product Action: " + act['name'] + " could not be defined hence rule:" + run_rule + " will not run that action!Error: {}".format(e))
                    ET.SubElement(warning,"RuntimeError").text = str("Product Action: " + act['name'] + " could not be defined hence rule:" + run_rule + " will not run that action!Error: {}".format(e))
                if act['name'] in case["actions"]:
                    logger.warning("Product Action: " + act['name'] + " could not be defined hence case will not run that action!Error: {}".format(e))
                    ET.SubElement(warning,"RuntimeError").text = str("Product Action: " + act['name'] + " could not be defined hence case will not run that action!Error: {}".format(e))
                for rule in case['rule_list']:
                    if act['name'] in rules[rule]['actions']:
                        for act_true in rules[rule]['actions_true']:
                            if act['name'] == act_true['name']:
                                rules[rule]['actions_true'].remove(act_true)
                        for act_false in rules[rule]['actions_false']:
                            if act['name'] == act_false['name']:
                                rules[rule]['actions_false'].remove(act_false)
                        logger.warning("Product Action: " + act['name'] + " could not be defined hence rule:" + rule + " will not run that action!Error: {}".format(e))
                        ET.SubElement(warning,"RuntimeError").text = str("Product Action: " + act['name'] + " could not be defined hence rule:" + rule + " will not run that action!Error: {}".format(e))



    #run rules
    try :
        if run_rule:
            if run(rule = rules[run_rule], defined_variables = ProductVariables(product), defined_actions = ProductActions(product)):
                logger.info("Rule has retuned true!")
                ET.SubElement(rules_report,run_rule).text = str("Rule has returned true!")
            else:
                logger.info("Rule has retuned false!")
                ET.SubElement(rules_report,run_rule).text = str("Rule has returned false!")
        else :
            if run_rules_list(case['rules'],stop_on_first_success=case["stop_on_first_success"],stop_on_first_failure = case["stop_on_first_failure"]) :
                do_actions(case["actions_true"], defined_actions = ProductActions(product))
            else :
                do_actions(case["actions_false"], defined_actions = ProductActions(product))
    except Exception as e:
        logger.critical("Couldn't run rules on engine!Error: {}".format(e))
        ET.SubElement(error,"RuntimeError").text = "Couldn't run rules on engine!Error: {}".format(e)
    if logger.handlers:
        for handler in logger.handlers:
            logger.removeHandler(handler)
    return output,parseString(ET.tostring(root)).toprettyxml()





