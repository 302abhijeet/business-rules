#API module

import requests
def _get_value():
	response = requests.get(var['input_method']['url'], params = var['input_method']['params'])
	exec("out = " + var['input_method']['command'],locals(),globals())

	#have to make changes here
	if  var["input_method"]['evaluation'] and type(response) is not type(exec(var["input_method"]['evaluation'])) :
		raise Exception("evaluation criteria not met")
	else :
		if var['input_method']['start'] or var['input_method']['end'] :
			out = out[var["input_method"]['start']:var["input_method"]['end']]
		return out