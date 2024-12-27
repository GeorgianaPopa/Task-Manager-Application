from database.db_setup import session, Task
import csv
from datetime import datetime

# Functia cu ajutorul careia adaugam sarcini 
def add_task(title, description, priority, due_date):
    try:
        new_task = Task(
            title=title,
            description=description,
            priority=priority,
            due_date=datetime.strptime(due_date, '%Y-%m-%d').date()
        )
        session.add(new_task)
        session.commit()
        print(f"Sarcina '{title}' a fost adăugată cu succes!")
    except Exception as e:
        session.rollback()
        print(f"Eroare la adăugarea sarcinii: {e}")

# Functia cu ajutorul careia vizualizam sarcini
def view_tasks():
    tasks = session.query(Task).all()
    if not tasks:
        print("Nu există sarcini disponibile.")
    else:
        for task in tasks:
            print(f"[ID: {task.id}] Titlu: {task.title}, Prioritate: {task.priority}, Termen: {task.due_date}")

# Functia cu ajutorul careia stergem sarcini
def delete_task(task_id):
    try:
        task = session.query(Task).filter_by(id=task_id).first()
        if task:
            session.delete(task)
            session.commit()
            print(f"Sarcina cu ID {task_id} a fost ștearsă.")
        else:
            print(f"Nicio sarcină găsită cu ID {task_id}.")
    except Exception as e:
        session.rollback()
        print(f"Eroare la ștergerea sarcinii: {e}")

# Functia cu ajutorul exportam sarcini in format CSV
def export_tasks_to_csv(file_name="tasks.csv"):
    tasks = session.query(Task).all()
    if not tasks:
        print("Nu există sarcini de exportat.")
        return
    try:
        with open(file_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Titlu", "Descriere", "Prioritate", "Termen"])
            for task in tasks:
                writer.writerow([task.id, task.title, task.description, task.priority, task.due_date])
        print(f"Sarcinile au fost exportate în fișierul {file_name}.")
    except Exception as e:
        print(f"Eroare la exportul sarcinilor: {e}")
        

if __name__ == "__main__":
    print("Bine ai venit în aplicația Task Manager!")
    print("Folosește funcțiile definite pentru a gestiona sarcinile.")
