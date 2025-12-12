from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    job_title = Column(String)
    country = Column(String)
    salary = Column(Float)