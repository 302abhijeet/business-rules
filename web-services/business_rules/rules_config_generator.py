#configuration file for the API
from pymongo import MongoClient
from sshtunnel import SSHTunnelForwarder
from fields import *

use_cases = [ 
	#restraunt locator
	{
        'name' : 'restraunt',
		'rule_list' : ['distance_check','cost_check'],
		'rules' : ['distance_check','cost_check'],
		'stop_on_first_success' : False,
		'stop_on_first_failure' : True,
		"actions_true" : [
			{
				'name' : "condition_pass",
				'params' : {'name' : 'restraunt_case','msg' : 'Restraunt meets all requirements!'},
				'multi_thread' : True
			}
		],
		"actions_false" : [
			{
				'name' : "condition_fail",
				'params' : {'name' : 'restraunt_case','msg' : 'Restraunt does NOT meet all requirements!'},
				'multi_thread' : True
			}
		],
		'actions' : ['condition_pass','condition_fail']
	},

	#CPU_Performance
	{
        'name' : "CPU_Performance",
	    'rule_list' : ['CPU_usage','memory','disk_space'],
		'rules' : [ 'CPU_usage','memory','disk_space'],
		'stop_on_first_success' : False,
		'stop_on_first_failure' : False,
		"actions_true" : [
			{
				'name' : "condition_pass",
				'params' : {'name' : 'CPU_case','msg' : 'CPU meets all requirements!'},
				'multi_thread' : True
			}
		],
		"actions_false" : [
			{
				'name' : "condition_fail",
				'params' : {'name' : 'CPU_case','msg' : 'CPU does NOT meet all requirements!'},
				'multi_thread' : True
			}
		],
		'actions' : ['condition_pass','condition_fail']
	},

	#CPU conditional
	{
        'name' : "CPU_Conditional",
		'rule_list' : ['CPU_usage','memory','disk_space','rule1','rule2','rule3'],
		'rules' : [
			{
				'all' : ['CPU_usage','memory','disk_space'],
				'then' : None,
				'else' : ['rule2']
			},
			{
				'any' : {
					'2' :  ['CPU_usage','memory','disk_space']
				},
				'then' : ['rule3'],
				'else' : ['rule1']
			}
		],
		'stop_on_first_success' : False,
		'stop_on_first_failure' : False,
		"actions_true" : [
			{
				'name' : "condition_pass",
				'params' : {'name' : 'CPU_case','msg' : 'CPU meets all requirements!'},
				'multi_thread' : True
			}
		],
		"actions_false" : [
			{
				'name' : "condition_fail",
				'params' : {'name' : 'CPU_case','msg' : 'CPU does NOT meet all requirements!'},
				'multi_thread' : True
			}
		],
		'actions' : ['condition_pass','condition_fail']
	},

	#CPU asynchronous
	{
        'name' : "CPU_Asynchronous",
		'rule_list' : ['CPU_usage','memory','disk_space'],
		'rules' : [ ('CPU_usage',['memory','disk_space'])],
		'stop_on_first_success' : False,
		'stop_on_first_failure' : False,
		"actions_true" : [
			{
				'name' : "condition_pass",
				'params' : {'name' : 'CPU_case','msg' : 'CPU meets all requirements!'},
				'multi_thread' : True
			}
		],
		"actions_false" : [
			{
				'name' : "condition_fail",
				'params' : {'name' : 'CPU_case','msg' : 'CPU does NOT meet all requirements!'},
				'multi_thread' : True
			}
		],
		'actions' : ['condition_pass','condition_fail']
	},

	#case 1
	{
        'name' : "case1",
		'rule_list' : ['rule1','rule2','rule3'],
	    'rules' : [
		    {
			    'all' : ['rule1','rule2'],
	            'then': ['rule3'],
	            'else': ['rule2']
	        },
	        {
		        'any': {
			        '1' :['rule1','rule2','rule3'] 
			    },
	            'then': ['rule3','rule2'],
	            'else': None
	        } 
	    ],
		'stop_on_first_success' : False,
		'stop_on_first_failure' : False,
		"actions_true" : [
			{
				'name' : "condition_pass",
				'params' : {'name' : 'case1','msg' : 'Meets all requirements!'},
				'multi_thread' : True
			}
		],
		"actions_false" : [
			{
				'name' : "condition_fail",
				'params' : {'name' : 'case1','msg' : 'Does NOT meet all requirements!'},
				'multi_thread' : True
			}
		],
		'actions' : ['condition_pass','condition_fail']
	},
 
	#case 2 
	{
        'name' : "case2",
	    'rule_list' : ['rule1','rule2','rule3'],
		'rules' : [ ('rule1',['rule2','rule3'])],
		'stop_on_first_success' : False,
		'stop_on_first_failure' : False,
		"actions_true" : [
			{
				'name' : "condition_pass",
				'params' : {'name' : 'case2','msg' : 'Meets all requirements!'},
				'multi_thread' : True
			}
		],
		"actions_false" : [
			{
				'name' : "condition_fail",
				'params' : {'name' : 'case2','msg' : 'Does NOT meet all requirements!'},
				'multi_thread' : True
			}
		],
		'actions' : ['condition_pass','condition_fail']
	},
    
    #new case
	{
        'name' : "case3",
		'rule_list' : ['rule1','rule2','rule3'],
		'rules' : ['rule1','rule2','rule3'],
		'stop_on_first_success' : False,
		'stop_on_first_failure' : False,
		"actions_true" : [
			{
				'name' : "condition_pass",
				'params' : {'name' : 'case3','msg' : 'Meets all requirements!'},
				'multi_thread' : True
			}
		],
		"actions_false" : [
			{
				'name' : "condition_fail",
				'params' : {'name' : 'case3','msg' : 'Does NOT meet all requirements!'},
				'multi_thread' : True
			}
		],
		'actions' : ['condition_pass','condition_fail']
	}
]
rules = [
	# distance < dist_limit
	{
        'name' : "distance_check",
		"conditions" : {
			'name' : ["distance","dist_limit"],
			'operator' : 'less_than',
			'value' : None
		},
		"actions_true" : [ 
			{
				'name' : "Threshold_true",
				'params' : {'name' : 'distance_check','threshold': 'self.product.dist_limit','var':'distance'},
				'multi_thread' : True
			}
		],
		"actions_false": [
			{ 
				'name' : "Threshold_false",
				'params' : {'name' : 'distance_check','threshold': 'self.product.dist_limit','var':'distance'},
				'multi_thread' : True
			}
		],
		'actions' : ['Threshold_true','Threshold_false'],
		'variables' : ['distance','dist_limit'],
		'multi_thread' : True
	},
	
	# cost < cost_limit
	{
        'name' : "cost_check",
		"conditions" : {
			'name' : ["cost","cost_limit"],
			'operator' : 'less_than',
			'value' : None
		},
		"actions_true" : [ 
			{
				'name' : "Threshold_true",
				'params' : {'name' : 'cost_check','threshold': 'self.product.cost_limit','var':'cost'},
				'multi_thread' : True
			}
		],
		"actions_false": [
			{ 
				'name' : "Threshold_false",
				'params' : {'name' : 'cost_check','threshold': 'self.product.cost_limit','var':'cost'},
				'multi_thread' : True
			}
		],
		'actions' : ['Threshold_true','Threshold_false'],
		'variables' : ['cost','cost_limit'],
		'multi_thread' : True
	},
	
    # CPU_usage <= 50% 
	{
        'name' : "CPU_usage",
		"conditions" : { 			
			'name' : ["CPU_usage"],
			'operator': 'less_than',
			'value' : 50
		},
		"actions_true" : [ 
			{
				'name' : "Threshold_true",
				'params' : {'name' : 'CPU Usage','threshold': '50','var':'CPU_usage'},
				'multi_thread' : True
			}
		],
		"actions_false": [
			{ 
				'name' : "Threshold_false",
				'params' : {'name' : 'CPU Usage','threshold': '50','var':'CPU_usage'},
				'multi_thread' : True
			}
		],
		"actions" : ["Threshold_true","Threshold_false"],
		'multi_thread' : True,
		'variables' : ['CPU_usage']
	},

	# memory <=60%
	{
        'name' : "memory",
		"conditions" : { 			
			'name' : ["memory"],
			'operator': 'less_than',
			'value' : 60
		},
		"actions_true" : [ 
			{
				'name' : "Threshold_true",
				'params' : {'name' : 'memory usage','threshold': '60','var':'memory'},
				'multi_thread' : True
			}
		],
		"actions_false": [
			{ 
				'name' : "Threshold_false",
				'params' : {'name' : 'memory usage','threshold': '60','var':'memory'},
				'multi_thread' : True
			}
		],
		"actions" : ["Threshold_true","Threshold_false"],
		'multi_thread' : True,
		'variables' : ['free_mem','total_mem','memory']
	},

	# disk_space < 70%
	{
        'name' : "disk_space",
		"conditions" : { 			
			'name' : ["disk_space"],
			'operator': 'less_than',
			'value' : 70
		},
		"actions_true" : [ 
			{
				'name' : "Threshold_true",
				'params' : {'name' : 'Disk Usage','threshold': '70','var':'disk_space'},
				'multi_thread' : True
			}
		],
		"actions_false": [
			{ 
				'name' : "Threshold_false",
				'params' : {'name' : 'Disk Usage','threshold': '70','var':'disk_space'},
				'multi_thread' : True
			}
		],
		"actions" : ["Threshold_true","Threshold_false"],
		'multi_thread' : False,
		'variables' : ['disk_space']
	},

	#(expected == actual and expected < 100) or actual > expected or correct < 10
    { 
        'name' : "rule1",
	    "conditions" : {
		    'any' : [ 
			    { 
				    'all': [ 
					    {
						    'name' : ["actual","expected"],
							'operator' : "equal_to",
							'value' : None
						},
						{
							'name' : ["expected"],
						    'operator': 'less_than',
					        'value' : 100
					    }
                    ]
				},
	   	        { 
		   	        'name' : ['actual','expected'],
		            'operator' : "greater_than",
		            'value' : None 
		        },
		        {
					'name' : ["correct"],
	   	            'operator': 'less_than',
			        'value' : 10
			    }
			]
		},
		"actions_true" : [ 
			{
				'name' : "condition_pass",
			    'params' : {'name' : "Rule1"},
				'multi_thread' : True
			}
		],
		"actions_false": [
			{ 
				'name' : "condition_fail",
			    'params' : {'name' : "Rule1"},
				'multi_thread' : True
			}
		],
		"variables" : ['actual','expected',"correct"],
		"actions" : ["condition_pass","condition_fail"],
		'multi_thread' : True		
     	},

	#(expected < actual and actual <  50 and correct < 10) or incorrect = 23
	{ 
        'name' : "rule2",
		"conditions" : { 
			'any' : [
				{
					'all': [
						{
							'name' : ["actual","expected"],
							'operator' : "greater_than",
							'value' : None
						},
						{
							'name' : ["actual"],
							'operator': 'less_than',
							'value' : 50
						},
						{
							'name' : ["correct"],
							'operator': 'less_than',
							'value' : 10
						}
					]
				},
				{
					'name' : ["incorrect"],
					'operator' : "equal_to",
					'value' : 23
				}
			]
		},
		"actions_true" : [ 
			{
				'name' : "condition_pass",
			    'params' : {'name' : "Rule2"},
				'multi_thread' : True
			}
		],
		"actions_false": [ 
			{
				'name' : "condition_fail",
			    'params' : {'name' : "Rule2"},
				'multi_thread' : True
			}
		],
		"variables" : ['actual','expected',"correct","incorrect"],
		"actions" : ["condition_pass","condition_fail"],
		'multi_thread' : True
	},

    #(expected = 70 or actual < 100 or correct < 10)
	{ 
        'name' : "rule3",
		"conditions" : { 
			'any': [
				{
					'name' : ["expected"],
			     	'operator' : "equal_to",
					'value' : 70
				},
				{
					'name' : ["actual"],
	   	            'operator': 'less_than',
			        'value' : 100
			    },
			    {
					'name' : ["correct"],
	   	            'operator': 'less_than',
			        'value' : 10
			    }
			]
		},
		"actions_true" : [ 
			{
				'name' : "condition_pass",
			    'params' : {'name' : "Rule3"},
				'multi_thread' : True
			}
		],
		"actions_false": [
			{
				'name' : "condition_fail",
			    'params' : {'name' : "Rule3"},
				'multi_thread' : True
			}
		],
		"variables" : ['actual','expected',"correct"],
	    "actions" : ["condition_pass","condition_fail"],
		'multi_thread' : True
	}
]

