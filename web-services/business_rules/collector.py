#collector for collecting and populating the data
import business_rules.SSH as SSH
import business_rules.collector_API as collector_API
import business_rules.data_base as data_base
import threading
class Collector:
	def _get_value(self,var,parameter_variables= None) :
		if parameter_variables and var['name'] in parameter_variables:
			exec("self." + var['name'] + " = " + var['input_method']['evaluation'] + '(parameter_variables[var["name"]])')
			return

		if var['input_method']['method'] == 'SSH' :
			exec("self." + var['name'] + " = " + var['input_method']['evaluation'] + '(SSH._get_value(var))')

		elif var['input_method']['method'] == "data_base" :
			exec("self." + var['name'] + " = " + var['input_method']['evaluation'] + '(data_base._get_value(var))')


		elif var['input_method']['method'] == "API":
			exec("self." + var['name'] + " = " + var['input_method']['evaluation'] + '(collector_API._get_value(var))')
		

		elif var['input_method']['method'] == "data_bus":
			pass

		else :
			raise Exception(print(var['input_method']['method'] + " Not found"))
			exit()

	def __init__(self, variables,parameter_variables = None) :
		
		threads = []
		for var in variables :

			if var['multi_thread'] :
				thread = threading.Thread(target = self._get_value, args = (var,parameter_variables,))
				thread.start()
				threads.append(thread)
			else :
				_get_value(var)

		for thread in threads :
			thread.join()
			
			