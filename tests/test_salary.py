from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_salary_calculation_india():
    # 1. Create an employee in India
    payload = {
        "full_name": "Rahul Dravid",
        "job_title": "Cricketer",
        "country": "India",
        "salary": 10000.0
    }
    create_res = client.post("/employees/", json=payload)
    emp_id = create_res.json()["id"]

    # 2. Get Salary Info
    response = client.get(f"/employees/{emp_id}/salary")
    
    assert response.status_code == 200
    data = response.json()
    
    # India = 10% deduction
    assert data["gross_salary"] == 10000.0
    assert data["deduction"] == 1000.0
    assert data["net_salary"] == 9000.0

def test_salary_calculation_usa():
    # 1. Create an employee in USA
    payload = {
        "full_name": "John Smith",
        "job_title": "Manager",
        "country": "United States",
        "salary": 10000.0
    }
    create_res = client.post("/employees/", json=payload)
    emp_id = create_res.json()["id"]

    # 2. Get Salary Info
    response = client.get(f"/employees/{emp_id}/salary")
    
    # US = 12% deduction
    assert response.json()["deduction"] == 1200.0
    assert response.json()["net_salary"] == 8800.0

def test_salary_calculation_other():
    # 1. Create an employee in Germany (Other)
    payload = {
        "full_name": "Hans Muller",
        "job_title": "Engineer",
        "country": "Germany",
        "salary": 10000.0
    }
    create_res = client.post("/employees/", json=payload)
    emp_id = create_res.json()["id"]

    # 2. Get Salary Info
    response = client.get(f"/employees/{emp_id}/salary")
    
    # Others = 0% deduction
    assert response.json()["deduction"] == 0.0
    assert response.json()["net_salary"] == 10000.0