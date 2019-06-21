#SSH module

import paramiko

def _get_value(var = []) :
	ssh_client=paramiko.SSHClient()
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	ssh_client.connect(hostname = var['input_method']['host_name'],username=var['input_method']['user_name'],password=var['input_method']['password'],key_filename = var['input_method']['key_filename'])

	stdin,stdout,stderr=ssh_client.exec_command(var["input_method"]['command'])

	if stderr.readlines() :
		ex = stderr.readlines()
		raise Exception(ex)
	else :
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
		
		