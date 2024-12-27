from database.db_setup import Task, session

def add_task(title, description, priority, due_date):
    new_task = Task(title=title, description=description, priority=priority, due_date=due_date)
    session.add(new_task)
    session.commit()
    return new_task

def get_all_tasks():
    return session.query(Task).all()

def update_task(task_id, title=None, description=None, priority=None, due_date=None):
    task = session.query(Task).get(task_id)
    if task:
        if title:
            task.title = title
        if description:
            task.description = description
        if priority:
            task.priority = priority
        if due_date:
            task.due_date = due_date
        session.commit()
        return task
    return None

def delete_task(task_id):
    task = session.query(Task).get(task_id)
    if task:
        session.delete(task)
        session.commit()
        return True
    return False
