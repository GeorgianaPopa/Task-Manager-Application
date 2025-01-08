from database.db_setup import session, Task
import csv
from datetime import datetime
import os

def validate_task(title, due_date):
    if not title or not title.strip():
        raise ValueError("🚨 Titlul este obligatoriu! 🚨")
    if not due_date:
        raise ValueError("🚨 Data limita este obligatorie! 🚨")

# Functia cu ajutorul careia adaugam sarcini 
def add_task(title, description, priority, due_date):
    try:
        validate_task(title, due_date) 
        existing_task = session.query(Task).filter_by(title=title, due_date=due_date).first()
        if existing_task:
            print(f"⚠️ Sarcina '{title}' cu termen {due_date} a fost deja adaugata! ⚠️")
            return

        new_task = Task(title=title, description=description, priority=priority, due_date=due_date)
        session.add(new_task)
        session.commit()
        print(f"✅ Sarcina '{title}' a fost adaugata cu succes!")
    except ValueError as ve:
        print(ve)
    except Exception as e:
        session.rollback()
        print(f"🚨 Eroare la adaugarea sarcinii: {e}")


# Functia cu ajutorul careia vizualizam sarcinile
def view_tasks():
    tasks = session.query(Task).all()
    if not tasks:
        print("Nu exista sarcini disponibile.❌")
    else:
        for task in tasks:
            print(f"[ID: {task.id}] Titlu: {task.title}, Prioritate: {task.priority}, Termen: {task.due_date}")

# Functia cu ajutorul careia stergem sarcinile
def delete_task(task_id):
    task = session.query(Task).filter_by(id=task_id).first()
    if not task:
        existing_ids = [task.id for task in session.query(Task).all()]
        print(f"⚠️ Nicio sarcina gasita cu ID {task_id}. ID-uri existente: {existing_ids}")
        return
    try:
        session.delete(task)
        session.commit()
        print(f"✅ Sarcina cu ID {task_id} a fost stearsa!")
    except Exception as e:
        session.rollback()
        print(f"🚨 Eroare la stergerea sarcinii: {e}")


# Functia cu ajutorul exportam sarcinile in format CSV
def export_tasks_to_csv(file_path='tasks.csv'):
    try:
        dir_name = os.path.dirname(file_path)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name)

        tasks = session.query(Task).all()
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'title', 'description', 'priority', 'due_date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for task in tasks:
                writer.writerow({
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'priority': task.priority,
                    'due_date': task.due_date
                })
        print(f"Sarcinile au fost exportate in fisierul {file_path}.")
    except FileNotFoundError as e:
        print(f"🚨 Calea specificata este invalida: {file_path}. Detalii: {e}")
    except Exception as e:
        print(f"🚨 Eroare neasteptata la export: {e}")

        

if __name__ == "__main__":
    print("=== TESTAREA TASK MANAGER ===")

    # Sarcini adaugate
    print("\n=== Test:Adaugam sarcini... ===")
    add_task("Proiect facultate", "Finalizez proiectul Task Manager", "High", "2024-12-30")
    add_task("Cumparaturi", "Cumparaturi pentru sarbatori", "Medium", "2024-12-28")

    # Sarcini duplicate
    print("\n=== Test: Adaug o sarcina duplicata ===")
    add_task("Cumparaturi", "Cumparaturi pentru sarbatori", "Medium", "2024-12-28")
    
     # Vizualizez sarcinile
    print("\n=== Test: Vizualizarea sarcinilor ===")
    view_tasks()

    print("\n=== Export sarcinile in CSV... ===")
    export_tasks_to_csv("tasks.csv")
    export_tasks_to_csv("/invalid_path/tasks.csv")

    # Sarcini sterse
    print("\n=== Test: Sterg sarcina... ===")
    delete_task(2)
    delete_task(14)

    # Vizualizarea sarcinilor ramase
    print("\n=== Test: Sarcinile ramase: ===")
    view_tasks()
    
    print("\nExportam din nou sarcinile ramase in CSV...")
    export_tasks_to_csv("tasks_remaining.csv")
    
    # Eroare la adaugarea unei sarcini fara campuri obligatorii
    print("\n=== Test: Sarcina fara campuri obligatorii ===")
    try:
        add_task("", "Sarcina fara titlu", "High", "2024-12-30")  
    except Exception as e:
        print(f"🚨 Eroare: {e} 🚨")

    # Eroare la export
    print("\n=== Test: Exportul sarcinilor cu eroare ===")
    try:
        export_tasks_to_csv("/invalid_path/tasks.csv")  
    except Exception as e:
        print(f"🚨 Eroare: {e} 🚨")
