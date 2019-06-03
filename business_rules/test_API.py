#test API for runing some basic tests on the engine

#input variables
class ProductVariables(BaseVariables):

    def __init__(self, product):
        self.product = product

    @numeric_rule_variable
    def actual(self):
        return self.product.current

    @numeric_rule_variable
    def expected(self):
        return self.product.actual


#action variables
class ProductActions(BaseActions):

    def __init__(self, product):
        self.product = product

    @rule_action
    def condition_pass(self):
        print("All expected access points are present")
    
    @rule_action
    def condition_fail(self) :
        print("NOT all expected access points are present")


#build rules
rules = [
#expected == actual
{ "conditions" : {  'name' : ["actual","expected"]
					'operator' : "equal_to"
				    'value' : None
				 },
  "action_true" : [ { 'name' : "condition_pass",
                  'params': None}],
  "action_false": [ { 'name' : "condition_fail",
                  'params': None}],
}
]
