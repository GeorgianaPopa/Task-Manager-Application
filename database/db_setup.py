from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import UniqueConstraint

# Clasa de baza pentru modelele Object-Relational Mapping
Base = declarative_base()

# Bazea de date SQLite
engine = create_engine('sqlite:///tasks.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# Tabela "tasks"
class Task(Base):
    __tablename__ = 'tasks'
    __table_args__ = (UniqueConstraint('title', 'due_date', name='_title_due_date_uc'),)
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    priority = Column(String, nullable=True)  # Exemplu: "High", "Medium", "Low"
    due_date = Column(Date, nullable=True)  # Format: YYYY-MM-DD

# Tabela in baza de date
def setup_database():
    Base.metadata.create_all(engine)
    print("Baza de date și tabela 'tasks' au fost create cu succes!")

if __name__ == '__main__':
    setup_database()
