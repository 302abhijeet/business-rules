import business_rules.API as API
import json
from utils import *
from flask import Flask,request,jsonify,Response,send_file
from pymongo import MongoClient
from flask_cors import CORS

server = Flask(__name__)
CORS(server)

dirpath = './business_rules/configuration_files/'

@server.route('/return-files/')
def return_files_tut():
    try:
        data=request.args.to_dict()
        return send_file(data["file"], attachment_filename=data["file"][9:])
    except Exception as e:
        return str(e)


@server.route('/runrule',methods=['POST'])
def runrule():
    """run rule given by user
    
    Returns:
        response -- response to be given to user
    """
    main_server.output = []
    mydb = MongoClient("127.0.0.1",27017)["rules_engine"]
    if request.method == 'POST':
        data_given = request.args.to_dict()
        if 'rule' not in data_given:
                return Response(
                        response=json.dumps({'Error':'Please specify a rule'}),
                        mimetype='application/json',
                        status=400
                )
        rulename = data_given['rule']
        flag = check_valid_rule(rulename,mydb)
        if not flag:
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
            
        except Exception as e:
            try:
                with open(str(e),'r') as f:
                    return  Response(
                            response=json.dumps({'parameter_warnings':main_server.output,'file':str(e)}),
                            mimetype='application/json',
                            status=500
                    )
            except:
                pass
            return  Response(
                    response=json.dumps({'parameter_warnings':main_server.output,'error':str(e)}),
                    mimetype='application/json',
                    status=500
            )
        return  Response(
                        response=json.dumps({'run_msg':'Run successful','data':data,'file':file_path,'parameter_warnings':main_server.output,}),
                        mimetype='application/json',
                        status=200
                )
       
            
#Server route to run use cases
@server.route('/runusecase',methods = ["POST"])
def runusecase():
    """run use_case requested by use
    
    Returns:
        response -- response to be given to user
    """
    main_server.output = []
    mydb = MongoClient("127.0.0.1",27017)["rules_engine"]
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
        flag = check_valid_usecase(ucname,mydb)
        if not flag:
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
            
            
        except Exception as e:
            
            
            try:
                with open(str(e),'r') as f:
                    return  Response(
                            response=json.dumps({'parameter_warnings':main_server.output,'file':str(e)}),
                            mimetype='application/json',
                            status=500
                        )
            except:
                pass 
            return  Response(
                        response=json.dumps({'parameter_warnings':main_server.output,'Error':str(e)}),
                        mimetype='application/json',
                        status=500
                    ) 
        return Response(
                        response=json.dumps({'run_msg':'run successful','data':data,'file':file_path,'parameter_warnings':main_server.output}),
                        mimetype='application/json',
                        status=200
                )


#Server route to add data
@server.route('/add/<ty>',methods = ['POST'])
def adddata(ty):
    """add data sent by user databse
    
    Arguments:
        ty {collection} -- collection in databses to be appended
    
    Returns:
        response -- response to be given to user
    """
    if request.method == 'POST':
        try:
            mydb = MongoClient("127.0.0.1",27017)["rules_engine"]
            collection = mydb[ty]
            data = json.loads(request.get_data())
            if data != None:
                    if type(data) == list:
                        collection.insert_many(data)
                    elif type(data) == dict:
                        collection.insert(data)
            return Response(
                            response=json.dumps({'run_msg':'Data added'}),
                            mimetype='application/json',
                            status=200
                    )
        except Exception as e:
            return Response(
                        response=json.dumps({'Error':str(e)}),
                        mimetype='application/json',
                        status=400
                )


#Server route to delete data
@server.route('/del/<ty>',methods = ['POST'])
def deldata(ty):
    """delete data from databse
    
    Arguments:
        ty {collection} -- collection from which data is to be deleted
    
    Returns:
        response -- response to be given to user
    """
    if request.method == 'POST':
        try:
            mydb = MongoClient("127.0.0.1",27017)["rules_engine"]
            collection = mydb[ty]
            querry = json.loads(request.get_data())
            if querry:
                deleted_count = collection.delete_many(querry).deleted_count
            message = 'Entries deleted: '+str(deleted_count)
            sts = 200 if deleted_count > 0 else 400
            return Response(
                            response=json.dumps({'run_msg':message}),
                            mimetype='application/json',
                            status=sts
                    )
        except Exception as e:
            return Response(
                        response=json.dumps({'Error':str(e)}),
                        mimetype='application/json',
                        status=400
                )

#Server route to modify data
@server.route('/modify/<ty>',methods = ['POST'])
def modifydata(ty):
    """modify the databse 
    
    Arguments:
        ty {collection} -- collection to be modified
    
    Returns:
        response -- response to be given to user
    """
    if request.method == 'POST':
        try:
            mydb = MongoClient("127.0.0.1",27017)["rules_engine"]
            collection = mydb[ty]
            data = json.loads(request.get_data())
            if data!=None:
                    querry=data["querry"]
                    newData = data['newData']
                    modified_count = collection.delete_many(querry).deleted_count
                    collection.insert(newData)
            msg = 'Entries updated: ' + str(modified_count)
            sts = 200 if modified_count > 0 else 400
            return Response(
                            response=json.dumps({'run_msg':msg}),
                            mimetype='application/json',
                            status=sts
                    )
        except Exception as e:
            return Response(
                        response=json.dumps({'Error':str(e)}),
                        mimetype='application/json',
                        status=400
                )

#Server route to get data
@server.route('/get/<ty>',methods = ['GET'])
def getdata(ty):
    """send data from database to GUI
    
    Arguments:
        ty {collection} -- collection which is requested
    
    Returns:
        response -- response to be given to user
    """
    if request.method=='GET':
        try:
            mydb = MongoClient("127.0.0.1",27017)["rules_engine"]
            collection = mydb[ty]
            result = collection.find({},{"_id":0})
            result = list(result) if result else None
            message = 'Data found' if result else 'data not found'
            sts = 200 if result  else 400            
            return Response(
                        response=json.dumps({'run_msg':message,'data':result}),
                        mimetype='application/json',
                        status=sts
                )
        except Exception as e:
            return Response(
                        response=json.dumps({'Error':str(e)}),
                        mimetype='application/json',
                        status=400
                )
        


@server.errorhandler(500)
def internal_error(error):
    """response in case of internal error
    
    Arguments:
        error {Exception} -- internal error hat occured
    
    Returns:
        response -- response to be given to user
    """
    print(error)
    return Response(status = 500,response=json.dumps({'Error':'Internal server error'}))

@server.errorhandler(405)
def bad_method(error):
    """error for bad method

    Returns:
        response -- response to be given to user
    """
    return Response(status=405,response=json.dumps({'Error':'Method not allowed'}))

@server.errorhandler(404)
def not_found(error):
    """error if module not found
    
    Arguments:
        error {Exception} -- error that raised the function
    
    Returns:
        response -- response to be given to user
    """
    return Response(status=404,response=json.dumps({'Error':'Route not found'}))

if __name__ == "__main__":
    server.run(port = 5000)