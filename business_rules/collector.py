#collector for collecting and populating the data
import SSH
import collector_API
import data_base
class Collector:

	def __init__(self, variables,parameter_variables = None) :
		
		for var in variables :
			
			if parameter_variables and var['name'] in parameter_variables:
				exec("self." + var['name'] + " = " + var['input_method']['evaluation'] + '(parameter_variables[var["name"]])')
				continue

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