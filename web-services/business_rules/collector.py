#collector for collecting and populating the data
import business_rules.SSH as SSH
import business_rules.collector_API as collector_API
import business_rules.data_base as data_base
import threading
class Collector:
	def _init_source_variables(self,variables,result):
		for var in result:
			var = variables[var]
			exec("self." + var['name'] + " = " + var['input_method']['evaluation'] + '(result[var["name"]])')

	def _get_source(self,source,variables) :
		if source['method'] == "SSH":
			result = SSH._get_file(source,variables)
		elif source['method'] == "API":
			result = collector_API._get_file(source,variables) 
		else :
			raise Exception("parameter_source Data not found in methods: ")
		self._init_source_variables(variables,result)


	def _get_value(self,var,parameter_variables= {}) :
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
			raise Exception(var['input_method']['method'] + " Not found")
		exec("self." + var['name'] + " = " + var['input_method']['evaluation'] + '(result)')


	def __init__(self, variables,parameter_variables = {},parameter_dataSource = [],source_variables = {}) :
		
		threads = []			
		for source in parameter_dataSource:
			print(source["method"])
			thread = threading.Thread(target = self._get_source, args = (source,source_variables,))
			thread.start()
			threads.append(thread)
		
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
			
			