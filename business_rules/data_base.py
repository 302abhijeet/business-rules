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
	for com in command:
	    mycursor.execute(com)
	result = mycursor.fetchall()

	if  var["input_method"]['evaluation'] and type(result) is not type(var["input_method"]['evaluation']) :
		raise Exception("evaluation criteria not met")
	else :
		if not  start or not end :
			out = result[var["input_method"]['start']:var["input_method"]['end']]
		else :
			out = result

		return out