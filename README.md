# Incubyte Salary Management Kata

A robust, production-ready REST API for managing employee salaries, built with **FastAPI** and **SQLAlchemy**. This project strictly follows **Test-Driven Development (TDD)** principles.

## 🚀 Features

* **Employee CRUD**: Full Create, Read, Update, Delete operations for employee records.
* **Salary Calculation**: Dynamic tax deduction logic based on country (India, US, others).
* **Salary Metrics**: Aggregated insights (Min, Max, Avg) by Country and Job Title.
* **Production Ready**: Uses Pydantic V2 for validation and SQLAlchemy 2.0 for database interactions.

## 🛠️ Tech Stack

* **Language**: Python 3.10+
* **Framework**: FastAPI
* **Database**: SQLite (SQLAlchemy ORM)
* **Testing**: Pytest + HTTPX (Async/Sync testing)

## 🏃‍♂️ How to Run

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/incubyte-hiring/incubyte-sm-kata-kalpan-ag
    cd incubyte-salary-kata
    ```

2.  **Set up the environment:**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    uvicorn app.main:app --reload
    ```
    *Access Swagger Documentation at: `http://127.0.0.1:8000/docs`*

5.  **Run Tests (TDD Verification):**
    ```bash
    python -m pytest
    ```

## 🤖 AI Implementation Details

In accordance with the assessment guidelines, I utilized AI (Gemini) to accelerate development while maintaining strict control over logic and code quality.

| Stage | Task | AI Usage & Rationale |
| :--- | :--- | :--- |
| **Setup** | Project Structure | **Prompt:** "Setup a Python FastAPI project structure and write a failing test for creating an Employee."<br>**Rationale:** Rapidly scaffolded boilerplate (files, imports) to jump straight into the TDD "Red" phase without manual setup overhead. |
| **Refactor** | Dependency Updates | **Prompt:** "Update this code to fix Pydantic V2 and SQLAlchemy 2.0 deprecation warnings."<br>**Rationale:** AI quickly identified and modernized syntax (e.g., `model_dump()` vs `dict()`), ensuring the code is future-proof and production-ready. |
| **Logic** | Salary Rules | **Prompt:** "Implement a salary calculation endpoint with these specific tax rules for India/USA."<br>**Rationale:** Used AI to generate the `if/else` business logic block, which I then verified against the requirements via the pre-written tests. |
| **Metrics** | SQL Aggregations | **Prompt:** "Write SQLAlchemy queries to find min, max, and avg salary grouped by country."<br>**Rationale:** AI is excellent at constructing complex SQL/ORM queries (`func.avg`, `func.count`), saving time on looking up syntax documentation. |