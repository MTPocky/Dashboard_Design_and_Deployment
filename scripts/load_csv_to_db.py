import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


def main():
    load_dotenv()

    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    csv_file = os.getenv("CSV_FILE")
    table_name = os.getenv("TABLE_NAME", "job_salary_prediction_dataset")

    if not all([db_host, db_port, db_name, db_user, db_password, csv_file]):
        raise ValueError("Missing environment variables. Please check your .env file.")

    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"CSV file not found: {csv_file}")

    print("Reading CSV file...")
    df = pd.read_csv(csv_file)

    print("Cleaning column names...")
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    print("Connecting to PostgreSQL...")
    engine = create_engine(
        f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )

    print(f"Loading data into table: {table_name}")
    df.to_sql(table_name, engine, if_exists="replace", index=False)

    with engine.connect() as connection:
        result = connection.execute(text(f"SELECT COUNT(*) FROM {table_name};"))
        total_rows = result.scalar()

    print("Migration completed successfully.")
    print(f"Rows inserted: {total_rows}")
    print(f"Table name: {table_name}")


if __name__ == "__main__":
    main()