#configuration file for the API

use_cases = { 
			#case 1
            'case1' : {
              #for finding closest match
              'parameter1' : {'name1' : {'formulae' : '',
										  'percentage' : 20,
										  'match' : 0},
							   'name2' : {'formulae' : '',
							              'percentage' : 80,
							              'match' : 0}
							   ,
							   'percentage' : 20,
							   'match' : 0
							   },
		      'parameter2' : {'name3' : {'formulae' : '',
										  'percentage' : 20,
										  'match' : 0},
							   'name2' : {'formulae' : '',
							              'percentage' : 80,
							              'match' : 0}
							   ,
							   'percentage' : 80,
							   'match' : 0},
			   'match' : 0,

			   'rule_list' : ['rule1','rule2'],

			   'rules' : [{'all' : ['rule1','rule2'],
			              'then': ['rule3'],
			              'else': ['rule2']
			              },
			              {'any': {1 :['rule1','rule2','rule3'] },
			              'then': ['rule3','rule2'],
			              'else': None
			              } 
			            ]
				},
			 
			 #case 2 begins
			 'case2' : {
			  #closest match for case2
			   'parameter1' : {'name5' : {'formulae' : '',
										  'percentage' : 20,
										  'match' : 0},
							   'name6' : {'formulae' : '',
							              'percentage' : 80,
							              'match' : 0}
							   ,
							   'percentage' : 20,
							   'match' : 0
							   },
		      'parameter2' : {'name1' : {'formulae' : '',
										  'percentage' : 20,
										  'match' : 0},
							   'name2' : {'formulae' : '',
							              'percentage' : 80,
							              'match' : 0}
							   ,
							   'percentage' : 80,
							   'match' : 0},
			  'match' : 0,

			  'rule_list' : ['rule1','rule2'],

			  'rules' : [ ('rule1',['rule2','rule3'])]
				},
                
                #new case
				'case3' : {
			   'parameter1' : {'name5' : {'formulae' : '',
										  'percentage' : 20,
										  'match' : 0},
							   'name6' : {'formulae' : '',
							              'percentage' : 80,
							              'match' : 0}
							   ,
							   'percentage' : 20,
							   'match' : 0
							   },
		      'parameter2' : {'name1' : {'formulae' : '',
										  'percentage' : 20,
										  'match' : 0},
							   'name2' : {'formulae' : '',
							              'percentage' : 80,
							              'match' : 0}
							   ,
							   'percentage' : 80,
							   'match' : 0},
			  'match' : 0,

			  'rule_list' : ['rule1','rule2','rule3'],

			  'rules' : ['rule1','rule2','rule3']
				}
 }

