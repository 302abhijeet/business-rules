#configuration file for the API
import yaml

use_cases = { 
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
			    'params' : None
			}
		],
		"actions_false": [
			{ 
				'name' : "condition_fail",
			    'params' : None
			}
		],
		"variables" : ['actual','expected',"correct"],
		"actions" : ["condition_pass","condition_fail"]
     	},

	#(expected < actual and actual <  50 and correct < 10)
	'rule2' :{ 
		"conditions" : { 
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
		"actions_true" : [ 
			{
				'name' : "condition_pass",
			    'params' : None
			}
		],
		"actions_false": [ 
			{
				'name' : "condition_fail",
			    'params' : None
			}
		],
		"variables" : ['actual','expected',"correct"],
		"actions" : ["condition_pass","condition_fail"]
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
			    'params' : None
			}
		],
		"actions_false": [
			{
				'name' : "condition_fail",
			    'params' : None
			}
		],
		"variables" : ['actual','expected',"correct"],
	    "actions" : ["condition_pass","condition_fail"]
	}
}

variables = {
	'actual' : { #actual numeric
	    'name' : "actual",
		'field' : "numeric_rule_variable",
		'label' : 'None',
		'options' : 'None',
		'formulae' : 'self.product.actual',
		'input_method' : {
			'method' : 'API',
            'url' : 'https://ce979fb9-c240-4259-bf6a-6d9de424e291.mock.pstmn.io/get',
            'params' : {},
            "command" : 'response.json()["actual"]',
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
		'formulae' : "print('All expected access points are present')",
		'multi_thread' : True
	},
	"condition_fail" :{
	    'name' : 'condition_fail',
		'params' : None,
		'formulae' : "print('NOT all expected access points are present')",
		'multi_thread' : True
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

