#configuration file for the API
import yaml

use_cases = { 
	#CPU_Performance begins
	'CPU_Performance' : {
	    'rule_list' : ['CPU_usage','memory','disk_space'],
		'rules' : [ ('CPU_usage','memory'),'disk_space']
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
 
	#case 2 begins
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
	
	# CPU_usage <= 50% and memory <=60% and disk_space < 70%
	'CPU_usage' : {
		"conditions" : { 			
			'name' : ["CPU_usage"],
			'operator': 'less_than',
			'value' : 50
		},
		"actions_true" : [ 
			{
				'name' : "CPU_true",
				'params' : None,
				'multi_thread' : True
			}
		],
		"actions_false": [
			{ 
				'name' : "CPU_false",
				'params' : None,
				'multi_thread' : True
			}
		],
		"actions" : ["CPU_true","CPU_false"],
		'multi_thread' : True,
		'variables' : ['CPU_usage']
	},

	# CPU_usage <= 50% and memory <=60% and disk_space < 70%
	'memory' : {
		"conditions" : { 			
			'name' : ["memory"],
			'operator': 'less_than',
			'value' : 60
		},
		"actions_true" : [ 
			{
				'name' : "memory_true",
				'params' : None,
				'multi_thread' : True
			}
		],
		"actions_false": [
			{ 
				'name' : "memory_false",
				'params' : None,
				'multi_thread' : True
			}
		],
		"actions" : ["memory_true","memory_false"],
		'multi_thread' : True,
		'variables' : ['free_mem','total_mem','memory']
	},

	# CPU_usage <= 50% and memory <=60% and disk_space < 70%
	'disk_space' : {
		"conditions" : { 			
			'name' : ["disk_space"],
			'operator': 'less_than',
			'value' : 70
		},
		"actions_true" : [ 
			{
				'name' : "disk_true",
			    'params' : None,
				'multi_thread' : True
			}
		],
		"actions_false": [
			{ 
				'name' : "disk_false",
			    'params' : None,
				'multi_thread' : True
			}
		],
		"actions" : ["disk_true","disk_false"],
		'multi_thread' : True,
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
			    'params' : None,
				'multi_thread' : True
			}
		],
		"actions_false": [
			{ 
				'name' : "condition_fail",
			    'params' : None,
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
			    'params' : None,
				'multi_thread' : True
			}
		],
		"actions_false": [ 
			{
				'name' : "condition_fail",
			    'params' : None,
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
			    'params' : None,
				'multi_thread' : True
			}
		],
		"actions_false": [
			{
				'name' : "condition_fail",
			    'params' : None,
				'multi_thread' : True
			}
		],
		"variables" : ['actual','expected',"correct"],
	    "actions" : ["condition_pass","condition_fail"],
		'multi_thread' : True
	}
}

variables = {
	'free_mem' : { #CPU numeric
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
	        "command" : "cat /proc/meminfo | grep MemAvailable",
	        'evaluation' : 'int',
	        'start' : ':',
	        'end' : 'kB',
       },
       'multi_thread' : False
	},

	'total_mem' : { #CPU numeric
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

	'memory' : { #CPU numeric
	    'name' : "memory",
		'field' : "numeric_rule_variable",
		'label' : 'None',
		'options' : 'None',
		'formulae' : 'self.product.memory = 100 * self.product.free_mem / self.product.total_mem',
		'input_method' : {
			'method' : 'derived'
       },
       'multi_thread' : False
	},

	'CPU_usage' : { #actual numeric
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

	'disk_space' : { #incorrect numeric
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
		'params' : None,
		'formulae' : "return {'msg' : 'All xpected access points are present'}",
	},
	"condition_fail" :{
	    'name' : 'condition_fail',
		'params' : None,
		'formulae' : "return {'msg' : 'NOT all expected access points are present'}",
	},
	"CPU_true" : { 
		'name' : 'CPU_true',
		'params' : None,
		'formulae' : "return {'msg' : 'CPU usage under threshold(50) : '+ str(self.product.CPU_usage)}",
	},
	"CPU_false" :{
	    'name' : 'CPU_false',
		'params' : None,
		'formulae' : "return {'msg' : 'CPU usage NOT under threshold(50): ' +  str(self.product.CPU_usage)}",
	},
	"memory_true" : { 
		'name' : 'memory_true',
		'params' : None,
		'formulae' : "return {'msg' : 'Memory usage under threshold(60) : '+ str(self.product.memory)}",
	},
	"memory_false" :{
	    'name' : 'memory_false',
		'params' : None,
		'formulae' : "return {'msg' : 'Memory usage NOT under threshold(60) : '+ str(self.product.memory)}",
	},
	"disk_true" : { 
		'name' : 'disk_true',
		'params' : None,
		'formulae' : "return {'msg' : 'disk usage under threshold(70) : '+  str(self.product.disk_space)}",
	},
	"disk_false" :{
	    'name' : 'disk_false',
		'params' : None,
		'formulae' : "return {'msg' : 'disk usage NOT under threshod(70) : '+ str(self.product.disk_space)}",
	}
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

