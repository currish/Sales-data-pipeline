from clean import clean_data
from load import load_data
from sqlalchemy import create_engine, text

def run_pipeline():

    print("\nSTARTING PIPELINE")

    path = "data/assignment_dataset.csv"

    print("\nCLEANING DATA")
    df = clean_data(path)

    print("\nLOADING DATA")
    load_data(df)

    print("\nRUNNING SQL TRANSFORMATIONS")
    engine = create_engine("postgresql://postgres:postgres@localhost:5432/sales")

    with open("src/transform.sql", "r") as f:
        sql = f.read()

    with engine.begin() as conn:
        conn.execute(text(sql))

    print("\nPIPELINE COMPLETED SUCCESSFULLY")


if __name__ == "__main__":
    run_pipeline()