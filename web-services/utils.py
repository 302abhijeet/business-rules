import main_server
import json

#to check if variables exists
def check_valid_data(data_given,mydb):
        variables = mydb["variables"]
        to_be_removed = []
        for d in data_given:
                if not variables.find_one({"name":d}):
                        main_server.output.append("parameter variable: {} not defined in database!".format(d))
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
        
        data =  json.loads(data)
        to_be_removed = []
        
        for d in data:
                if d['method'] == "API":
                    if not {"name","method","request","url","cache","multi_thread","params","variables"}.issubset(d.keys()) or (d["request"]=="post" and "data" not in d):
                        main_server.output.append("DataSource: {} mandatory arguments are missing!".format(d))
                        to_be_removed.append(d)
                elif d["method"] == "SSH":
                    if not {"name","method","host_name","user_name","cache","password","key_filename","variables","multi_thread"}.issubset(d.keys()):
                            main_server.output.append("DataSource: {} mandatory arguments are missing!".format(d))
                            to_be_removed.append(d)
                elif d["method"] == "database":
                    if not {"name","method","host_name","user_name","cache","password","data_base","variables","multi_thread"}.issubset(d.keys()):
                            main_server.output.append("DataSource: {} mandatory arguments are missing!".format(d))
                            to_be_removed.append(d)
                else:
                        main_server.output.append("DataSource method: {} not defined in database!".format(d))
                        data.remove(d)
        for d in to_be_removed:
            data.remove(d)
        return data
