#API module

import requests
import json
def _get_variable_output(var,response) :
    """obtain desired output from response obtained
    
    Arguments:
        var {dict} -- variable[var] in config file
        response {request} -- response from API request
    
    Raises:
        RuntimeError: response not obtained 
        RuntimeError: error in commands of variable in config file
        RuntimeError: error in splitting method defined in variable config file
    
    Returns:
        [type] -- [description]
    """
    if not response :
        raise RuntimeError("Invalid respose from API!Error: {}".format(response))
    try: 
        ldict = locals()
        exec("out = " + var['input_method']['command'],globals(),ldict)
        out = ldict['out']
    except Exception as e:
        raise RuntimeError(var['name'] + " Error in API commands:" + var['input_method']['command']+"!Error: {}".format(e))
    #have to make changes here
    try :
        if var['input_method']['start'] or var['input_method']['end'] :
            out = out[var["input_method"]['start']:var["input_method"]['end']]
    except Exception as e:
        raise RuntimeError("Error in API splitting of variable: "+var['name']+"!Error: {}".format(e))
    return out


def _get_file(source,variables):
    """connect too source and get response
    
    Arguments:
        source {dict} -- source to be connected to
        variables {dict} -- variables in config file
    
    Raises:
        NameError: request method not defined
        RuntimeError: unable to connect to source
    
    Returns:
        [dict] -- result of input variable 
    """
    result = {}
    try:
        if source['request'] == 'get':
            response = requests.get(source['url'], params = source['params'])
        elif source['request'] == 'post':
            response = requests.post(source['url'], params = source['params'],data = json.dumps(source['data']))
        else:
            raise NameError("request method not defined: "+ source['request'])
    except Exception as e:
        raise RuntimeError("API Source unable to connect!Error: {}".format(e))
    for var in source['variables']:
        try:
            result[var] = _get_variable_output(variables[var],response)
        except Exception as e:
            result[var] = e
    return result
        
    