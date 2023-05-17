from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

class TaskStatus(Base):
    __tablename__ = 'task_statuses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(200), nullable=False)
    Task = relationship('Task')

    def __init__(self, description: str):
        self.description = description

    def __repr__(self):
        return self.name

    def __str__(self):
        return str(self.name)

    def __int__(self):
        return self.id

class UserRole(Base):
    __tablename__ = 'user_roles'

    id = Column(Integer, primary_key=True,  autoincrement=True)
    description = Column(String(200), nullable=False)
    User = relationship('User')

    def __init__(self, description: str):
        self.description = description

    def __repr__(self):
        return self.name

    def __str__(self):
        return str(self.name)

    def __int__(self):
        return self.id

user_has_tasks = Table(
    "user_has_tasks",
    Base.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("task_id", ForeignKey("tasks.id")),
)

user_has_subtasks = Table(
    "user_has_subtasks",
    Base.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("subtask_id", ForeignKey("subtasks.id")),
)

user_has_projects = Table(
    "user_has_projects",
    Base.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("project_id", ForeignKey("projects.id")),
)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    role = Column(Integer, ForeignKey('user_roles.id'))
    login = Column(String(200), nullable=False)
    password = Column(String(200), nullable=False)
    name = Column(String(200), nullable=True)
    surname = Column(String(200), nullable=True)
    tasks = relationship('Task',
                         secondary=user_has_tasks, back_populates="users",
                         cascade='all, delete')
    subtasks = relationship('Subtask',
                         secondary=user_has_subtasks, back_populates="users",
                         cascade='all, delete')
    projects = relationship('Project',
                            secondary=user_has_projects,back_populates="users",
                            cascade='all, delete')

    def __repr__(self):
        return self.name

    def __int__(self):
        return self.id

    def __str__(self):
        return str(self.name)
    

class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    description = Column(String, nullable=True)
    owner = Column(Integer, ForeignKey(User.id))
    tasks = relationship('Task', backref='projects', cascade='all, delete-orphan')
    users = relationship('User', secondary=user_has_projects, back_populates="projects")

    def __repr__(self):
        return self.name

    def __init__(self, name, owner, description=''):
        self.name = name
        self.description = description
        self.owner = owner

    def __int__(self):
        return self.id


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(Integer, ForeignKey(TaskStatus.id))
    name = Column(String(200), nullable=False)
    description = Column(String, nullable=True)
    assigned_to = Column(Integer, ForeignKey(User.id))
    project = Column(Integer, ForeignKey(Project.id))
    subtasks = relationship('Subtask', cascade='all, delete-orphan')
    documentation = relationship('Documentation', cascade='all, delete-orphan')
    users = relationship('User', secondary=user_has_tasks, back_populates="tasks", cascade='all, delete')

    def __repr__(self):
        return self.name

    def __init__(self, status, name, assigned_to, project, description=""):
        self.status = status
        self.name = name
        self.assigned_to = assigned_to
        self.description = description
        self.project = project

    def __int__(self):
        return self.id
    
class Subtask(Base):
    __tablename__ = 'subtasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(Integer, ForeignKey(TaskStatus.id))
    name = Column(String(200), nullable=False)
    description = Column(String, nullable=True)
    assigned_to = Column(Integer, ForeignKey(User.id))
    task = Column(Integer, ForeignKey(Task.id))
    users = relationship('User', secondary=user_has_subtasks, back_populates='subtasks', cascade='all, delete')

    def __repr__(self):
        return self.name

    def __init__(self, status, name, assigned_to, task, description=""):
        self.status = status
        self.name = name
        self.assigned_to = assigned_to
        self.description = description
        self.task = task

    def __int__(self):
        return self.id
    

class Documentation(Base):
    __tablename__ = 'documentation'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    path = Column(String(1024), nullable=False)
    task = Column(Integer, ForeignKey(Task.id))

    def __init__(self, name: str, path: str, task: int):
        self.name = name
        self.path = path
        self.task = task

    def __int__(self):
        return self.id
    
    def __repr__(self):
        return self.name
    



    
    


