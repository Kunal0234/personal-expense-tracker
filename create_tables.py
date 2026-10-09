from database import engine, Base
from models import Expense

Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")