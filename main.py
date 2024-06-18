from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import csv

app = FastAPI()

DATABASE_URL = "sqlite:///./rpn_calculator.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Operation(Base):
    __tablename__ = "operations"
    id = Column(Integer, primary_key=True, index=True)
    expression = Column(String, index=True)
    result = Column(Float)

Base.metadata.create_all(bind=engine)

class RPNExpression(BaseModel):
    expression: str = Field(...)

def evaluate_rpn(expression: str) -> float:
    stack = []
    operators = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x / y,
    }
    
    for token in expression.split():
        if token in operators:
            y, x = stack.pop(), stack.pop()
            result = operators[token](x, y)
            stack.append(result)
        else:
            stack.append(float(token))
    
    return stack[0] if stack else None

@app.post("/calculate/")
def calculate(expression: RPNExpression):
    try:
        result = evaluate_rpn(expression.expression)
        with SessionLocal() as db:
            operation = Operation(expression=expression.expression, result=result)
            db.add(operation)
            db.commit()
            db.refresh(operation)
        return {"expression": expression.expression, "result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/export/")
def export_data():
    with SessionLocal() as db:
        operations = db.query(Operation).all()
    
    filename = "operations.csv"
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Expression", "Result"])
        for op in operations:
            writer.writerow([op.id, op.expression, op.result])
    
    return {"message": f"Data exported to {filename}"}
