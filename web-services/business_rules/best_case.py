#file for allocatng best use case
import json


#function for returning best cases rules :
def case_rules(use_cases,parameters):
    best_match = 0
    best_case = []
    #loop for finding match of each case
    for case in use_cases : 
        #loop for finding match of each correllated param
        for param in case:
            #loop for finding match for each param in correlated param
            for name in case[param]['param'] :
                if name in parameters:
                    actual = parameters[name]
                    case[param]['param'][name]['match'] = exec(case[param]['param'][name]['formulae'])
                else :
                    case[param]['param'][name]['match'] = 0
                case[param]['match'] += case[param]['param'][name]['match'] * case[param]['param'][name]['percentage']  
            case['match'] += case[param]['match'] * case[param]['percentage']
        if case['match'] > best_match:
            best_match = case['match']
            best_case = [case]
        elif case['match'] == best_match:
            #decide what to do
            best_case.append(case)
    return best_case    
