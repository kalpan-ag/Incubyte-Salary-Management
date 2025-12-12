from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas, database

router = APIRouter()

# --- CRUD Operations ---

@router.post("/employees/", response_model=schemas.Employee, tags=["Employees"])
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(database.get_db)):
    """
    Create a new employee record.
    
    Args:
        employee: The employee data (name, title, country, salary).
    
    Returns:
        The created employee object with assigned ID.
    """
    db_employee = models.Employee(**employee.model_dump())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@router.get("/employees/{employee_id}", response_model=schemas.Employee, tags=["Employees"])
def read_employee(employee_id: int, db: Session = Depends(database.get_db)):
    """Retrieve details of a specific employee by ID."""
    db_employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee

@router.put("/employees/{employee_id}", response_model=schemas.Employee, tags=["Employees"])
def update_employee(employee_id: int, employee: schemas.EmployeeCreate, db: Session = Depends(database.get_db)):
    """Update an existing employee's details."""
    db_employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    for key, value in employee.model_dump().items():
        setattr(db_employee, key, value)
    
    db.commit()
    db.refresh(db_employee)
    return db_employee

@router.delete("/employees/{employee_id}", tags=["Employees"])
def delete_employee(employee_id: int, db: Session = Depends(database.get_db)):
    """Delete an employee record permanently."""
    db_employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    db.delete(db_employee)
    db.commit()
    return {"detail": "Employee deleted"}

# --- Business Logic ---

@router.get("/employees/{employee_id}/salary", response_model=schemas.SalaryResponse, tags=["Salary"])
def calculate_salary(employee_id: int, db: Session = Depends(database.get_db)):
    """
    Calculate gross, deduction, and net salary based on country tax rules.
    
    Rules:
    - India: 10% deduction
    - USA: 12% deduction
    - Others: 0% deduction
    """
    db_employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    gross = db_employee.salary
    country = db_employee.country.lower()
    
    deduction = 0.0
    if country == "india":
        deduction = gross * 0.10
    elif country == "united states":
        deduction = gross * 0.12
    
    return {
        "gross_salary": gross,
        "deduction": deduction,
        "net_salary": gross - deduction
    }

# --- Metrics ---

@router.get("/metrics/country", response_model=schemas.CountryMetricResponse, tags=["Metrics"])
def get_country_metrics(country: str, db: Session = Depends(database.get_db)):
    """Get salary statistics (min, max, avg, count) for a specific country."""
    stats = db.query(
        func.count(models.Employee.id),
        func.min(models.Employee.salary),
        func.max(models.Employee.salary),
        func.avg(models.Employee.salary)
    ).filter(func.lower(models.Employee.country) == country.lower()).first()
    
    if stats[0] == 0:
        raise HTTPException(status_code=404, detail="No data found for this country")
        
    return {
        "country": country,
        "count": stats[0],
        "min_salary": stats[1],
        "max_salary": stats[2],
        "avg_salary": stats[3]
    }

@router.get("/metrics/job_title", response_model=schemas.JobMetricResponse, tags=["Metrics"])
def get_job_metrics(job_title: str, db: Session = Depends(database.get_db)):
    """Get average salary and count for a specific job title."""
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