#configuration file for the API
import yaml
from fields import *

use_cases = { 
	#CPU_Performance
	'CPU_Performance' : {
	    'rule_list' : ['CPU_usage','memory','disk_space'],
		'rules' : [ 'CPU_usage','memory','disk_space']
	},

	#CPU conditional
	'CPU_Conditional' : {
		'rule_list' : ['CPU_usage','memory','disk_space','rule1','rule2','rule3'],
		'rules' : [
			{
				'all' : ['CPU_usage','memory','disk_space'],
				'then' : None,
				'else' : ['rule2']
			},
			{
				'any' : {
					2 :  ['CPU_usage','memory','disk_space']
				},
				'then' : ['rule3'],
				'else' : ['rule1']
			}
		]
	},

	#CPU asynchronous
	'CPU_Asynchronous' : {
		'rule_list' : ['CPU_usage','memory','disk_space'],
		'rules' : [ ('CPU_usage',['memory','disk_space'])]
	},

	#case 1
	'case1' : {
		'rule_list' : ['rule1','rule2','rule3'],
	    'rules' : [
		    {
			    'all' : ['rule1','rule2'],
	            'then': ['rule3'],
	            'else': ['rule2']
	        },
	        {
		        'any': {
			        1 :['rule1','rule2','rule3'] 
			    },
	            'then': ['rule3','rule2'],
	            'else': None
	        } 
	    ]
	},
 
	#case 2 
	'case2' : {
	    'rule_list' : ['rule1','rule2','rule3'],
		'rules' : [ ('rule1',['rule2','rule3'])]
	},
    
    #new case
	'case3' : {
		'rule_list' : ['rule1','rule2','rule3'],
		'rules' : ['rule1','rule2','rule3']
	}
}

