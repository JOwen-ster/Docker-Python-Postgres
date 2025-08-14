import asyncio
import asyncpg
from os import getenv
from dotenv import load_dotenv


# The docker compose discord_bot service loads 1 environment variable when started
# If you are not using docker to run this application, that env var will never be loaded
# This is how we switch from locally running to runing in a containerized environment
is_containerized = getenv("IS_DOCKER_CONTAINER") # True or None

async def main():
    load_dotenv()
    """
    Connects to the database, creates a table, inserts a row,
    selects the row. Includes a retry loop for the initial connection.
    """

    env_msg = None
    if is_containerized:
        # Postgre Server Created By Postgre Docker Image
        env_msg = 'Docker Environment Variable Set - Using Container Env Vars.'
        print(env_msg)
        DB_USER = getenv('POSTGRES_USER')    
        DB_PASS = getenv('POSTGRES_PASSWORD')
        DB_NAME = getenv('POSTGRES_DB')   
        DB_HOST = getenv('POSTGRES_HOST')    
        DB_PORT = getenv('POSTGRES_PORT')    
    else:
        # Locally Hosted Postre Server, NOT Created By Postgre Docker Image
        env_msg = 'Docker Environment Variable Not Found - Using Local Env Vars.'
        DB_USER = getenv('LOCAL_POSTGRES_USER')     # development environment variable
        DB_PASS = getenv('LOCAL_POSTGRES_PASSWORD') # development environment variable
        DB_NAME = getenv('LOCAL_POSTGRES_DB')       # development environment variable
        DB_HOST = getenv('LOCAL_POSTGRES_HOST')     # development environment variable
        DB_PORT = getenv('LOCAL_POSTGRES_PORT')     # development environment variable

    try:
        print("Attempting to connect to the database...")
        conn = await asyncpg.connect(
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
            host=DB_HOST,
            port=DB_PORT
        )
        print("Connected to database")
    except Exception as e:
        print(f"Error: {e}")
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

        # Insert a new row
        await conn.execute("INSERT INTO users(name) VALUES($1)", 'Test_User')
        print("Inserted a new user: Test_User")

        # Select the new row
        user = await conn.fetchrow("SELECT * FROM users WHERE name = $1", 'Test_User')
        if user:
            print(f"Found user: {dict(user)}")
        else:
            print("Could not find the user.")

    except Exception as conn_error:
        print(conn_error)

    finally:
        # Close the connection
        await conn.close()
        print("Database connection closed.")

asyncio.run(main())
