#SSH module

import paramiko

def _start_connection(source) :
	ssh_client=paramiko.SSHClient()
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh_client.connect(hostname = source['host_name'],username=source['user_name'],password=source['password'],key_filename = source['key_filename'])
	return ssh_client

def _get_variable_output(var,ssh_client) :
	stdin,stdout,stderr=ssh_client.exec_command(var["input_method"]['command'])
	if stderr.readlines() :
		ex = stderr.readlines()
		raise Exception(ex)
	if var['input_method']['start'] or var['input_method']['end'] :
		try:
			out = stdout.readlines()[0]
			if type(var['input_method']['start']) == type(int()) :
				out = out[var['input_method']['start']:var['input_method']['end']]
			else :
				out = out[out.index(var["input_method"]['start']) +1:out.index(var["input_method"]['end'])]
		except Exception as e:
			print(var['name'] + " Error in SSH splitting of variable: ")
			raise e
	else :
		out = stdout.readlines()[0]
	return out


def _get_file(source, variables):
	ssh_client = _start_connection(source)
	result = {}
	for var in source['variables']:
		result[var] = _get_variable_output(variables[var],ssh_client)
	return result


def _get_value(var) :
	ssh_client = _start_connection(var['input_method'])
	return _get_variable_output(var,ssh_client)
		
		