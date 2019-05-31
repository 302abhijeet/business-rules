#API for the Rule based engine

from business_rules import run_all
import json

#import prodcut variables from UI
with open('variables.json') as f:
    variables = json.load(f)


#create ruleVariables
class ProductVariables(BaseVariables):

    def __init__(self, product):
        self.product = product

    for var in variables :
    	if var['options'] == 'None' :
	    	exec("@" + var['field'] + "(" + var['label'] + ")" + """
	    	def """ + var['name'] + """(self):
		    	return """ + var['formulae'])
	    else :
	    	exec("@" + var['field'] + "(" + var['label'] + "," + var['options'] + """)
	    	def """ + var['name'] + """(self):
		    	return """ + var['formulae'])


#import product actions from UI
with open('actions.json') as f:
    actions = json.load(f)


#Create ruleActions
class ProductActions(BaseActions):

    def __init__(self, product):
        self.product = product

    for act in actions : 
		li = []
    	for args in act['params'] :
    		li.append(args)
    	args = "(self," + ','.join(li) + ")"
    	@rule_action(params = act['params'])
    	exec("def " + act['name'] + args + """ :
    		""" + act["formulae"])


#take the input rules
with open('rules.json') as f:
    rules = json.load(f)


#access the database to get all products


#run the engine
for product in Products.objects.all():
    run_all(rule_list=rules,
            defined_variables=ProductVariables(product),
            defined_actions=ProductActions(product),
            stop_on_first_trigger=True
           )
