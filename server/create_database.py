from database import create_db, session
from models import User, Task, Subtask, Project, UserRole, TaskStatus




def create_database(load_fake_data: bool = False):
    create_db()
    if load_fake_data:
        _load_fake_data(session)


def _load_fake_data(session):

    task_status1 = TaskStatus(description="Завершено")
    task_status2 = TaskStatus(description="Не начато")
    task_status3 = TaskStatus(description="В процессе")
    session.add(task_status1)
    session.add(task_status2)
    session.add(task_status3)
    session.commit()

    user_role1 = UserRole(description="admin")
    user_role2 = UserRole(description="user")
    session.add(user_role1)
    session.add(user_role2)
    session.commit()
    session.flush()

    user1 = User(int(user_role1), "login", "pass", "John", "Doe")
    user2 = User(int(user_role2), "login11", "pass11", "Jane", "Doe")
    user3 = User(int(user_role1), "login22", "pass22", "Иванов", "Иван")
    session.add(user1)
    session.add(user2)
    session.add(user3)
    session.commit()
    session.flush()

    project1 = Project("awesome project", int(user1), "so awesome")
    project2 = Project("ППЛУП", int(user2))
    project3 = Project("ПАРНИTRTYRTYRТ", int(user1), "делаем крутой проект")
    session.add(project1)
    session.add(project2)
    session.add(project3)
    session.commit()
    session.flush()

    task1 = Task(int(task_status1), "Сделать что-то",
                 int(user1), int(project1), "очень срочно")
    task2 = Task(int(task_status2), "Сделать что-то еще",
                 int(user2), int(project1), "не очень срочно")
    task3 = Task(int(task_status3), "Сделать срочно",
                 int(user2), int(project3), "")
    task4 = Task(int(task_status1), "Написать что-то",
                 int(user3), int(project2), "без чатгпт")
    task5 = Task(int(task_status2), "Уточнить про что-то",
                 int(user1), int(project2), "у директора")
    task6 = Task(int(task_status1), "Купить кофи",
                 int(user2), int(project1), "вкусный")
    session.add(task1)
    session.add(task2)
    session.add(task3)
    session.add(task4)
    session.add(task5)
    session.add(task6)

    session.commit()
    session.flush()
    session.close()
