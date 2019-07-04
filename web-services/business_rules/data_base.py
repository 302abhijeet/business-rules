    #Database module

import mysql.connector
def _start_connection(source):
    """connect to database source
    
    Arguments:
        source {dict} -- source to be connected to
    
    Raises:
        RuntimeError: couldn't connect to host
    
    Returns:
        mysql -- mysql object connected to database
    """
    try:
        mydb = mysql.connector.connect(
            host=source['host_name'],
            user=source['user_name'],
            passwd=source['password'],
            database=source['data_base']
                )
        return mydb
    except Exception as e:
        raise RuntimeError("Couldn't connect to database host!Error: {}".format(e))

def _get_variable_output(var,mydb):
    """get desired output from response
    
    Arguments:
        var {dict} -- variable[var] in config file
        mydb {mysql} -- mysql object connected to host
    
    Raises:
        RuntimeError: Error in config files commands of variable
        RuntimeError: Error in config file spltting of variable         
    
    Returns:
        output -- desired output for variable var
    """
    command = var['input_method']['command'].split("\n")
    mycursor = mydb.cursor()
    try:
        for com in command:
            mycursor.execute(com)
        result = mycursor.fetchall()
    except Exception as e:
        raise RuntimeError(var['name'] + " Error in data_base commands:" + var['input_method']['command']+"!Error: {}".format(e))

    if var['input_method']['start'] or var['input_method']['end'] :
        try:
            out = result[var["input_method"]['start']:var["input_method"]['end']]
        except Exception as e:
            raise RuntimeError("Error in SSH splitting of variable: "+var['name']+"!Error: {}".format(e))
    else :
        if len(result) == 1 :
            out = result[0]
            if len(out) == 1 :
                out = out[0]
        else :
            out = result
    return out

def _get_file(source,variables):
    """connect to file and get desired outputs for variables in source
    
    Arguments:
        source {dict} -- source to be connected to
        variables {dict} -- variables in config file
    
    Returns:
        dict -- result of variable inputs in source
    """
    mydb = _start_connection(source)
    result = {}
    for var in source['variables']:
        try: 
            result[var] = _get_variable_output(variables[var],mydb)
        except Exception as e:
            result[var] = e
    return result