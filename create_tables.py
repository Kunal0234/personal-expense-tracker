from database import engine, Base
from models import Expense,Budget

Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")