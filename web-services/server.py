'''
    Web service to run rules/use cases
    Endpoints to run rules/use cases by:
     - Category/use cases
     - Name
    Optional inputs are possible too
'''
import business_rules.API as API
from flask import Flask,request,jsonify
import yaml


server = Flask(__name__)



def check_valid_data(data_given):
        with open('./business_rules/configuration_files/variables.yml') as f:
                variables = yaml.load(f)
        to_be_removed = []
        for d in data_given:
                if d not in variables:
                        to_be_removed.append(d)

        for d in to_be_removed:
                del data_given[d]                        
#route to run rules
@server.route('/runrule',methods = ['GET'])
def runrule():
    if request.method == 'GET':
        #get the optional variable values as arguments`
        data_given = request.args.to_dict()
        if 'rule' not in data_given:
                return jsonify({'msg':'please specify a rule'})
        rulename = data_given['rule']
        del data_given['rule']
        check_valid_data(data_given)
        #API function to run the rules
        API._run_API(run_rule=rulename,case=None,parameter_variables=data_given)
        return jsonify({'msg':'run successful'})


#route to run use cases
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
        del data_given['use_case']
        check_valid_data(data_given)
        API._run_API(run_rule=None,case=ucname,parameter_variables=data_given)
        return jsonify({'msg':'run successful'})




if __name__ == "__main__":
    server.run(port=5000,debug=True)