from pydantic import BaseModel, ConfigDict

class EmployeeBase(BaseModel):
    full_name: str
    job_title: str
    country: str
    salary: float

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: int

    # New Pydantic V2 config style
    model_config = ConfigDict(from_attributes=True)

class SalaryResponse(BaseModel):
    gross_salary: float
    deduction: float
    net_salary: float


class CountryMetricResponse(BaseModel):
    country: str
    count: int
    min_salary: float
    max_salary: float
    avg_salary: float

class JobMetricResponse(BaseModel):
    job_title: str
    count: int
    avg_salary: float