from flask import Flask,jsonify,request
from filehandler import *
import yaml

app = Flask(__name__)
filename = '../business_rules/rules.yml'

#endpoint to add a new rule to rules.json
@app.route('/addrule',methods=['POST'])
def addrule():
    if request.method == 'POST':
        rule = request.get_data()
        if rule != None:
                rule = eval(rule)
                appendData(filename,rule)

        return jsonify({'msg':'file updated'})

#endpoint to delete a rule, requires rule id
@app.route('/delrule',methods=['DELETE'])
def delrule():
    if request.method == 'DELETE':
        id = request.args['id']
        flag = deleteData(filename,id)
        message = 'file updated' if flag is True else 'error'
        return jsonify({'msg':message})

#endpoint to get all or specific rules
@app.route('/getrule',methods=['GET'])
def getrule():
    if request.method=='GET':
        id = request.args['id']
        if id == 'all':
            data = getAllRules(filename,id)
        else:
            data = getSpecificRule(filename,id)

        message = 'Rules found' if data != False else 'Rule not found'
        return jsonify({'msg':message,'rules':data})

#endpoint to modify a specific rule
@app.route('/modifyrule',methods=['POST'])
def modifyrule():
    if request.method == 'POST':
        flag =False
        rule = request.get_data()
        if rule!=None:
                rule=eval(rule)
                flag = updateRule(filename,rule)
        msg = 'Rule updated' if flag else 'Rule with specified id not found'
    return jsonify({'msg':msg})


if __name__ == "__main__":
    checkFileExists(filename)
    print('Starting server')
    app.run(port=5050,debug=True)