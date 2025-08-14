import asyncio
import asyncpg
import os

async def main():
    """
    Connects to the database, creates a table, inserts a row,
    selects the row. Includes a retry loop for the initial connection.
    """
    db_user = os.getenv("DB_USER", "postgres")  # default for development
    db_pass = os.getenv("DB_PASS", "password")  # default for development
    db_name = os.getenv("DB_NAME", "appdb")     # default for development
    db_host = os.getenv("DB_HOST", "localhost") # default for development, this will be replaced with the service name "db" in Docker Compose.
    db_port = os.getenv("DB_PORT", "5432")      # default for development

    conn = None
    retries = 10
    for i in range(1, retries+1):
        try:
            print("Attempting to connect to the database...")
            conn = await asyncpg.connect(
                user=db_user,
                password=db_pass,
                database=db_name,
                host=db_host,
                port=db_port
            )
            print("Connected to database")
            break
        except Exception as e:
            print(f"Connection failed. Retrying... ({retries-i} retries left)")
            print(f"Error: {e}")

    if not conn:
        print("Could not connect to the database after several attempts. Exiting.")
        return

    try:
        # Create a table (if it doesn't exist)
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS users(
                id serial PRIMARY KEY,
                name text
            )
        ''')
        print("Table 'users' is ready.")

        # Insert a new record
        await conn.execute("INSERT INTO users(name) VALUES($1)", 'Test_User')
        print("Inserted a new user: Test_User")

        # Query the record
        user = await conn.fetchrow("SELECT * FROM users WHERE name = $1", 'Test_User')
        if user:
            print(f"Found user: {dict(user)}")
        else:
            print("Could not find the user.")

    finally:
        # Close the connection
        await conn.close()
        print("Database connection closed.")

asyncio.run(main())
