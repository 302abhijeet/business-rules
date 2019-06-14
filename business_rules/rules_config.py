#file for configuring the rules
import json

#export use cases

use_cases = [ 
            { 'name' : 'case1',
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
			   'rules' : [
							#(expected == actual and expected < 100) or actual > expected 
							{ "conditions" : {'any' : [ { 'all': [{'name' : ["actual","expected"],
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
							}
							],
				'variables' : [
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
                'actions' : [
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
			 
			  {'name' : 'case2',
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
			  'rules' : [
						#(expected == actual and expected < 100) or actual > expected 
						{ "conditions" : {'any' : [ { 'all': [{'name' : ["actual","expected"],
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
						}
						],
				'variables' : [
							#actual numeric
							{ 'name' : "actual",
							  'field' : "numeric_rule_variable",
							  'label' : 'None',
							  'options' : 'None',
							  'formulae' : 'self.product.actual',
							  'input_method' : {'method' : 'API',
							                    'url' : 'https://541d0516-65f5-4002-a22d-c4dcafa91315.mock.pstmn.io/get',
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
							  'input_method' :  {'method' : 'API',
							                    'url' : 'https://541d0516-65f5-4002-a22d-c4dcafa91315.mock.pstmn.io/get',
							                    'params' : {},
							                    "command" : 'response.json()["expected"]',
							                    'evaluation' : None,
							                    'start' : None,
							                    'end' : None
							                    }
							  }
							],
                'actions' : [
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

				{'name' : 'case3',
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
			  'rules' : [
						#(expected == actual and expected < 100) or actual > expected 
						{ "conditions" : {'any' : [ { 'all': [{'name' : ["actual","expected"],
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
						}
						],
				'variables' : [
							#actual numeric
							{ 'name' : "actual",
							  'field' : "numeric_rule_variable",
							  'label' : 'None',
							  'options' : 'None',
							  'formulae' : 'self.product.actual',
							  'input_method' : {'method' : 'API',
							                    'url' : 'https://b774ca47-c8f5-4304-91ac-18800789f863.mock.pstmn.io',
							                    'params' : {},
							                    "command" : 'resonse.json()["actual"]',
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
                'actions' : [
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
 ]
#export rules (these are compulsory)
rules = [
#(expected == actual and expected < 100) or actual > expected 
{ "conditions" : {'any' : [ { 'all': [{'name' : ["actual","expected"],
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
}
]

with open('use_cases.txt', 'w') as outfile:  
    json.dump(use_cases, outfile)
with open('rules.txt', 'w') as outfile:  
    json.dump(rules, outfile)


#export variables (these are compulsory)
variables = [
#actual numeric
{ 'name' : "actual",
  'field' : "numeric_rule_variable",
  'label' : 'None',
  'options' : 'None',
  'formulae' : 'self.product.actual'
  },

#expected numeric
{ 'name' : "expected",
  'field' : "numeric_rule_variable",
  'label' : 'None',
  'options' : 'None',
  'formulae' : 'self.product.expected',
  }
]
with open('variables.txt', 'w') as outfile:  
    json.dump(variables, outfile)


#export actions (these are compulsory)
actions = [
{ 'name' : 'condition_pass',
  'params' : None,
  'formulae' : "print('All expected access points are present')"
  },
{ 'name' : 'condition_fail',
  'params' : None,
  'formulae' : "print('NOT all expected access points are present')"
}
]
with open('actions.txt', 'w') as outfile:  
    json.dump(actions, outfile)