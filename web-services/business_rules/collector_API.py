#API module

import requests
def _get_variable_output(var,response) :
	if not response :
		raise Exception("invalid request to API! Faulty response!\n" + str(response))
	try: 
		ldict = locals()
		exec("out = " + var['input_method']['command'],globals(),ldict)
		out = ldict['out']
	except Exception as e:
		raise Exception(var['name'] + " Error in API commands:" + var['input_method']['command']+"\n"+str(e))
	#have to make changes here
	try :
		if var['input_method']['start'] or var['input_method']['end'] :
			out = out[var["input_method"]['start']:var["input_method"]['end']]
	except Exception as e:
		raise Exception("Error in API splitting of variable: "+var['name']+"\n"+str(e))
	return out


def _get_file(source,variables):
	result = {}
	try:
		if source['request'] == 'get':
			response = requests.get(source['url'], params = source['params'])
		elif source['request'] == 'post':
			response = requests.post(source['url'], params = source['params'],data = source['data'])
		else:
			raise Exception("request method not defined: "+ source['request'])
	except Exception as e:
		raise Exception("API Source unable to connect\n"+str(e))
	for var in source['variables']:
		result[var] = _get_variable_output(variables[var],response)
	return result

def _get_value(var = []):
	try :
		if var["input_method"]['request'] == 'get':
			response = requests.get(var['input_method']['url'], params = var['input_method']['params'])
		elif var["input_method"]['request'] == 'post':
			response = requests.post(var['input_method']['url'], params = var['input_method']['params'],data = var['input_method']['data'])
		else:
			raise Exception("request method not defined: "+ source['request'])
	except Exception as e:
		raise Exception("API Source unable to connect\n"+str(e))
	return _get_variable_output(var,response)
		
	