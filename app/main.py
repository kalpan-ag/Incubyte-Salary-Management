from fastapi import FastAPI
from . import models, database, routes

# Create tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Incubyte Salary API",
    description="A TDD implementation of the Salary Management Kata",
    version="1.0.0"
)

app.include_router(routes.router)