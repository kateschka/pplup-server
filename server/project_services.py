from database import session
from models import User, Task, Subtask, Project, TaskStatus, UserRole


#returns project object, False if parsed successfully|True if error occurred and error message
def extract_project_data_from_json(json_msg, project):
    try:
        #if creating project, id field should still be present (could be blank)
        project.id = json_msg['data']['id'] 
        project.name = json_msg['data']['name']
        project.description = json_msg['data']['description']
        project.owner = int(json_msg['data']['owner'])
        return project, False, ""
    except KeyError:
        return project, True, 'Could not get project data from JSON'

def get_project_list(json_msg):
    err=[]
    result = []
    try:
        result = session.query(Project).all()
    except:
        err.append("Error reading from database") 
        return None, err
    return result, err

# get single project from db by id
def get_project(json_msg):
    err=[]
    project = Project()
    project, error, errormsg = extract_project_data_from_json(json_msg, project)
    if error:
        err.append(errormsg)
        return None, err
    try:
        project = session.query(Project).filter(Project.id == project.id).one()
    except:
        err.append("Error getting project from database") 
        return None, err
    return project, err

# get tasks related to a particular project (project info should be provided)
def get_project_tasks(json_msg):
    project, err = get_project(json_msg)
    if project is not None:
        try:
            tasks = session.query(Task).filter(Task.project == project.id).all()
        except:
            err.append("Error getting project tasks from database")
            return None, err 
    return tasks, err

#this is obvious
def create_project(json_msg):
    err=[]
    project = Project()
    project, error, errormsg = extract_project_data_from_json(json_msg, project)
    if error:
        err.append(errormsg)
        return None, err
    else:   
        try:
            session.add(project)
            session.commit()
            session.flush()
            #returning last added project
            project = session.query(Project).order_by(Project.id.desc()).first()
        except:
            err.append("Error adding to database")  
            return None, err 
    return project, err


def update_project(json_msg):
    err=[]
    #get project that we want to update
    project, error = get_project(json_msg)
    if project is not None:
        #if project is not none, this should get an updated project correctly
        updated_project, error, error_msg = extract_project_data_from_json(json_msg, updated_project)
        try:
            project.name = updated_project.name
            project.description = updated_project.description
            session.flush()
            result = session.query(Project).filter(Project.id == project.id).one()
        except:
            err.append("Error changing project data") 
            return None, err 
    else:
        err.extend(error)
        return None, err

    return result, err

def delete_project(json_msg):
    msg=[]
    err=[]
    project, error = get_project(json_msg)
    if project is not None:
        try:
            project = session.query(Project).filter(Project.id == project.id).one()
            session.delete(project)
            session.commit()
            session.flush()
            msg.append("Project was successfully deleted")
        except:
            err.append("Error deleting from db")
            return None, err
    else:
        err.extend(error)
        return None, err
    
    return msg, err
    