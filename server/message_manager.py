import json
from project_services import *
from user_services import *
from database import AlchemyEncoder

# all commands take json_msg as an argument and return an object, object list or None and a list of errors

server_commands = {
    #user_services (all methods that require user info)
    'auth': authenticate,
    'user_projects': get_user_projects,
    #'user_tasks': get_user_tasks,

    #project_services (all methods that require project info)
    'projects': get_project_list,
    'project': get_project,
    'tasks': get_project_tasks,
    'create_project': create_project,
    'delete_project': delete_project, 
    'update_project': update_project,

    #task_services (all methods that require task info)
    #'task_subtasks' : get_task_subtasks,
    #'update_task': update_task,
    #'delete_task' : delete_task,
    #'task': get_task,

    # subtask_services (all methods that require subtask info)
    #'subtask' : get_subtask,
    #'update_subtask': update_subtask,
    #'delete_subtask' : delete_subtask,

}


def generate_reply(msg):
    #get data and errorlist
    data, err = process_message(msg)
    result = []
    #set status to success, ignore errors
    if data is not None:        
        result.append({"status":"success"})
        result.append({"data": data})
    #set status to error, append list of errors
    else:
        result.append({"status":"error"})
        result.append({"errorlist":err})
    #convert to json
    json_result = json.dumps(result, cls=AlchemyEncoder, ensure_ascii=False, skipkeys=True)
    return json_result


def process_message(msg):
    err=[]
    #trying to parse message to json and get command
    try:
        json_msg = json.loads(msg)
        command = json_msg['command']
        #if command is unknown
        if command not in server_commands:
            err.append("Wrong command")
            return None, err
        
    #if we couldn't parse json or no command field
    except:
        err.append("Wrong message format")
        return None, err      
    
    return server_commands.get(command)(json_msg)
