from sqlalchemy.orm import Session
from . import models, schemas, database
from fastapi import FastAPI, Depends, HTTPException # Add HTTPException
from sqlalchemy import func # Import func

# Create tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/employees/", response_model=schemas.Employee)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    # usage of model_dump() instead of dict()
    db_employee = models.Employee(**employee.model_dump())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee



# ... (Previous code remains)

@app.get("/employees/{employee_id}", response_model=schemas.Employee)
def read_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee

@app.put("/employees/{employee_id}", response_model=schemas.Employee)
def update_employee(employee_id: int, employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Update fields
    for key, value in employee.model_dump().items():
        setattr(db_employee, key, value)
    
    db.commit()
    db.refresh(db_employee)
    return db_employee

@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    db.delete(db_employee)
    db.commit()
    return {"detail": "Employee deleted"}

# Add this endpoint to app/main.py

@app.get("/employees/{employee_id}/salary", response_model=schemas.SalaryResponse)
def calculate_salary(employee_id: int, db: Session = Depends(get_db)):
    db_employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    gross = db_employee.salary
    country = db_employee.country.lower() # Normalize case for easier comparison
    
    deduction = 0.0
    
    if country == "india":
        deduction = gross * 0.10
    elif country == "united states":
        deduction = gross * 0.12
    # else: deduction remains 0.0
    
    net = gross - deduction
    
    return {
        "gross_salary": gross,
        "deduction": deduction,
        "net_salary": net
    }


# ... (Previous imports)

@app.get("/metrics/country", response_model=schemas.CountryMetricResponse)
def get_country_metrics(country: str, db: Session = Depends(get_db)):
    # Filter by country (case insensitive)
    stats = db.query(
        func.count(models.Employee.id),
        func.min(models.Employee.salary),
        func.max(models.Employee.salary),
        func.avg(models.Employee.salary)
    ).filter(func.lower(models.Employee.country) == country.lower()).first()
    
    # stats is a tuple: (count, min, max, avg)
    if stats[0] == 0:
        raise HTTPException(status_code=404, detail="No data found for this country")
        
    return {
        "country": country,
        "count": stats[0],
        "min_salary": stats[1],
        "max_salary": stats[2],
        "avg_salary": stats[3]
    }

@app.get("/metrics/job_title", response_model=schemas.JobMetricResponse)
def get_job_metrics(job_title: str, db: Session = Depends(get_db)):
    # Filter by job title (case insensitive)
    stats = db.query(
        func.count(models.Employee.id),
        func.avg(models.Employee.salary)
    ).filter(func.lower(models.Employee.job_title) == job_title.lower()).first()
    
    if stats[0] == 0:
        raise HTTPException(status_code=404, detail="No data found for this job title")
        
    return {
        "job_title": job_title,
        "count": stats[0],
        "avg_salary": stats[1]
    }