rules = { 
	
	# CPU_usage <= 50% 
	'CPU_usage' : {
		"conditions" : { 			
			'name' : ["CPU_usage"],
			'operator': 'less_than',
			'value' : 50
		},
		"actions_true" : [ 
			{
				'name' : "CPU_true",
				'params' : {'name' : 'CPU Usage','threshold': 50,'var':'CPU_usage'},
				'multi_thread' : True
			}
		],
		"actions_false": [
			{ 
				'name' : "CPU_false",
				'params' : {'name' : 'CPU Usage','threshold': 50,'var':'CPU_usage'},
				'multi_thread' : True
			}
		],
		"actions" : ["CPU_true","CPU_false"],
		'multi_thread' : True,
		'variables' : ['CPU_usage']
	},

	# memory <=60%
	'memory' : {
		"conditions" : { 			
			'name' : ["memory"],
			'operator': 'less_than',
			'value' : 60
		},
		"actions_true" : [ 
			{
				'name' : "CPU_true",
				'params' : {'name' : 'memory usage','threshold': 60,'var':'memory'},
				'multi_thread' : True
			}
		],
		"actions_false": [
			{ 
				'name' : "CPU_false",
				'params' : {'name' : 'memory usage','threshold': 60,'var':'memory'},
				'multi_thread' : True
			}
		],
		"actions" : ["CPU_true","CPU_false"],
		'multi_thread' : True,
		'variables' : ['free_mem','total_mem','memory']
	},

	# disk_space < 70%
	'disk_space' : {
		"conditions" : { 			
			'name' : ["disk_space"],
			'operator': 'less_than',
			'value' : 70
		},
		"actions_true" : [ 
			{
				'name' : "CPU_true",
				'params' : {'name' : 'Disk Usage','threshold': 70,'var':'disk_space'},
				'multi_thread' : True
			}
		],
		"actions_false": [
			{ 
				'name' : "CPU_false",
				'params' : {'name' : 'Disk Usage','threshold': 70,'var':'disk_space'},
				'multi_thread' : True
			}
		],
		"actions" : ["CPU_true","CPU_false"],
		'multi_thread' : False,
		'variables' : ['disk_space']
	},

	#(expected == actual and expected < 100) or actual > expected or correct < 10
    'rule1' : { 
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
	'rule2' :{ 
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
	'rule3' :{ 
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
}

variables = {
	'free_mem' : { #numeric
	    'name' : "free_mem",
		'field' : "numeric_rule_variable",
		'label' : 'None',
		'options' : 'None',
		'formulae' : 'self.product.free_mem',
		'input_method' : {
			'method' : 'SSH',
	        'host_name' : '10.137.89.13',
	        'user_name' : 'ubuntu',
	        'password' : None,
	        'key_filename' : 'C:\\Users\\axsingh\\Documents\\Rules-engine.pem',
	        "command" : "cat /proc/meminfo | grep MemFree",
	        'evaluation' : 'int',
	        'start' : ':',
	        'end' : 'kB',
       },
       'multi_thread' : False
	},

	'total_mem' : { #numeric
	    'name' : "total_mem",
		'field' : "numeric_rule_variable",
		'label' : 'None',
		'options' : 'None',
		'formulae' : 'self.product.total_mem',
		'input_method' : {
			'method' : 'SSH',
	        'host_name' : '10.137.89.13',
	        'user_name' : 'ubuntu',
	        'password' : None,
	        'key_filename' : 'C:\\Users\\axsingh\\Documents\\Rules-engine.pem',
	        "command" : "cat /proc/meminfo | grep MemTotal",
	        'evaluation' : 'int',
	        'start' : ':',
	        'end' : 'kB',
       },
       'multi_thread' : False
	},

	'memory' : { #numeric
	    'name' : "memory",
		'field' : "numeric_rule_variable",
		'label' : 'None',
		'options' : 'None',
		'formulae' : 'self.product.memory = 100 - 100 * self.product.free_mem / self.product.total_mem',
		'input_method' : {
			'method' : 'derived'
       },
       'multi_thread' : False
	},

	'CPU_usage' : { #numeric
	    'name' : "CPU_usage",
		'field' : "numeric_rule_variable",
		'label' : 'None',
		'options' : 'None',
		'formulae' : 'self.product.CPU_usage',
		'input_method' : {
			'method' : 'API',
			'request' : 'get',
            'url' : 'https://ce979fb9-c240-4259-bf6a-6d9de424e291.mock.pstmn.io/get',
            'params' : {},
            "command" : 'response.json()["actual"]',
            'evaluation' : 'int',
            'start' : None,
	        'end' : None
       },
       'multi_thread' : True
	},

	'disk_space' : { #numeric
	    'name' : "disk_space",
		'field' : "numeric_rule_variable",
		'label' : 'None',
		'options' : 'None',
		'formulae' : 'self.product.disk_space',
		'input_method' : {
			'method' : 'API',
			'request' : 'post',
            'url' : 'https://50e3b433-59fc-4582-80f2-3d006f1ab57d.mock.pstmn.io/post',
            'params' : {},
			'data' : { "method" : "POST", "value" : 13},
            "command" : 'response.json()["incorrect"]',
            'evaluation' : 'int',
            'start' : None,
	        'end' : None
       },
       'multi_thread' : True
	},

	'actual' : { #actual numeric
	    'name' : "actual",
		'field' : "numeric_rule_variable",
		'label' : 'None',
		'options' : 'None',
		'formulae' : 'self.product.actual',
		'input_method' : {
			'method' : 'API',
			'request' : 'get',
            'url' : 'https://ce979fb9-c240-4259-bf6a-6d9de424e291.mock.pstmn.io/get',
            'params' : {},
            "command" : 'response.json()["actual"]',
            'evaluation' : 'int',
            'start' : None,
	        'end' : None
       },
       'multi_thread' : True
	},

	'incorrect' : { #incorrect numeric
	    'name' : "incorrect",
		'field' : "numeric_rule_variable",
		'label' : 'None',
		'options' : 'None',
		'formulae' : 'self.product.incorrect',
		'input_method' : {
			'method' : 'API',
			'request' : 'post',
            'url' : 'https://50e3b433-59fc-4582-80f2-3d006f1ab57d.mock.pstmn.io/post',
            'params' : {},
			'data' : { "method" : "POST", "value" : 13},
            "command" : 'response.json()["incorrect"]',
            'evaluation' : 'int',
            'start' : None,
	        'end' : None
       },
       'multi_thread' : True
	},

	'expected' : { #expected numeric
		'name' : "expected",
	    'field' : "numeric_rule_variable",
	    'label' : 'None',
	    'options' : 'None',
	    'formulae' : 'self.product.expected',
	    'input_method' : {
		    'method' : 'SSH',
	        'host_name' : '10.137.89.13',
	        'user_name' : 'ubuntu',
	        'password' : None,
	        'key_filename' : 'C:\\Users\\axsingh\\Documents\\Rules-engine.pem',
	        "command" : """cd abhijeet\ncat expected.txt""",
	        'evaluation' : 'int',
	        'start' : None,
	        'end' : None,
	    },
	    'multi_thread' : True
	},

	'correct' : {#correct numeric
		 'name' : "correct",
		 'field' : "numeric_rule_variable",
		 'label' : 'None',
		 'options' : 'None',
		 'formulae' : 'self.product.correct',
		 'input_method' : {
			'method' : 'data_base',
		    'host_name' : 'localhost',
		    'user_name' : 'root',
		    'password' : 'Perfacio1',
		    'data_base' : 'rules_engine',
		    "command" : 'select correct from rule where correct order by correct limit 1',
		    'evaluation' : 'int',
		    'start' : None,
		    'end' : None,
	     },
	     'multi_thread' : True
 	}
}

actions = {
	"condition_pass" : { 
		'name' : 'condition_pass',
		'params' : {'name' : FIELD_TEXT},
		'formulae' : "return {name : 'All xpected access points are present'}",
	},
	"condition_fail" :{
	    'name' : 'condition_fail',
		'params' : {'name' : FIELD_TEXT},
		'formulae' : "return {name : 'NOT all expected access points are present'}",
	},
	"CPU_true" : { 
		'name' : 'CPU_true',
		'params' : {'name' : FIELD_TEXT,"threshold" : FIELD_NUMERIC,'var': FIELD_TEXT},
		'formulae' : "l=locals()\n\texec('var = self.product.' + var,globals(),l)\n\tvar = l['var']\n\treturn {name : name + ' under threshold(' + str(threshold) +') : '+ str(var)}",
	},
	"CPU_false" :{
	    'name' : 'CPU_false',
		'params' :{'name' : FIELD_TEXT,"threshold" : FIELD_NUMERIC,'var': FIELD_TEXT},
		'formulae' : "l=locals()\n\texec('var = self.product.' + var,globals(),l)\n\tvar = l['var']\n\treturn {name : name + ' NOT under threshold(' + str(threshold) +'): ' +  str(var)}",
	},

}


with open("./configuration_files/use_cases.yml", 'w') as f:
    yaml.dump(use_cases, f)
with open("./configuration_files/rules.yml", 'w') as f:
    yaml.dump(rules, f)
with open("./configuration_files/variables.yml", 'w') as f:
    yaml.dump(variables, f)
with open("./configuration_files/actions.yml", 'w') as f:
    yaml.dump(actions, f)


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

