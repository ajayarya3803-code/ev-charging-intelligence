
from sqlalchemy import text
from src.database.connection import get_sql_engine

engine = get_sql_engine()

try:
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT DB_NAME()")
        )

        print("Connected successfully!")
        print("Database:", result.scalar())

except Exception as e:
    print("Connection failed:", e)

finally:
    engine.dispose()
