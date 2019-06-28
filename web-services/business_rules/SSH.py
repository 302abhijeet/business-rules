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
			raise Exception(var['name'] + " Error in SSH splitting of variable: " + str(e))
	else :
		out = stdout.readlines()[0]
	return out


def _get_file(source, variables):
	try:
		ssh_client = _start_connection(source)
	except Exception as e:
		raise Exception("Couldn't connect to SSH host\n"+str(e))
	result = {}
	for var in source['variables']:
		try:
			result[var] = _get_variable_output(variables[var],ssh_client)
		except Exception as e:
			result[var] = e
	return result
		
		