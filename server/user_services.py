from database import session
from models import User, Project


def extract_user_data_from_json(json_msg, user):
    try:
        user.login = json_msg['data']['login']
        user.password = json_msg['data']['password']
        return user, False, ""
    except KeyError:
        return user, True, 'provided information was incorrect'

def authenticate(json_msg):
    user = User()
    err = []
    #get user data from json
    user, error, errormsg = extract_user_data_from_json(json_msg, user)
    if error:
        err.append(errormsg)
        return None, err
    else:
        try:
            #trying get user from database
            user = session.query(User).filter(User.login == user.login,
                                      User.password == user.password).one()
        except:
            err.append("user not found")
            return None, err
        
    return user, err


# ы фор сесюрити    
def get_user(json_msg):
    try:
        user_id = json_msg['data']['id']
        user = session.query(User).filter(User.id == user_id).one()
        return user, ""
    except KeyError:
        return None, 'provided information was incorrect'


def get_user_projects(json_msg):
    err=[]
    projects = []
    user, error_msg = get_user(json_msg)
    if user is not None:
        try:
            projects = session.query(Project).filter(Project.users.any(User.id == user.id)).all()
        except:
            err.append("Error getting user projects from database")
            return None, err 
    else:
        err.append(error_msg)
    return projects, err