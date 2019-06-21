import business_rules.API as API
from filehandler import *
from utils import *
from flask import Flask,request,jsonify,Response

server = Flask(__name__)


dirpath = './business_rules/configuration_files/'


#Server route to run rules
@server.route('/runrule',methods=['GET'])
def runrule():
    if request.method == 'GET':
        data_given = request.args.to_dict()
        if 'rule' not in data_given:
                return jsonify({'msg':'please specify a rule'})
        rulename = data_given['rule']
        flag = check_valid_rule(rulename)
        if not flag:
            return jsonify({'msg':'Rule does not exist'})
        del data_given['rule']
        check_valid_data(data_given)
        #API function to run the rules
        
        API._run_API(run_rule=rulename,case=None,parameter_variables=data_given)
        return jsonify({'msg':'run successful'})
       
            
#Server route to run use cases
@server.route('/runusecase',methods = ["GET"])
def runusecase():
    if request.method == 'GET':
        #get the optional variable values as arguments
        data_given = request.args.to_dict()
        #API function to run the use cases
        data_given = request.args.to_dict()
        if 'use_case' not in data_given:
                return jsonify({'msg':'please specify a use case'})
        ucname = data_given['use_case']
        flag = check_valid_usecase(ucname)
        if not flag:
            return jsonify({'msg':'Use case does not exist'})


        del data_given['use_case']
        check_valid_data(data_given)
        
        API._run_API(run_rule=None,case=ucname,parameter_variables=data_given)
        return jsonify({'msg':'run successful'})


#Server route to add data
@server.route('/add/<ty>',methods = ['POST'])
def addrule(ty):
    if request.method == 'POST':
        
        filepath = updateFilePath(dirpath,ty) 
        if filepath == False:
                return jsonify({'msg':'Wrong type'})
        

        rule = request.get_data()
        if rule != None:
                rule = eval(rule)
    
        
                appendData(filepath,rule)

        return jsonify({'msg':'file updated'})

#Server route to delete data
@server.route('/del/<ty>',methods = ['DELETE'])
def delrule(ty):
    if request.method == 'DELETE':

        filepath = updateFilePath(dirpath,ty) 
        if filepath == False:
                return jsonify({'msg':'Wrong type'})

        id = request.args['id']
        flag = deleteData(filepath,id)
        message = 'file updated' if flag is True else 'error'
        return jsonify({'msg':message})

#Server route to modify data
@server.route('/modify/<ty>',methods = ['POST'])
def modifyrule(ty):
    if request.method == 'POST':

        filepath = updateFilePath(dirpath,ty) 
        if filepath == False:
                return jsonify({'msg':'Wrong type'})

        flag =False
        rule = request.get_data()
        if rule!=None:
                rule=eval(rule)
                flag = updateRule(filepath,rule)
        msg = 'Rule updated' if flag else 'Rule with specified id not found'
    return jsonify({'msg':msg})

#Server route to get data
@server.route('/get/<ty>',methods = ['GET'])
def getrule(ty):
    if request.method=='GET':

        filepath = updateFilePath(dirpath,ty) 
        if filepath == False:
                return jsonify({'msg':'Wrong type'})

        id = request.args['id']
        if id == 'all':
            data = getAllRules(filepath,id)
        else:
            data = getSpecificRule(filepath,id)

        message = 'data found' if data != False else 'data not found'
        return jsonify({'msg':message,'data':data})


@server.errorhandler(500)
def internal_error(error):
    print(error)
    return Response(status = 500)



if __name__ == "__main__":
    server.run(port = 5000,debug=False)