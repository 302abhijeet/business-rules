'''
    Web service to run rules/use cases
    Endpoints to run rules/use cases by:
     - Category/use cases
     - Name
    Optional inputs are possible too
'''
import sys
sys.path.append('C:\\Users\\avij\\Documents\\busrules\\SNU-RuleEngine\\business_rules')
from flask import Flask,request,jsonify
import yaml
import API
server = Flask(__name__)

#route to run rules
@server.route('/runrule',methods = ['GET'])
def runrule():
    if request.method == 'GET':
        #get the optional variable values as arguments
        data_given = request.args.to_dict()
        #API function to run the rules
        API._run_API(run_rule='rule1',case='case2',parameter_variables={'expected':2,'actual':3,'correct':5})
        return jsonify({'msg':'run successful'})


#route to run use cases
@server.route('/runusecase',methods = ["GET"])
def runusecase():
    if request.method == 'GET':
        #get the optional variable values as arguments
        data_given = request.args.to_dict()
        #API function to run the use cases
        API._run_API(run_rule=None,case='case2',parameter_variables={'expected':2,'actual':3,'correct':5})





if __name__ == "__main__":
    #get data from config files
    server.run(port=5000,debug=True)