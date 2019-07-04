import os,yaml

def appendData(filepath,rule):
    data= {}
    if os.stat(filepath).st_size == 0:
        data.update(rule)
    else:
        with open(filepath,'r') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            data.update(rule)
    with open(filepath,'w') as f:
        yaml.dump(data,f)

    
def deleteData(filepath,id):
    with open(filepath,'r') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        try:
            del data[id]
        except:
            return False
        
    with open(filepath,'w') as f:
        yaml.dump(data,f)
    return True

def checkFilesExists(filepath):
    if not os.path.isfile(filepath+'rules.yml'):
        with open(filepath+'rules.yml','w'):
            print('Creating rules.yml')
    if not os.path.isfile(filepath+'variables.yml'):
        with open(filepath+'variables.yml','w'):
            print('Creating variables.yml')
    if not os.path.isfile(filepath+'use_cases.yml'):
        with open(filepath+'use_cases.yml','w'):
            print('Creating use_cases.yml')

    if not os.path.isfile(filepath+'actions.yml'):
        with open(filepath+'actions.yml','w'):
            print('Creating actions.yml')
              
        
def getAllRules(filepath,id):
    with open(filepath,'r') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    
    return data

def getSpecificRule(filepath,id):
    with open(filepath,'r') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        for key in data.keys():
            if key == id:
                return data[key]
        return False

def updateRule(filepath,newrule):
    with open(filepath,'r') as f:
        data= yaml.load(f, Loader=yaml.FullLoader)
        key = list(newrule.keys())[0]
        if key in data.keys():
            data.update(newrule)
            
            with open(filepath,'w') as f:
                yaml.dump(data,f)
            return True
    return False

def updateFilePath(filepath,ty):
    if ty == 'use_case':
        filepath += 'use_cases.yml'
    elif ty == 'rule':
        filepath += 'rules.yml'
    elif ty == 'variables':
        filepath += 'variables.yml'
    elif ty == 'action':
        filepath += 'actions.yml'
    elif ty == 'datasource':
        filepath+= 'DataSource.yml'
    else:
        return False
    return filepath