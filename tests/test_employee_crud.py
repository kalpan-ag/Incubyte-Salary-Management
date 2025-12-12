from fastapi.testclient import TestClient
from app.main import app

def test_create_employee(client):
    payload = {
        "full_name": "Jane Doe",
        "job_title": "Software Engineer",
        "country": "India",
        "salary": 50000.0
    }
    
    response = client.post("/employees/", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Jane Doe"
    assert data["id"] is not None  # Ensure an ID was assigned
    assert data["country"] == "India"
    
def test_read_employee(client):
    # First create an employee
    payload = {
        "full_name": "John Read",
        "job_title": "Reader",
        "country": "USA",
        "salary": 60000.0
    }
    create_res = client.post("/employees/", json=payload)
    emp_id = create_res.json()["id"]

    # Now try to read it
    response = client.get(f"/employees/{emp_id}")
    assert response.status_code == 200
    assert response.json()["full_name"] == "John Read"

def test_update_employee(client):
    # Create
    payload = {"full_name": "Old Name", "job_title": "Dev", "country": "UK", "salary": 40000.0}
    create_res = client.post("/employees/", json=payload)
    emp_id = create_res.json()["id"]

    # Update
    update_payload = {"full_name": "New Name", "job_title": "Senior Dev", "country": "UK", "salary": 80000.0}
    response = client.put(f"/employees/{emp_id}", json=update_payload)
    
    assert response.status_code == 200
    assert response.json()["full_name"] == "New Name"
    assert response.json()["salary"] == 80000.0

def test_delete_employee(client):
    # Create
    payload = {"full_name": "To Delete", "job_title": "Temp", "country": "Canada", "salary": 30000.0}
    create_res = client.post("/employees/", json=payload)
    emp_id = create_res.json()["id"]

    # Delete
    response = client.delete(f"/employees/{emp_id}")
    assert response.status_code == 200

    # Verify it's gone
    get_response = client.get(f"/employees/{emp_id}")
    assert get_response.status_code == 404