from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from database import SessionLocal
from models import Expense as ExpenseModel

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
    db = SessionLocal()

    try:
        db_expense = ExpenseModel(
            title=expense.title,
            amount=expense.amount,
            category=expense.category,
            date=expense.date,
            description=expense.description
        )

        db.add(db_expense)
        db.commit()
        db.refresh(db_expense)

        return {
            "id": db_expense.id,
            "title": db_expense.title,
            "amount": db_expense.amount,
            "category": db_expense.category,
            "date": db_expense.date,
            "description": db_expense.description
        }
    finally:
        db.close()

@app.get("/expenses")
def get_expenses():
    db = SessionLocal()

    try:
        expenses = db.query(ExpenseModel).all()
        return expenses
    finally:
        db.close()


@app.get("/expenses/{expense_id}")
def show_expense(expense_id: int):
    db = SessionLocal()

    try:
        expense = db.query(ExpenseModel).filter(
            ExpenseModel.id == expense_id
        ).first()

        if expense is None:
            raise HTTPException(
                status_code=404,
                detail="Expense not found"
            )

        return expense
    finally:
        db.close()

@app.put("/expenses/{expense_id}")
def update_expense(expense_id: int, updated_expense: ExpenseSchema):
    db = SessionLocal()

    try:
        expense = db.query(ExpenseModel).filter(
            ExpenseModel.id == expense_id
        ).first()

        if expense is None:
            raise HTTPException(
                status_code=404,
                detail="Expense not found"
            )

        expense.title = updated_expense.title
        expense.amount = updated_expense.amount
        expense.category = updated_expense.category
        expense.date = updated_expense.date
        expense.description = updated_expense.description

        db.commit()
        db.refresh(expense)

        return expense
    finally:
        db.close()

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):
    db = SessionLocal()

    try:
        expense = db.query(ExpenseModel).filter(
            ExpenseModel.id == expense_id
        ).first()

        if expense is None:
            raise HTTPException(
                status_code=404,
                detail="Expense not found"
            )

        db.delete(expense)
        db.commit()

        return {"message": "Expense deleted successfully"}
    finally:
        db.close()