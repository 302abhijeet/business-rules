from flask import Flask,jsonify,request
from filehandler import *
import yaml

app = Flask(__name__)
dirpath = './business_rules/configuration_files/'

#endpoint to add a new rule
@app.route('/add/<ty>',methods=['POST'])
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

#endpoint to delete a rule, requires rule id
@app.route('/del/<ty>',methods=['DELETE'])
def delrule(ty):
    if request.method == 'DELETE':

        filepath = updateFilePath(dirpath,ty) 
        if filepath == False:
                return jsonify({'msg':'Wrong type'})

        id = request.args['id']
        flag = deleteData(filepath,id)
        message = 'file updated' if flag is True else 'error'
        return jsonify({'msg':message})

#endpoint to get all or specific rules
@app.route('/get/<ty>',methods=['GET'])
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

#endpoint to modify a specific rule
@app.route('/modify/<ty>',methods=['POST'])
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



if __name__ == "__main__":
    checkFilesExists(dirpath)
    print('Starting server')
    app.run(port=5050,debug=True)