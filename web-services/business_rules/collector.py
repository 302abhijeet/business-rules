#collector for collecting and populating the data
import business_rules.SSH as SSH
import business_rules.collector_API as collector_API
import business_rules.data_base as data_base
import threading
import business_rules.API as API

kill_variable = []

class Collector:
	def _init_source_variables(self,variables,result):
		for var in result:
			try:
				var = variables[var]			
				exec("self." + var['name'] + " = " + var['input_method']['evaluation'] + '(result[var["name"]])')
			except Exception as e:
				API.log.append({
					"Error": "Couldn't init variables: "+var+" in collector module using default",
					"Exception": str(e)
				})
				self._get_value(var)

	def _get_source(self,source,variables) :
		result = {}
		try:
			if source['method'] == "SSH":
				result = SSH._get_file(source,variables)
			elif source['method'] == "API":
				result = collector_API._get_file(source,variables) 
			else :
				raise Exception("source method: "+source['method']+" not found vriables taken from default!")
			self._init_source_variables(variables,result)
		except Exception as e:
			API.log.append({
				"Error": "unable to declare source! variables taken from default",
				"Exception":str(e)
			})
			for var in source['variables']:
				self._get_value(variables[var])



	def _get_value(self,var,parameter_variables= {}) :
		try:
			if parameter_variables and var['name'] in parameter_variables:
				result = parameter_variables[var['name']]
			elif var['input_method']['method'] == 'SSH' :
				result = SSH._get_value(var)
			elif var['input_method']['method'] == "data_base" :
				result = data_base._get_value(var)
			elif var['input_method']['method'] == "API":
				result = collector_API._get_value(var)
			elif var['input_method']['method'] == "derived":
				return
			else :
				API.log.append({"Error":"Variable: "+var+" input method not found: "+var["input_method"]['method']})
			exec("self." + var['name'] + " = " + var['input_method']['evaluation'] + '(result)')
		except Exception as e:
			try:
				API.log.append({
					"Error":"Unable to init variable: "+var['name']+"! Rules with variable will not run!",
					"Exception" : str(e)
				})
				kill_variable.append(var['name'])
			except Exception as e:
				API.log.append({
					"Error":"Variable error:" + str(var),
					"Exception": str(e)
				})

	def __init__(self, variables,parameter_variables = {},parameter_dataSource = [],source_variables = {}) :
		
		threads = []			
		for source in parameter_dataSource:
			if source["multi_thread"]:
				thread = threading.Thread(target = self._get_source, args = (source,source_variables,))
				thread.start()
				threads.append(thread)
			else:
				if threads:
					for thread in threads:
						thread.join()
					threads = []
				self._get_source(source,source_variables)
		
		for var in variables :

			if var['multi_thread'] :
				thread = threading.Thread(target = self._get_value, args = (var,parameter_variables,))
				thread.start()
				threads.append(thread)
			else :
				if threads:
					for thread in threads :
						thread.join()
					threads = []
				self._get_value(var)
		for thread in threads:
			thread.join()
			
			