from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:postgres@localhost:5432/sales")

try:
    conn = engine.connect()
    print("Connection successful!")
    conn.close()

except Exception as e:
    print("Connection Failed:", e)