variables = [
	{
		'name' : "distance",
		'field' : "numeric_rule_variable",
		'label' : 'None',
		'options' : 'None',
		'formulae' : 'self.product.distance',
		'input_method' : {
			"DataSource" : "API_mapQuest",
            "command" : 'response.json()["distance"][1]',
            'evaluation' : 'int',
            'start' : None,
	        'end' : None
       },
       'multi_thread' : True
	},

	{
		'name' : "dist_limit",
		'field' : "numeric_rule_variable",
		'label' : 'None',
		'options' : 'None',
		'formulae' : 'self.product.dist_limit',
		'input_method' : {
			"DataSource" : "API_getPostman",
            "command" : 'response.json()["actual"]',
            'evaluation' : 'int',
            'start' : None,
	        'end' : None
       },
       'multi_thread' : True
	},

	{
		'name' : "cost",
		'field' : "numeric_rule_variable",
		'label' : 'None',
		'options' : 'None',
		'formulae' : 'self.product.cost',
		'input_method' : {
			"DataSource" : "API_mapQuest",
            "command" : 'response.json()["time"][1]',
            'evaluation' : 'int',
            'start' : None,
	        'end' : None
       },
       'multi_thread' : True
	},

	{
		'name' : "cost_limit",
		'field' : "numeric_rule_variable",
		'label' : 'None',
		'options' : 'None',
		'formulae' : 'self.product.cost_limit',
		'input_method' : {
			"DataSource" : "API_getPostman",
            "command" : 'response.json()["actual"]',
            'evaluation' : 'int',
            'start' : None,
	        'end' : None
       },
       'multi_thread' : True
	},

	{ #numeric
	    'name' : "free_mem",
		'field' : "numeric_rule_variable",
		'label' : 'None',
		'options' : 'None',
		'formulae' : 'self.product.free_mem',
		'input_method' : {
			"DataSource" : "SSH_awsIntern",
	        "command" : "cat /proc/meminfo | grep MemFree",
	        'evaluation' : 'int',
	        'start' : ':',
	        'end' : 'kB',
       },
       'multi_thread' : False
	},

	{ #numeric
	    'name' : "total_mem",
		'field' : "numeric_rule_variable",
		'label' : 'None',
		'options' : 'None',
		'formulae' : 'self.product.total_mem',
		'input_method' : {
			"DataSource" : "SSH_awsIntern",
	        "command" : "cat /proc/meminfo | grep MemTotal",
	        'evaluation' : 'int',
	        'start' : ':',
	        'end' : 'kB',
       },
       'multi_thread' : False
	},

	{ #numeric
	    'name' : "memory",
		'field' : "numeric_rule_variable",
		'label' : 'None',
		'options' : 'None',
		'formulae' : 'self.product.memory = 100 - 100 * self.product.free_mem / self.product.total_mem',
		'input_method' : {
			'method' : 'derived',
            'variables' : ['free_mem','total_mem']
        },
        'multi_thread' : False
	},

	{ #numeric
	    'name' : "CPU_usage",
		'field' : "numeric_rule_variable",
		'label' : 'None',
		'options' : 'None',
		'formulae' : 'self.product.CPU_usage',
		'input_method' : {
			"DataSource" : "API_getPostman",
            "command" : 'response.json()["actual"]',
            'evaluation' : 'int',
            'start' : None,
	        'end' : None
       },
       'multi_thread' : True
	},

	{ #numeric
	    'name' : "disk_space",
		'field' : "numeric_rule_variable",
		'label' : 'None',
		'options' : 'None',
		'formulae' : 'self.product.disk_space',
		'input_method' : {
			"DataSource" : "API_postPostman",
            "command" : 'response.json()["incorrect"]',
            'evaluation' : 'int',
            'start' : None,
	        'end' : None
       },
       'multi_thread' : True
	},

	{ #actual numeric
	    'name' : "actual",
		'field' : "numeric_rule_variable",
		'label' : 'None',
		'options' : 'None',
		'formulae' : 'self.product.actual',
		'input_method' : {
			"DataSource" : "API_getPostman",
            "command" : 'response.json()["actual"]',
            'evaluation' : 'int',
            'start' : None,
	        'end' : None
       },
       'multi_thread' : True
	},

	{ #incorrect numeric
	    'name' : "incorrect",
		'field' : "numeric_rule_variable",
		'label' : 'None',
		'options' : 'None',
		'formulae' : 'self.product.incorrect',
		'input_method' : {
			"DataSource" : "API_postPostman",
            "command" : 'response.json()["incorrect"]',
            'evaluation' : 'int',
            'start' : None,
	        'end' : None
       },
       'multi_thread' : True
	},

	{ #expected numeric
		'name' : "expected",
	    'field' : "numeric_rule_variable",
	    'label' : 'None',
	    'options' : 'None',
	    'formulae' : 'self.product.expected',
	    'input_method' : {
			"DataSource" : "SSH_awsIntern",
	        "command" : """cd abhijeet\ncat expected.txt""",
	        'evaluation' : 'int',
	        'start' : None,
	        'end' : None,
	    },
	    'multi_thread' : True
	},

	{#correct numeric
		 'name' : "correct",
		 'field' : "numeric_rule_variable",
		 'label' : 'None',
		 'options' : 'None',
		 'formulae' : 'self.product.correct',
		 'input_method' : {
			"DataSource" : "database_sqlRuleEngine",
		    "command" : 'select correct from rule where correct order by correct limit 1',
		    'evaluation' : 'int',
		    'start' : None,
		    'end' : None,
	     },
	     'multi_thread' : True
 	}
]

