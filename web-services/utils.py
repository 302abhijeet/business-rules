import main_server

#to check if variables exists
def check_valid_data(data_given,mydb):
        variables = mydb["variables"]
        to_be_removed = []
        for d in data_given:
                if not variables.find_one({"name":d}):
                        to_be_removed.append(d)

        for d in to_be_removed:
                del data_given[d]  

#to check if rule exists
def check_valid_rule(rulename,mydb):
    rule_list = mydb["rules"]
    if not rule_list.find_one({"name":rulename}):
        return False
    return True

#to check if use case exist
def check_valid_usecase(ucname,mydb):
    uc_list = mydb["use_cases"]
    if not uc_list.find_one({"name":ucname}):
        return False
    return True

#to check and validate parameter data
def checkValidatePD(data):
        if not data:
                return []
        
        data =  eval(data)
        type_allowed = ['API','SSH','data_base','derived']
        
        for d in data:
                if d['method'] not in type_allowed:
                        data.remove(d)
        return data
