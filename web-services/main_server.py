import business_rules.API as API
import json
from filehandler import *
from utils import *
from flask import Flask,request,jsonify,Response
from flask_cors import CORS

server = Flask(__name__)
CORS(server)

dirpath = './business_rules/configuration_files/'


#Server route to run rules
@server.route('/runrule',methods=['POST'])
def runrule():
    if request.method == 'POST':
        data_given = request.args.to_dict()
        if 'rule' not in data_given:
                return Response(
                        response=json.dumps({'Error':'Please specify a rule'}),
                        mimetype='application/json',
                        status=400
                )
        rulename = data_given['rule']
        flag = check_valid_rule(rulename)
        if not flag:
            return  Response(
                        response=json.dumps({'Error':'Rule doesnot exist'}),
                        mimetype='application/json',
                        status=400
                )
        del data_given['rule']
        check_valid_data(data_given)
        #check if any data is in body or not
        parameter_data = checkValidatePD(request.get_data())
        
        #API function to run the rules
        #this function returns a list of messages
        try:
                data,file_path = API._run_API(run_rule=rulename,case=None,parameter_variables=data_given,parameter_dataSource=parameter_data)
        except Exception as e:
            try:
                with open(str(e),'r') as f:
                    return  Response(
                            response=json.dumps({'file':str(e)}),
                            mimetype='application/json',
                            status=500
                    )
            except:
                pass
            return  Response(
                    response=json.dumps({'file':str(e)}),
                    mimetype='application/json',
                    status=500
            )
        return  Response(
                        response=json.dumps({'run_msg':'Run successful','data':data,'file':file_path}),
                        mimetype='application/json',
                        status=200
                )
       
            
#Server route to run use cases
@server.route('/runusecase',methods = ["POST"])
def runusecase():
    if request.method == 'POST':
        #get the optional variable values as arguments
        data_given = request.args.to_dict()
        if 'use_case' not in data_given:
               return Response(
                        response=json.dumps({'Error':'Please specify a Use Case'}),
                        mimetype='application/json',
                        status=400
                )
        ucname = data_given['use_case']
        flag = check_valid_usecase(ucname)
        if not flag:
            return Response(
                        response=json.dumps({'Error':'Use case doesnot exist'}),
                        mimetype='application/json',
                        status=400
                )


        del data_given['use_case']
        check_valid_data(data_given)
        
        parameter_data = checkValidatePD(request.get_data())
        
        #this function returns a list of messages
        try:
            data,file_path = API._run_API(run_rule=None,case=ucname,parameter_variables=data_given,parameter_dataSource=parameter_data)
        except Exception as e:
            try:
                with open(str(e),'r') as f:
                    return  Response(
                            response=json.dumps({'file':str(e)}),
                            mimetype='application/json',
                            status=500
                        )
            except:
                pass 
            return  Response(
                        response=json.dumps({'Error':str(e)}),
                        mimetype='application/json',
                        status=500
                    ) 
        return Response(
                        response=json.dumps({'run_msg':'run successful','data':data,'file':file_path}),
                        mimetype='application/json',
                        status=200
                )


#Server route to add data
@server.route('/add/<ty>',methods = ['POST'])
def addrule(ty):
    if request.method == 'POST':
        
        filepath = updateFilePath(dirpath,ty) 
        if filepath == False:
                return Response(
                        response=json.dumps({'Error':'Wrong type'}),
                        mimetype='application/json',
                        status=400
                )
        

        rule = request.get_data()
        if rule != None:
                rule = eval(rule)
    
        
                appendData(filepath,rule)

        return Response(
                        response=json.dumps({'run_msg':'Data added'}),
                        mimetype='application/json',
                        status=200
                )

#Server route to delete data
@server.route('/del/<ty>',methods = ['DELETE'])
def delrule(ty):
    if request.method == 'DELETE':

        filepath = updateFilePath(dirpath,ty) 
        if filepath == False:
                return Response(
                        response=json.dumps({'Error':'Wrong type'}),
                        mimetype='application/json',
                        status=400
                )

        id = request.args['id']
        flag = deleteData(filepath,id)
        message = 'Data deleted' if flag is True else id+' doesnot exist'
        sts = 200 if flag is True else 400
        return Response(
                        response=json.dumps({'run_msg':message}),
                        mimetype='application/json',
                        status=sts
                )

#Server route to modify data
@server.route('/modify/<ty>',methods = ['POST'])
def modifyrule(ty):
    if request.method == 'POST':

        filepath = updateFilePath(dirpath,ty) 
        if filepath == False:
                return Response(
                        response=json.dumps({'Error':'Wrong type'}),
                        mimetype='application/json',
                        status=400
                )

        flag =False
        rule = request.get_data()
        if rule!=None:
                rule=eval(rule)
                flag = updateRule(filepath,rule)
        
        msg = 'Data updated' if flag else 'Data with specified id not found'
        sts = 200 if flag is True else 400

        return Response(
                        response=json.dumps({'run_msg':msg}),
                        mimetype='application/json',
                        status=sts
                )
#Server route to get data
@server.route('/get/<ty>',methods = ['GET'])
def getrule(ty):
    if request.method=='GET':

        filepath = updateFilePath(dirpath,ty) 
        if filepath == False:
                return Response(
                        response=json.dumps({'Error':'Wrong type'}),
                        mimetype='application/json',
                        status=400
                )

        id = request.args['id']
        if id == 'all':
            data = getAllRules(filepath,id)
        else:
            data = getSpecificRule(filepath,id)

        message = 'Data found' if data != False else 'data not found'
        sts = 200 if data!=False  else 400
        return Response(
                        response=json.dumps({'run_msg':message,'data':data}),
                        mimetype='application/json',
                        status=sts
                )
        


@server.errorhandler(500)
def internal_error(error):
    print(error)
    return Response(status = 500,response=json.dumps({'Error':'Internal server error'}))

@server.errorhandler(405)
def bad_method(error):
        return Response(status=405,response=json.dumps({'Error':'Method not allowed'}))

@server.errorhandler(404)
def not_found(error):
        return Response(status=404,response=json.dumps({'Error':'Route not found'}))

if __name__ == "__main__":
    server.run(port = 5000,debug=True)