actions = [
	{ 
		'name' : 'condition_pass',
		'params' : {'name' : FIELD_TEXT, 'msg' : FIELD_TEXT},
		'formulae' : "return {name : 'All conditions were met succesfully!', 'msg' : msg}",
	},
	{
	    'name' : 'condition_fail',
		'params' : {'name' : FIELD_TEXT, 'msg' : FIELD_TEXT},
		'formulae' : "return {name : 'NOT all conditions were met!', 'msg' : msg}",
	},
	{ 
		'name' : 'Threshold_true',
		'params' : {'name' : FIELD_TEXT,"threshold" : FIELD_TEXT,'var': FIELD_TEXT},
		'formulae' : "l=locals()\n\texec('var,t = self.product.' + var+','+threshold,globals(),l)\n\tt,var=l['t'],l['var']\n\treturn {name : name + ' under threshold(' + str(t) +') : '+ str(var)}",
	},
	{
	    'name' : 'Threshold_false',
		'params' :{'name' : FIELD_TEXT,"threshold" : FIELD_TEXT,'var': FIELD_TEXT},
		'formulae' : "l=locals()\n\texec('var,threshold = self.product.' + var+','+threshold,globals(),l)\n\tthreshold,var =l['threshold'],l['var']\n\treturn {name : name + ' NOT under threshold(' + str(threshold) +'): ' +  str(var)}",
	},
]

