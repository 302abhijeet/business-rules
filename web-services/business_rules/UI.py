#UI for the API
import json

#input rules
flag = True
with open('rules.txt') as f:
    rules = json.load(f)
with open('variables.txt') as f:
    variables = json.load(f)
with open('actions.txt') as f:
    actions = json.load(f)

while flag :
    cond = {'conditions' : {},'actions_true' : [], 'actions_false' : []}
    print("Enter conditions : ")
    c = []
    c.append(cond["conditions"])
    count = 0
    while flag: #Loop through for all and any
        print("Enter 0 if only one condition or to exit: ")
        if input() == '0':
            break
        print("Enter condition connector if any or all: ")
        c[count][input()] = []
        count += 1
        c.append([])
        for key in c[count-1] :
            c[count] = c[count-1][key]

    while(count >= 0) :  # Loop for entering all all's and any's conditions
        while flag:   #for taking in multiple conditions
            pred = {'name': [],'operator': '','value': ''}
            while flag :   #for taking in all variables
                print("Enter input variable name, field, label, options and formulae :")
                var = {'name' : input(), 'field' : input(),'label' : input(),'options' : input(),'formulae' : input()}
                if var not in variables :
                    variables.append(var)
                pred['name'].append(var['name'])
                print("Enter 0 to exit input variables :")
                if input() == '0':
                    break
            print("Enter operator and value: ")
            pred['operator'] = input()
            pred['value'] = exec(input())
            if count == 0 :
                cond['conditions'] = pred
                break
            c[count].append(pred)
            print("Enter 0 to exit conditions :")
            if input() == '0' :
                break
        count -= 1
        if(count == 0) :
            break

    while flag:
        print("Enter action_true name: ")
        act = {}
        act['name'] = input()
        act['params'] = {}
        while flag :
            print("Enter 0 to exit params:")
            if input() == '0':
                act['params'] = None
                break
            print("Enter parameter value and name:")
            act['params'][input()] = exec(input())
        cond['actions_true'].append(act)
        print("Enter formulae for actions_true: ")
        act['formulae'] = input()
        if act not in actions :
            actions.append(act)
        print("Enter 0 to exit actions_true:")
        if input() == '0':
            break

    while flag:
        print("Enter actions_false name: ")
        act = {}
        act['name'] = input()
        act['params'] = {}
        while flag :
            print("Enter 0 to exit params:")
            if input() == '0':
                act['params'] = None
                break
            print("Enter parameter value and name:")
            act['params'][input()] = exec(input())
        cond['actions_false'].append(act)
        print("Enter formulae for actions_false: ")
        act['formulae'] = input()
        if act not in actions :
            actions.append(act)
        print("Enter 0 to exit actions_false:")
        if input() == '0':
            break

    rules.append(cond)
    print("Enter 0 to exit rules: ")
    if input() == '0' : 
        break


#save variable
with open('variables.txt', 'w') as f:
        json.dump(variables, f)


#save actions
with open('actions.txt', 'w') as f:
        json.dump(actions, f)


#save variable
with open('rules.txt', 'w') as f:
        json.dump(rules, f)