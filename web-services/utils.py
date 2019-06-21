import yaml

#to check if variables exists
def check_valid_data(data_given):
        with open('./business_rules/configuration_files/variables.yml') as f:
                variables = yaml.load(f, Loader=yaml.FullLoader)
        to_be_removed = []
        for d in data_given:
                if d not in variables:
                        to_be_removed.append(d)

        for d in to_be_removed:
                del data_given[d]  

#to check if rule exists
def check_valid_rule(rulename):
    with open('./business_rules/configuration_files/rules.yml') as f:
        rule_list = yaml.load(f,Loader=yaml.FullLoader)
    if rulename not in rule_list:
        return False
    return True

#to check if use case exist
def check_valid_usecase(ucname):
    with open('./business_rules/configuration_files/use_cases.yml') as f:
        uc_list = yaml.load(f,Loader=yaml.FullLoader)
    if ucname not in uc_list:
        return False
    return True