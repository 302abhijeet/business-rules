#SSH module
import paramiko

def _start_connection(source) :
    """connect to source
    
    Arguments:
        source {dict} -- source to be connected to 
    
    Returns:
        [paramiko] -- ssh object connected
    """
    ssh_client=paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname = source['host_name'],username=source['user_name'],password=source['password'],key_filename = source['key_filename'])
    return ssh_client

def _get_variable_output(var,ssh_client) :
    """get desired variable output from response
    
    Arguments:
        var {dict} -- variable[var] in config file
        ssh_client {paramiko} -- ssh object connected to source
    
    Raises:
        RuntimeError: error obtained in response from source
        RuntimeError: error in splitting method defined in config
    
    Returns:
        result -- output from the response desired
    """
    stdin,stdout,stderr=ssh_client.exec_command(var["input_method"]['command'])
    if stderr.readlines() :
        ex = stderr.readlines()
        raise RuntimeError(ex)
    if var['input_method']['start'] or var['input_method']['end'] :
        try:
            out = stdout.readlines()[0]
            if type(var['input_method']['start']) == type(int()) :
                out = out[var['input_method']['start']:var['input_method']['end']]
            else :
                out = out[out.index(var["input_method"]['start']) +1:out.index(var["input_method"]['end'])]
        except Exception as e:
            raise RuntimeError(var['name'] + " Error in SSH splitting of variable: {}".format(e))
    else :
        out = stdout.readlines()[0]
    return out


def _get_file(source, variables):
    """get all input variables from source
    
    Arguments:
        source {dict} -- source to be connected to
        variables {dict} -- variables in config file
    
    Raises:
        RuntimeError: couldn't connect to host
    
    Returns:
        {dict} -- result of all input variables in source
    """
    try:
        ssh_client = _start_connection(source)
    except Exception as e:
        raise RuntimeError("Couldn't connect to SSH host!Error: {}".format(e))
    result = {}
    for var in source['variables']:
        try:
            result[var] = _get_variable_output(variables[var],ssh_client)
        except Exception as e:
            result[var] = e
    return result
        
        