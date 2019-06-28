#Database module

import mysql.connector
def _start_connection(source):
	try:
		mydb = mysql.connector.connect(
			host=source['host_name'],
			user=source['user_name'],
			passwd=source['password'],
			database=source['data_base']
				)
		return mydb
	except Exception as e:
		raise Exception("Couldn't connect to database host\n"+str(e))

def _get_variable_output(var,mydb):
	command = var['input_method']['command'].split("\n")
	mycursor = mydb.cursor()
	try:
		for com in command:
			mycursor.execute(com)
		result = mycursor.fetchall()
	except Exception as e:
		raise Exception(var['name'] + " Error in data_base commands:" + var['input_method']['command']+"\n"+str(e))

	if var['input_method']['start'] or var['input_method']['end'] :
		try:
			out = result[var["input_method"]['start']:var["input_method"]['end']]
		except Exception as e:
			raise Exception("Error in SSH splitting of variable: "+var['name']+"\n"+str(e))
	else :
		if len(result) == 1 :
			out = result[0]
			if len(out) == 1 :
				out = out[0]
		else :
			out = result
	return out

def _get_file(source,variables):
	mydb = _start_connection(source)
	result = {}
	for var in source['variables']:
		try: 
			result[var] = _get_variable_output(variables[var],mydb)
		except Exception as e:
			result[var] = e
	return result