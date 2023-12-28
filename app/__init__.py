from flask import Flask
import sqlite3

# Initialize the Flask application
app = Flask(__name__)

# Database file path
DATABASE = 'smoking_habits.db'

# Function to get database connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database
def init_db() -> None:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS habits (
                            date TEXT PRIMARY KEY,
                            smoking_level INTEGER,
                            emoji TEXT)''')
        conn.commit()

# Import the routes from views.py
from app import views

# Initialize the database
init_db()