rules = { 
		#(expected == actual and expected < 100) or actual > expected 
	    'rule1' : { "conditions" : {'any' : [ { 'all': [{'name' : ["actual","expected"],
											            'operator' : "equal_to",
										                'value' : None},
						                               {'name' : ["expected"],
						                                'operator': 'less_than',
					                                    'value' : 100}
						                                ]
						                       },
		   	                                  { 'name' : ['actual','expected'],
			                                    'operator' : "greater_than",
			                                    'value' : None }
						                   ]
				                    },
				    "actions_true" : [ { 'name' : "condition_pass",
				                       'params' : None}],
				    "actions_false": [ { 'name' : "condition_fail",
				                       'params' : None}],
				    "variables" : [
							#actual numeric
							{ 'name' : "actual",
							  'field' : "numeric_rule_variable",
							  'label' : 'None',
							  'options' : 'None',
							  'formulae' : 'self.product.actual',
							  'input_method' : {'method' : 'SSH',
							                    'host_name' : '10.137.89.13',
							                    'user_name' : 'ubuntu',
							                    'password' : 'rulesengine',
							                    'key_filename' : None,
							                    "command" : """cd abhijeet
							                                   cat actual.txt""",
							                    'evaluation' : 'int',
							                    'start' : None,
							                    'end' : None,
							                    }
							  },

							#expected numeric
							{ 'name' : "expected",
							  'field' : "numeric_rule_variable",
							  'label' : 'None',
							  'options' : 'None',
							  'formulae' : 'self.product.expected',
							  'input_method' : {'method' : 'SSH',
							                    'host_name' : '10.137.89.13',
							                    'user_name' : 'ubuntu',
							                    'password' : None,
							                    'key_filename' : 'C:\\Users\\axsingh\\Documents\\Rules-engine.pem',
							                    "command" : """cd abhijeet
							                                   cat expected.txt""",
							                    'evaluation' : 'int',
							                    'start' : None,
							                    'end' : None,
							                    }
							  }
							],
						"actions" : [
							{ 'name' : 'condition_pass',
							  'params' : None,
							  'formulae' : "print('All expected access points are present')"
							  },
							{ 'name' : 'condition_fail',
							  'params' : None,
							  'formulae' : "print('NOT all expected access points are present')"
							}
							]
				   },

		#(expected < actual and actual <  50)
		'rule2' :{ "conditions" : { 'all': [{'name' : ["actual","expected"],
				     			             'operator' : "greater_than",
							                 'value' : None},
						                    {'name' : ["actual"],
		   	                                 'operator': 'less_than',
				                             'value' : 50}
						                   ]
				                    },
				    "actions_true" : [ { 'name' : "condition_pass",
				                       'params' : None}],
				    "actions_false": [ { 'name' : "condition_fail",
				                       'params' : None}],
				    "variables" : [
							#actual numeric
							{ 'name' : "actual",
							  'field' : "numeric_rule_variable",
							  'label' : 'None',
							  'options' : 'None',
							  'formulae' : 'self.product.actual',
							  'input_method' : {'method' : 'API',
							                    'url' : 'https://ce979fb9-c240-4259-bf6a-6d9de424e291.mock.pstmn.io/get',
							                    'params' : {},
							                    "command" : 'response.json()["actual"]',
							                    'evaluation' : None,
							                    'start' : None,
							                    'end' : None
							                    }
							  },

							#expected numeric
							{ 'name' : "expected",
							  'field' : "numeric_rule_variable",
							  'label' : 'None',
							  'options' : 'None',
							  'formulae' : 'self.product.expected',
							  'input_method' : {'method' : 'API',
							                    'url' : 'https://ce979fb9-c240-4259-bf6a-6d9de424e291.mock.pstmn.io/get',
							                    'params' : {},
							                    "command" : 'response.json()["expected"]',
							                    'evaluation' : None,
							                    'start' : None,
							                    'end' : None
							                    }
							  }
							],
						"actions" : [
							{ 'name' : 'condition_pass',
							  'params' : None,
							  'formulae' : "print('All expected access points are present')"
							  },
							{ 'name' : 'condition_fail',
							  'params' : None,
							  'formulae' : "print('NOT all expected access points are present')"
							}
							]
				   },

	    #(expected = 70 or actual < 100)
		'rule3' :{ "conditions" : { 'any': [{'name' : ["expected"],
				     			             'operator' : "equal_to",
							                 'value' : 70},
						                    {'name' : ["actual"],
		   	                                 'operator': 'less_than',
				                             'value' : 100}
						                   ]
				                    },
				    "actions_true" : [ { 'name' : "condition_pass",
				                       'params' : None}],
				    "actions_false": [ { 'name' : "condition_fail",
				                       'params' : None}],
				    "variables" : [
							#actual numeric
							{ 'name' : "actual",
							  'field' : "numeric_rule_variable",
							  'label' : 'None',
							  'options' : 'None',
							  'formulae' : 'self.product.actual',
							  'input_method' : {'method' : 'API',
							                    'url' : 'https://ce979fb9-c240-4259-bf6a-6d9de424e291.mock.pstmn.io/get',
							                    'params' : {},
							                    "command" : 'response.json()["actual"]',
							                    'evaluation' : None,
							                    'start' : None,
							                    'end' : None
							                    }
							  },

							#expected numeric
							{ 'name' : "expected",
							  'field' : "numeric_rule_variable",
							  'label' : 'None',
							  'options' : 'None',
							  'formulae' : 'self.product.expected',
							  'input_method' : {'method' : 'data_base',
							                    'host_name' : '',
							                    'user_name' : '',
							                    'password' : '',
							                    'data_base' : '',
							                    "command" : '',
							                    'evaluation' : None,
							                    'start' : None,
							                    'end' : None,
							                    }
							  }
							],
						"actions" : [
							{ 'name' : 'condition_pass',
							  'params' : None,
							  'formulae' : "print('All expected access points are present')"
							  },
							{ 'name' : 'condition_fail',
							  'params' : None,
							  'formulae' : "print('NOT all expected access points are present')"
							}
							]
				   }
		}