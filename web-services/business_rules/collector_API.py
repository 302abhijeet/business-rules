#API module

import requests
def _run_get(var) :
	response = requests.get(var['input_method']['url'], params = var['input_method']['params'])
	
	ldict = locals()
	exec("out = " + var['input_method']['command'],globals(),ldict)
	out = ldict['out']

	if not response :
		assert Exception(response)

	#have to make changes here
	if var['input_method']['start'] or var['input_method']['end'] :
		out = out[var["input_method"]['start']:var["input_method"]['end']]
	return out

def _run_post(var):
	response = requests.post(var['input_method']['url'], params = var['input_method']['params'],data = var['input_method']['data'])
	
	ldict = locals()
	exec("out = " + var['input_method']['command'],globals(),ldict)
	out = ldict['out']

	if not response :
		assert Exception(response)

	#have to make changes here
	if var['input_method']['start'] or var['input_method']['end'] :
		out = out[var["input_method"]['start']:var["input_method"]['end']]
	return out


def _get_value(var = []):

	if var["input_method"]['request'] == 'get':
		return _run_get(var)

	elif var["input_method"]['request'] == 'post':
		return _run_post(var)
		
	