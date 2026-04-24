import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

import dash
from dash import dcc, html
import plotly.express as px


load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "salary_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD")
TABLE_NAME = os.getenv("TABLE_NAME", "job_salary_prediction_dataset")

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)

query = f"SELECT * FROM {TABLE_NAME};"
df = pd.read_sql(query, engine)

average_salary = round(df["salary"].mean(), 2)
maximum_salary = round(df["salary"].max(), 2)
minimum_salary = round(df["salary"].min(), 2)
total_jobs = len(df)

salary_by_experience = (
    df.groupby("experience_years", as_index=False)["salary"]
    .mean()
    .sort_values("experience_years")
)

salary_by_education = (
    df.groupby("education_level", as_index=False)["salary"]
    .mean()
    .sort_values("salary", ascending=False)
)

salary_by_industry = (
    df.groupby("industry", as_index=False)["salary"]
    .mean()
    .sort_values("salary", ascending=False)
)

salary_by_company_size = (
    df.groupby("company_size", as_index=False)["salary"]
    .mean()
    .sort_values("salary", ascending=False)
)

salary_by_remote_work = (
    df.groupby("remote_work", as_index=False)["salary"]
    .mean()
    .sort_values("remote_work")
)

salary_by_remote_work["remote_work"] = salary_by_remote_work["remote_work"].replace(
    {0: "On-site", 1: "Remote"}
)

salary_by_skills = (
    df.groupby("skills_count", as_index=False)["salary"]
    .mean()
    .sort_values("skills_count")
)

fig_experience = px.line(
    salary_by_experience,
    x="experience_years",
    y="salary",
    markers=True,
    title="Average Salary by Experience Years",
)

fig_education = px.bar(
    salary_by_education,
    x="education_level",
    y="salary",
    color="education_level",
    title="Average Salary by Education Level",
)

fig_industry = px.bar(
    salary_by_industry,
    x="industry",
    y="salary",
    color="industry",
    title="Average Salary by Industry",
)

fig_company_size = px.bar(
    salary_by_company_size,
    x="company_size",
    y="salary",
    color="company_size",
    title="Average Salary by Company Size",
)

fig_remote = px.pie(
    salary_by_remote_work,
    names="remote_work",
    values="salary",
    color="remote_work",
    title="Average Salary by Remote Work",
)

fig_skills = px.line(
    salary_by_skills,
    x="skills_count",
    y="salary",
    markers=True,
    title="Average Salary by Skills Count",
)

app = dash.Dash(__name__)

app.layout = html.Div(
    style={
        "backgroundColor": "#f4f6f8",
        "fontFamily": "Arial",
        "padding": "30px",
    },
    children=[
        html.H1(
            "Salary Prediction Dashboard",
            style={
                "textAlign": "center",
                "color": "#1f2937",
                "marginBottom": "10px",
            },
        ),
        html.P(
            "Interactive dashboard created with Plotly Dash to analyze salary KPIs.",
            style={
                "textAlign": "center",
                "color": "#4b5563",
                "fontSize": "18px",
                "marginBottom": "30px",
            },
        ),

        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(4, 1fr)",
                "gap": "20px",
                "marginBottom": "30px",
            },
            children=[
                html.Div(
                    className="card",
                    style={
                        "backgroundColor": "white",
                        "padding": "20px",
                        "borderRadius": "15px",
                        "boxShadow": "0 4px 10px rgba(0,0,0,0.1)",
                        "textAlign": "center",
                    },
                    children=[
                        html.H3("Average Salary"),
                        html.H2(f"${average_salary:,.2f}", style={"color": "#2563eb"}),
                    ],
                ),
                html.Div(
                    style={
                        "backgroundColor": "white",
                        "padding": "20px",
                        "borderRadius": "15px",
                        "boxShadow": "0 4px 10px rgba(0,0,0,0.1)",
                        "textAlign": "center",
                    },
                    children=[
                        html.H3("Maximum Salary"),
                        html.H2(f"${maximum_salary:,.2f}", style={"color": "#16a34a"}),
                    ],
                ),
                html.Div(
                    style={
                        "backgroundColor": "white",
                        "padding": "20px",
                        "borderRadius": "15px",
                        "boxShadow": "0 4px 10px rgba(0,0,0,0.1)",
                        "textAlign": "center",
                    },
                    children=[
                        html.H3("Minimum Salary"),
                        html.H2(f"${minimum_salary:,.2f}", style={"color": "#dc2626"}),
                    ],
                ),
                html.Div(
                    style={
                        "backgroundColor": "white",
                        "padding": "20px",
                        "borderRadius": "15px",
                        "boxShadow": "0 4px 10px rgba(0,0,0,0.1)",
                        "textAlign": "center",
                    },
                    children=[
                        html.H3("Total Job Records"),
                        html.H2(f"{total_jobs:,}", style={"color": "#7c3aed"}),
                    ],
                ),
            ],
        ),

        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(2, 1fr)",
                "gap": "25px",
            },
            children=[
                dcc.Graph(figure=fig_experience),
                dcc.Graph(figure=fig_education),
                dcc.Graph(figure=fig_industry),
                dcc.Graph(figure=fig_company_size),
                dcc.Graph(figure=fig_remote),
                dcc.Graph(figure=fig_skills),
            ],
        ),
    ],
)

if __name__ == "__main__":
    app.run(debug=True, port=8050)