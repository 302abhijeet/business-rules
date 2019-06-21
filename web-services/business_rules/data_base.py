#Database module

import mysql.connector
def _get_value(var = []) :
	mydb = mysql.connector.connect(
			  host=var['input_method']['host_name'],
			  user=var['input_method']['user_name'],
			  passwd=var['input_method']['password'],
			  database=var['input_method']['data_base']
				)
	
	command = var['input_method']['command'].split("\n")
	mycursor = mydb.cursor()
	try:
		for com in command:
			mycursor.execute(com)
		result = mycursor.fetchall()
	except Exception as e:
		print(var['name'] + " Error in data_base commands:" + var['input_method']['command'])
		raise e

	if var['input_method']['start'] or var['input_method']['end'] :
		try:
			out = result[var["input_method"]['start']:var["input_method"]['end']]
		except Exception as e:
			print(var['name'] + " Error in SSH splitting of variable: ")
			raise e
	else :
		if len(result) == 1 :
			out = result[0]
			if len(out) == 1 :
				out = out[0]
		else :
			out = result

	return out