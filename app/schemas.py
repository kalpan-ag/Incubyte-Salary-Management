from pydantic import BaseModel, ConfigDict, Field

class EmployeeBase(BaseModel):
    full_name: str = Field(..., min_length=1, json_schema_extra={"example": "Jane Doe"})
    job_title: str = Field(..., min_length=1, json_schema_extra={"example": "Software Engineer"})
    country: str = Field(..., min_length=1, json_schema_extra={"example": "India"})
    salary: float = Field(..., gt=0, json_schema_extra={"example": 50000.0})

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: int
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