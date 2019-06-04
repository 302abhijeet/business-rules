import json

#export rules
rules = [
#expected == actual
{ "conditions" : {  'name' : ["actual","expected"],
					'operator' : "equal_to",
				    'value' : None
				 },
  "actions_true" : [ { 'name' : "condition_pass",
                       'params' : None}],
  "actions_false": [ { 'name' : "condition_fail",
                       'params' : None}],
}
]

with open('rules.txt', 'w') as outfile:  
    json.dump(rules, outfile)


#export variables
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


#export actions
actions = [
{ 'name' : 'condition_pass',
  'params' : None,
  'formulae' : "print('All expected access points are present')"
  },
{ 'name' : 'condition_fail',
  'params' : None,
  'formulae' : "print('NOT all expected access points are present')"
}]
with open('actions.txt', 'w') as outfile:  
    json.dump(actions, outfile)