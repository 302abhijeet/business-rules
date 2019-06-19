import os,yaml

def appendData(filename,rule):
    data= {}
    if os.stat(filename).st_size == 0:
        data.update(rule)
    else:
        with open(filename,'r') as f:
            data = yaml.load(f)
            data.update(rule)
    with open(filename,'w') as f:
        yaml.dump(data,f)

    
def deleteData(filename,id):
    with open(filename,'r') as f:
        data = yaml.load(f)
        try:
            del data[id]
        except:
            return False
        
    with open(filename,'w') as f:
        yaml.dump(data,f)
    return True

def checkFileExists(filename):
    if not os.path.isfile(filename):
        with open(filename,'w'):
            print('Creating %s'%filename)
            pass
        
def getAllRules(filename,id):
    with open(filename,'r') as f:
        data = yaml.load(f)
    
    return data

def getSpecificRule(filename,id):
    with open(filename,'r') as f:
        data = yaml.load(f)
        for key in data.keys():
            if key == id:
                return data[key]
        return False

def updateRule(filename,newrule):
    with open(filename,'r') as f:
        data= yaml.load(f)
        key = list(newrule.keys())[0]
        if key in data.keys():
            data.update(newrule)
            
            with open(filename,'w') as f:
                yaml.dump(data,f)
            return True
    return False

