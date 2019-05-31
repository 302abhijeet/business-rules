#UI for the API

#input variables
flag = True
variables = []
var = {'name' : '','field' : '', 'label' : '', 'options' : '', 'formulae' : ''}
print("Enter Variables : ")
while flag:
	print("Name : ")
	var['name'] = input()
	print("Field : ")
	var['field'] = input()
	print("label : ")
	var['label'] = input()
	print("options : ")
	var['options'] = input()
	lines = []
	while True:
	    line = input()
	    if line:
	        lines.append(line)
	    else:
	        break
	var['formulae'] = '\n'.join(lines)

	variables.append(var)

	print("Enter 0 to exit:")
	if input() == 0 :
		break


#input actions
flag = True
actions = []
act = {'name' : '','params' : {},'formulae' : ''}
print("Enter Actions : ")
while flag:
	print("Name : ")
	act['name'] = input()
	prm = {}
	while flag :
        print("Parameters name and type: ")
        act['params'].add(input(),input())    #field type has to be changed from string
	while True:
	    line = input()
	    if line:
	        lines.append(line)
	    else:
	        break
	var['formulae'] = '\n'.join(lines)

	print("Enter 0 to exit:")
	if input() == 0 :
		break


#input rules

#contruct rules on own without input for now


#save variable
with open('variables.txt', 'w') as f:
        json.dump(variables, f)


#save actions
with open('actions.txt', 'w') as f:
        json.dump(actions, f)


#save variable
with open('rules.txt', 'w') as f:
        json.dump(rules, f)