DataSource = [
	{
        'name' : "SSH_awsIntern",
		'method' : 'SSH',
		'host_name' : '10.137.89.13',
		'user_name' : 'ubuntu',
		'password' : None,
		'key_filename' : 'C:\\Users\\axsingh\\Documents\\Rules-engine.pem',
		'variables' : [],
		'multi_thread' : True
	},
	{
        'name' : "API_getPostman",
		'method' : 'API',
		'request' : 'get',
		'url' : 'https://548a3990-a83e-4862-a950-cc252c905ce2.mock.pstmn.io/get',
		'params' : {},
		'variables' : [],
		'multi_thread' : True
	},
	{
        'name' : "API_postPostman",
		'method' : 'API',
		'request' : 'post',
		'url' : 'https://75c9507b-8f2e-4211-a518-2c2ab988c27d.mock.pstmn.io/post',
		'params' : {},
		'data' : { "method" : "POST", "value" : 13},
		'variables' : [],
		'multi_thread' : True
	},
	{
        'name' : "API_mapQuest",
		'method' : 'API',
		'request' : 'post',
		'url' : 'http://www.mapquestapi.com/directions/v2/routematrix?key=1XpKHYmtfjhVKQhYAfpTfbjP8pz0d7Q4',
		'params' : {},
		'data' : {"locations": ["Denver, CO","Westminster, CO"]},
		'variables' : [],
		'multi_thread' : True
	},
	{
        'name' : "database_sqlRuleEngine",
		'method' : 'data_base',
		'host_name' : 'localhost',
		'user_name' : 'root',
		'password' : 'Perfacio1',
		'data_base' : 'rules_engine',
		'variables' : [],
		'multi_thread' : True
	}
]

