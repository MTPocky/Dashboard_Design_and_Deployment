from fastapi import FastAPI
from app.db import fetch_one, fetch_all, table_name


app = FastAPI(
    title="Salary KPI API",
    description="API to access salary dataset KPIs",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Salary KPI API is running",
        "docs": "/docs"
    }


@app.get("/kpis/average-salary")
def average_salary():
    query = f"""
    SELECT ROUND(AVG(salary)::numeric, 2) AS average_salary
    FROM {table_name()};
    """
    return fetch_one(query)


@app.get("/kpis/maximum-salary")
def maximum_salary():
    query = f"""
    SELECT MAX(salary) AS maximum_salary
    FROM {table_name()};
    """
    return fetch_one(query)


@app.get("/kpis/minimum-salary")
def minimum_salary():
    query = f"""
    SELECT MIN(salary) AS minimum_salary
    FROM {table_name()};
    """
    return fetch_one(query)


@app.get("/kpis/total-job-count")
def total_job_count():
    query = f"""
    SELECT COUNT(*) AS total_job_count
    FROM {table_name()};
    """
    return fetch_one(query)


@app.get("/kpis/average-salary-by-experience")
def average_salary_by_experience():
    query = f"""
    SELECT 
        experience_years,
        ROUND(AVG(salary)::numeric, 2) AS average_salary
    FROM {table_name()}
    GROUP BY experience_years
    ORDER BY experience_years;
    """
    return fetch_all(query)


@app.get("/kpis/average-salary-by-education")
def average_salary_by_education():
    query = f"""
    SELECT 
        education_level,
        ROUND(AVG(salary)::numeric, 2) AS average_salary
    FROM {table_name()}
    GROUP BY education_level
    ORDER BY average_salary DESC;
    """
    return fetch_all(query)


@app.get("/kpis/average-salary-by-company-size")
def average_salary_by_company_size():
    query = f"""
    SELECT 
        company_size,
        ROUND(AVG(salary)::numeric, 2) AS average_salary
    FROM {table_name()}
    GROUP BY company_size
    ORDER BY average_salary DESC;
    """
    return fetch_all(query)


@app.get("/kpis/average-salary-by-industry")
def average_salary_by_industry():
    query = f"""
    SELECT 
        industry,
        ROUND(AVG(salary)::numeric, 2) AS average_salary
    FROM {table_name()}
    GROUP BY industry
    ORDER BY average_salary DESC;
    """
    return fetch_all(query)


@app.get("/kpis/average-salary-by-certifications")
def average_salary_by_certifications():
    query = f"""
    SELECT 
        certifications,
        ROUND(AVG(salary)::numeric, 2) AS average_salary
    FROM {table_name()}
    GROUP BY certifications
    ORDER BY certifications;
    """
    return fetch_all(query)


@app.get("/kpis/average-salary-by-remote-work")
def average_salary_by_remote_work():
    query = f"""
    SELECT 
        remote_work,
        ROUND(AVG(salary)::numeric, 2) AS average_salary
    FROM {table_name()}
    GROUP BY remote_work
    ORDER BY remote_work;
    """
    return fetch_all(query)


@app.get("/kpis/average-salary-by-skills-count")
def average_salary_by_skills_count():
    query = f"""
    SELECT 
        skills_count,
        ROUND(AVG(salary)::numeric, 2) AS average_salary
    FROM {table_name()}
    GROUP BY skills_count
    ORDER BY skills_count;
    """
    return fetch_all(query)