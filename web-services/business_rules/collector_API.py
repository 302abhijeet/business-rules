#API module

import requests
def _get_variable_output(var,response) :
	try: 
		ldict = locals()
		exec("out = " + var['input_method']['command'],globals(),ldict)
		out = ldict['out']
	except Exception as e:
		print(var['name'] + " Error in API commands:" + var['input_method']['command'])
		raise e
	if not response :
		raise Exception(response)
	#have to make changes here
	try :
		if var['input_method']['start'] or var['input_method']['end'] :
			out = out[var["input_method"]['start']:var["input_method"]['end']]
	except Exception as e:
		print(var['name'] + " Error in API splitting of variable: ")
		raise e
	return out


def _get_file(source,variables):
	if var["input_method"]['request'] == 'get':
		response = requests.get(var['input_method']['url'], params = var['input_method']['params'])
	elif var["input_method"]['request'] == 'post':
		response = requests.post(var['input_method']['url'], params = var['input_method']['params'],data = var['input_method']['data'])
	for var in source['variables']:
		result[var] = _get_variable_output(variables[var],response)
	return result

def _get_value(var = []):
	if var["input_method"]['request'] == 'get':
		response = requests.get(var['input_method']['url'], params = var['input_method']['params'])
	elif var["input_method"]['request'] == 'post':
		response = requests.post(var['input_method']['url'], params = var['input_method']['params'],data = var['input_method']['data'])
	return _get_variable_output(var,response)
		
	