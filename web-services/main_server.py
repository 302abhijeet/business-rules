import business_rules.API as API
import json
from utils import *
from flask import Flask,request,jsonify,Response
from sshtunnel import SSHTunnelForwarder
from pymongo import MongoClient

server = Flask(__name__)


dirpath = './business_rules/configuration_files/'

#conect to database
def _create_SSHtunnel():
    server = SSHTunnelForwarder(
        "10.137.89.13",
        ssh_username="ubuntu",
        ssh_password="rules_engine",
        remote_bind_address=('127.0.0.1', 27017)
    )
    return server

#Server route to run rules
@server.route('/runrule',methods=['POST'])
def runrule():
    server = _create_SSHtunnel()
    server.start()
    mydb = MongoClient("127.0.0.1",server.local_bind_port)["rules_engine"]
    if request.method == 'POST':
        data_given = request.args.to_dict()
        if 'rule' not in data_given:
                server._server_list[0].block_on_close = False
                server.stop()
                return Response(
                        response=json.dumps({'Error':'Please specify a rule'}),
                        mimetype='application/json',
                        status=400
                )
        rulename = data_given['rule']
        flag = check_valid_rule(rulename,mydb)
        if not flag:
            server._server_list[0].block_on_close = False
            server.stop()
            return  Response(
                        response=json.dumps({'Error':'Rule does not exist'}),
                        mimetype='application/json',
                        status=400
                )
        del data_given['rule']
        check_valid_data(data_given,mydb)
        #check if any data is in body or not
        parameter_data = checkValidatePD(request.get_data())
        
        #API function to run the rules
        #this function returns a list of messages
        try:
                data,file_path = API._run_API(run_rule=rulename,case=None,parameter_variables=data_given,parameter_dataSource=parameter_data,mydb=mydb)
                server._server_list[0].block_on_close = False
                server.stop()
        except Exception as e:
            server._server_list[0].block_on_close = False
            server.stop()
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
    server = _create_SSHtunnel()
    server.start()
    mydb = MongoClient("127.0.0.1",server.local_bind_port)["rules_engine"]
    if request.method == 'POST':
        #get the optional variable values as arguments
        data_given = request.args.to_dict()
        if 'use_case' not in data_given:
                server._server_list[0].block_on_close = False
                server.stop()
                return Response(
                        response=json.dumps({'Error':'Please specify a Use Case'}),
                        mimetype='application/json',
                        status=400
                )
        ucname = data_given['use_case']
        flag = check_valid_usecase(ucname,mydb)
        if not flag:
            server._server_list[0].block_on_close = False
            server.stop()
            return Response(
                        response=json.dumps({'Error':'Use case doesnot exist'}),
                        mimetype='application/json',
                        status=400
                )


        del data_given['use_case']
        check_valid_data(data_given,mydb)
        
        parameter_data = checkValidatePD(request.get_data())
        
        #this function returns a list of messages
        try:
            data,file_path = API._run_API(run_rule=None,case=ucname,parameter_variables=data_given,parameter_dataSource=parameter_data,mydb=mydb)
            server._server_list[0].block_on_close = False
            server.stop()
        except Exception as e:
            server._server_list[0].block_on_close = False
            server.stop()
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
def adddata(ty):
    if request.method == 'POST':
        try:
            server = _create_SSHtunnel()
            server.start()
            mydb = MongoClient("127.0.0.1",server.local_bind_port)["rules_engine"]
            collection = mydb[ty]
            data = request.get_data()
            if data != None:
                    data = eval(rule)
                    if type(data) == list:
                        collection.insert_many(data)
                    elif type(data) == dict:
                        collection.insert(data)
            server._server_list[0].block_on_close = False
            server.stop()
            return Response(
                            response=json.dumps({'run_msg':'Data added'}),
                            mimetype='application/json',
                            status=200
                    )
        except Exception as e:
            server._server_list[0].block_on_close = False
            server.stop()
            return Response(
                        response=json.dumps({'Error':str(e)}),
                        mimetype='application/json',
                        status=400
                )


#Server route to delete data
@server.route('/del/<ty>',methods = ['DELETE'])
def deldata(ty):
    if request.method == 'DELETE':
        try:
            server = _create_SSHtunnel()
            server.start()
            mydb = MongoClient("127.0.0.1",server.local_bind_port)["rules_engine"]
            collection = mydb[ty]

            querry = request.get_data()
            if querry:
                querry = eval(querry)
                deleted_count = collection.delete_many(querry)
            message = 'Entries deleted: '+str(deleted_count)
            sts = 200 if deleted_count > 0 else 400
            server._server_list[0].block_on_close = False
            server.stop()
            return Response(
                            response=json.dumps({'run_msg':message}),
                            mimetype='application/json',
                            status=sts
                    )
        except Exception as e:
            server._server_list[0].block_on_close = False
            server.stop()
            return Response(
                        response=json.dumps({'Error':str(e)}),
                        mimetype='application/json',
                        status=400
                )

#Server route to modify data
@server.route('/modify/<ty>',methods = ['POST'])
def modifydata(ty):
    if request.method == 'POST':
        try:
            server = _create_SSHtunnel()
            server.start()
            mydb = MongoClient("127.0.0.1",server.local_bind_port)["rules_engine"]
            collection = mydb[ty]
            
            data = request.get_data()
            if data!=None:
                    querry=eval(data)["querry"]
                    newData = eval(data)['newData']
                    modified_count = collection.update_many(querry,{"$set":newData}).modified_count
            msg = 'Entries updated: ' + str(modified_count)
            sts = 200 if modified_count > 0 else 400
            server._server_list[0].block_on_close = False
            server.stop()
            return Response(
                            response=json.dumps({'run_msg':msg}),
                            mimetype='application/json',
                            status=sts
                    )
        except Exception as e:
            server._server_list[0].block_on_close = False
            server.stop()
            return Response(
                        response=json.dumps({'Error':str(e)}),
                        mimetype='application/json',
                        status=400
                )

#Server route to get data
@server.route('/get/<ty>',methods = ['GET'])
def getdata(ty):
    if request.method=='GET':
        try:
            server = _create_SSHtunnel()
            server.start()
            mydb = MongoClient("127.0.0.1",server.local_bind_port)["rules_engine"]
            collection = mydb[ty]

            data = request.get_data()
            if data:
                querry = eval(data)
                result = collection.find(querry,{"_id":0})
                result = list(result) if result else None

            message = 'Data found' if result else 'data not found'
            sts = 200 if result  else 400
            server._server_list[0].block_on_close = False
            server.stop()
            return Response(
                        response=json.dumps({'run_msg':message,'data':data}),
                        mimetype='application/json',
                        status=sts
                )
        except Exception as e:
            server._server_list[0].block_on_close = False
            server.stop()
            return Response(
                        response=json.dumps({'Error':str(e)}),
                        mimetype='application/json',
                        status=400
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