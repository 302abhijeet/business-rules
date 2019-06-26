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
					"Error":"Unable to init variable: "+var['name']+"! Rules with variable will not run!",
					"Exception" : str(e)
				})
				kill_variable.append(var['name'])

	def _get_source(self,source,variables) :
		result = {}
		try:
			if source['method'] == "SSH":
				result = SSH._get_file(source,variables)
			elif source['method'] == "API":
				result = collector_API._get_file(source,variables) 
			elif source['method'] == "data_base":
				result = data_base._get_file(source,variables)
			else :
				raise Exception("source method: "+source['method']+" not found variables will not run!")
			self._init_source_variables(variables,result)
		except Exception as e:
			API.log.append({
				"Error": "Unable to declare source host: "+source["method"]+"! Rules with variables in source will not run",
				"Exception":str(e)
			})
			for var in source['variables']:
				kill_variable.append(variables[var]['name'])


	def __init__(self,parameter_variables = {},parameter_dataSource = [],variables = {}) :
		
		threads = []			
		for source in parameter_dataSource:
			if source["multi_thread"]:
				thread = threading.Thread(target = self._get_source, args = (source,variables))
				thread.start()
				threads.append(thread)
			else:
				if threads:
					for thread in threads:
						thread.join()
					threads = []
				self._get_source(source,variables)
		
		for var in parameter_variables :
			result = parameter_variables[var]
			var = variables[var]
			exec("self." + var['name'] + " = " + var['input_method']['evaluation'] + '(result)')
			
		for thread in threads:
			thread.join()
			
			