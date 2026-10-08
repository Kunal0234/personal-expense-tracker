from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
app = FastAPI()

expenses = []

class Student(BaseModel):
    name: str
    age:int
    course:str

class ExpenseSchema(BaseModel):
    title:str
    amount: float = Field(gt=0)
    category:str
    date: str
    description:str


@app.get("/")
def home():
    return{"message":"Hello world"}

@app.post("/students")
def create_student(student: Student):
    return student

@app.post("/expenses")
def create_expense(expense: ExpenseSchema):
    expenses.append(expense)
    return expense

@app.get("/expenses")
def get_expenses():
    return expenses


@app.get("/expenses/{expense_id}")
def show_expense(expense_id: int):
    if expense_id < 0 or expense_id >= len(expenses):
        raise HTTPException(status_code=404, detail="Expense not found")

    return expenses[expense_id]