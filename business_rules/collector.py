#collector for collecting and populating the data
class Collector:
	def create(self, variables) :
		for var in variables :
			
			if var['input_method']['method'] == 'SSH' :
				import paramiko
				ssh_client=paramiko.SSHClient()
				ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
				ssh_client.connect(hostname = var['input_method']['host_name'],username=var['input_method']['user_name'],password=var['input_method']['password'])

				stdin,stdout,stderr=ssh_client.exec_command(var["input_method"]['command'])
				
				if stderr.readlines() :
					ex = stderr.readlines()
					raise Exception(ex)
				elif  var["input_method"]['evaluation'] and type(stdout.readlines()) is not type(var["input_method"]['evaluation']) :
					raise Exception("evaluation criteria not met")
				else :
					if not  start or not end :
						out = stdout.readlines()[var["input_method"]['start']:var["input_method"]['end']]
					else :
						out = stdout.readlines()
					
					exec("self." + var['name'] + " = " + 'out')


			elif var['input_method']['method'] == "data_base" :
				import mysql.connector
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

					exec("self." + var['name'] + " = " + 'out')


			elif var['input_method']['method'] == "API":
				import requests
				response = requests.get(var['input_method']['url'], params = var['input_method']['params'])
				exec(var['input_method']['command'])
                

				#have to make changes here
				if  var["input_method"]['evaluation'] and type(response) is not type(var["input_method"]['evaluation']) :
					raise Exception("evaluation criteria not met")
				else :
					if not  start or not end :
						out = response[var["input_method"]['start']:var["input_method"]['end']]
					else :
						out = response

				exec("self." + var['name'] + " = " + 'out')
			

			elif var['input_method']['method'] == "data_bus":
				pass
			else :
				raise Exception(var['input_method']['method'] + " Not found")
				exit()

		return self