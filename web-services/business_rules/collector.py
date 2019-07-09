#collector for collecting and populating the data
import business_rules.SSH as SSH
import business_rules.collector_API as collector_API
import business_rules.data_base as data_base
import threading
import business_rules.API as API
import xml.etree.ElementTree as ET
from pymongo import MongoClient

kill_variable = []
var_report = None
class Collector:
    def _init_source_variables(self,variables,result,source):
        """initialise product variable with input value
        
        Arguments:
            variables {dict} -- variables in config file
            result {dict} -- input values obtained for variables
            source {dict} -- source of variables
        
        Raises:
            result: error in obtaining variable from source
        """
        for var in result:
            try:
                if isinstance(result[var],Exception):
                	raise result[var]	
                exec("self." + var + " = " + variables[var]['input_method']['evaluation'] + '(result[var])')
                API.logger.info("Variable: {} has been created!Value: {}!Source: {}".format(var,result[var],source))
                ET.SubElement(var_report,var, source = source).text = str(result[var])
            except Exception as e:
                API.logger.error("Unable to initiate variable: {}! Rules with variable will not run!Error: {}".format(var,e))
                ET.SubElement(API.root[0],"RuntimeError").text = str("Unable to initiate variable: {}! Rules with variable will not run!Error: {}".format(var,e))
                kill_variable.append(var)

    def _get_source(self,source,variables) :
        """connect to source and get vlues for input variables
        
        Arguments:
            source {dict} -- source to be connected to
            variables {dict} -- variables in config file
        
        Raises:
            NameError: source method is not defined
        """
        result = {}
        mydb = MongoClient("localhost",27017)[API.database]
        if source["cache"]:
            result = mydb["cache"].find_one({"name":source['name']},{"_id":0,"result":1})
            if result and set(source['variables']).issubset(result['result'].keys()):
                API.logger.info("Variables : {} of Source : {} taken from cache!".format(source['variables'],source["name"]))
                ET.SubElement(API.root[1],"INFO").text = str("Variables: {} of Source: {} taken from cache!".format(source['variables'],source["name"]))
                result = result["result"]
                return self._init_source_variables(variables,result,source['name'])
        try:
            if source['method'] == "SSH":
                result = SSH._get_file(source,variables)
            elif source['method'] == "API":
                result = collector_API._get_file(source,variables) 
            elif source['method'] == "data_base":
                result = data_base._get_file(source,variables)
            else :
                API.logger.error("source method: {} not found!".format(source['method']))
                raise NameError("source method: "+source['method']+" not found!")
            API.logger.info("Source: {} fetched variables: {}".format(source['name'],result))
            mydb["cache"].update_one({"name":source['name']},{"$set":{"result":result}},upsert=True)
        except Exception as e:
            result = mydb["cache"].find_one({"name":source['name']},{"_id":0,"result":1}) or {}
            if result:
                result = result['result']
                API.logger.warning("Unable to connect to source host: {}! Source Variables will be taken from cache: {}! Error: {}".format(source['name'],source["variables"],e))
                ET.SubElement(API.root[1],"RuntimeError").text = str("Unable to connect to source host: {}! Source variables in source will be taken from cache: {}! Error: {}".format(source['name'],source["variables"],e))
                if not source["cache"]:
                    for var in result:
                        if not variables[var]["cache"] or var not in result:
                            result[var] = RuntimeError("Variable cannot be cached!")
                            kill_variable.append(var)
                
            else:
                API.logger.error("Unable to connect to source host: {}! Rules with variables in source will not run: {}! Error: {}".format(source['name'],source["variables"],e))
                ET.SubElement(API.root[0],"RuntimeError").text = str("Unable to connect to source host: {}! Rules with variables in source will not run: {}! Error: {}".format(source['name'],source["variables"],e))
                for var in source['variables']:
                    kill_variable.append(variables[var]['name'])
        self._init_source_variables(variables,result,source['name'])


    def __init__(self,parameter_variables = {},parameter_dataSource = [],variables = {}) :
        """initialise product with input variables
        
        Keyword Arguments:
            parameter_variables {dict} -- user defined values for variables (default: {{}})
            parameter_dataSource {list} -- data sources to fetch input values from (default: {[]})
            variables {dict} -- variables in config file (default: {{}})
        """
        API.logger.info("starting collector module")
        global var_report
        var_report = ET.SubElement(API.root,"Variables")
        global kill_variable
        kill_variable = []
        threads = []			
        for source in parameter_dataSource:
            API.logger.info("Getting data source: {} variables!".format(source['name']))
            if "multi_thread" not in source:
                API.logger.error("Incorrect format for Source host: {}! Rules with variables in source will not run: {}!".format(source['name'],source["variables"]))
                ET.SubElement(API.root[0],'KeyError').text=  str("multi_thread not in source: {}!Rules with variables will not run: {}".format(source['name'],source["variables"]))
                for var in source['variables']:
                    kill_variable.append(variables[var]['name'])
                continue
            if source["multi_thread"]:
                thread = threading.Thread(target = self._get_source, args = (source,variables),name=source['name'])
                API.logger.info("Starting thread: {}".format(thread.getName()))
                thread.start()
                threads.append(thread)
            else:
                if threads:
                    for thread in threads:
                        thread.join()
                        API.logger.info("Joining thread: {}".format(thread.getName()))
                    threads = []
                self._get_source(source,variables)
            
		
        for var in parameter_variables :
            result = parameter_variables[var]
            var = variables[var]
            try:
                exec("self." + var['name'] + " = " + var['input_method']['evaluation'] + '(result)')
                API.logger.info("Variable: {} has been created!Value: {}!Source: Parameter_Variable".format(var['name'],result))
                ET.SubElement(var_report,var['name'],source="Parameter_Variable").text = result
            except Exception as e:
                API.logger.error("Variable: {} couldn't be declared!Rules with variable will not run!Error: {}".format(var,e))
                ET.SubElement(API.root[0],"RuntimeError").text = str("Variable: {} couldn't be declared!Rules with variable will not run!Error: {}".format(var,e))
			
        for thread in threads:
            thread.join()
			
			