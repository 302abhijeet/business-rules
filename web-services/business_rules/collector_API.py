#API module

import requests
def _get_value(var = []):
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