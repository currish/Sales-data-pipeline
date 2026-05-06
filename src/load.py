from sqlalchemy import create_engine

def load_data(df):
    engine = create_engine("postgresql://postgres:postgres@localhost:5432/sales")

    print("\n Loading data into Postgres")
    df.to_sql("sales_raw", engine, if_exists="replace", index=False)

    print("Data successfully loaded into sales_raw table")