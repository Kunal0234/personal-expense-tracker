from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from database import SessionLocal
from models import Expense as ExpenseModel
from models import Budget as BudgetModel
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

class BudgetSchema(BaseModel):
    month :str
    amount : float = Field(gt=0)
    

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


@app.post("/budgets")
def create_budget(budget: BudgetSchema):
    db = SessionLocal()

    try:
        existing_budget = db.query(BudgetModel).filter(
            BudgetModel.month == budget.month
        ).first()

        if existing_budget:
            raise HTTPException(
                status_code=409,
                detail="Budget already exists for this month"
            )

        new_budget = BudgetModel(
            month=budget.month,
            amount=budget.amount
        )

        db.add(new_budget)
        db.commit()
        db.refresh(new_budget)

        return {
            "message": "Budget created successfully",
            "id": new_budget.id,
            "month": new_budget.month,
            "amount": new_budget.amount
        }

    finally:
        db.close()

@app.get("/expenses")
def get_expenses(
    category: str = None,
    sort_by: str = "date",
    order: str = "asc",
    skip: int = 0,
    limit: int = 10
):
    db = SessionLocal()

    try:
        query = db.query(ExpenseModel)

        # Category filtering
        if category:
            query = query.filter(
                ExpenseModel.category == category
            )

        # Sorting
        if sort_by == "amount":
            sort_column = ExpenseModel.amount
        else:
            sort_column = ExpenseModel.date

        if order == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())

        # Pagination
        expenses = query.offset(skip).limit(limit).all()

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

@app.get("/budgets")
def get_budgets():
    db = SessionLocal()

    try:
        budgets = db.query(BudgetModel).all()
        return budgets
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