# define ssh tunnel
server = SSHTunnelForwarder(
    "10.137.89.13",
    ssh_username="ubuntu",
    ssh_password="rules_engine",
    remote_bind_address=('127.0.0.1', 27017)
)

# start ssh tunnel
server.start()

myclient = MongoClient('127.0.0.1', server.local_bind_port)
myclient.drop_database("rules_engine")
mydb = myclient["rules_engine"]
mydb["use_cases"].insert_many(use_cases)
mydb["rules"].insert_many(rules)
mydb["variables"].insert_many(variables)
mydb["actions"].insert_many(actions)
mydb["DataSource"].insert_many(DataSource)

# close ssh tunnel
server._server_list[0].block_on_close = False
server.stop()


"""
#can be added for parameter matching
use_cases_match = { 
	#case 1
	'case1' : {
		#for finding closest match
		'parameter1' : {
		    'name1' : {
			    'formulae' : '',
				'percentage' : 20,
				'match' : 0
			},
			'name2' : {
				'formulae' : '',
				'percentage' : 80,
				'match' : 0
			},
			'percentage' : 20,
			'match' : 0
		},
	    'parameter2' : {
		    'name3' : {
			    'formulae' : '',
				'percentage' : 20,
				'match' : 0
			},
			'name2' : {
				'formulae' : '',
				'percentage' : 80,
				'match' : 0
			},
			'percentage' : 80,
			'match' : 0
		},
	    'match' : 0,
		'rule_list' : ['rule1','rule2','rule3'],
	    'rules' : ['rule1','rule2','rule3']
	},
}
"""

