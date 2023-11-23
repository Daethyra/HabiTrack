from typing import Any
from flask import request, jsonify, render_template
import sqlite3
import pandas as pd
from app import app, get_db_connection

# Function to determine emoji
def determine_emoji(level: int) -> str:
    emoji_map = {0: '✅', 1: '🤘🏼', 2: '⚠️', 3: '🛑'}
    return emoji_map.get(level, '❓')

# Route for landing page
@app.route('/')
def index():
    return render_template('index.html')

# Route for fetching the last 7 days of data
@app.route('/get_data', methods=['GET'])
def get_data() -> Any:
    conn = get_db_connection()
    data = pd.read_sql_query('SELECT * FROM habits ORDER BY date DESC LIMIT 7', conn)
    conn.close()
    return jsonify(data.to_dict(orient='records'))

# Route for adding a new entry
@app.route('/add_entry', methods=['POST'])
def add_entry() -> Any:
    data = request.json
    date = data.get('date')
    level = data.get('level')

    if not date or level is None:
        return jsonify({'status': 'error', 'message': 'Missing date or level'}), 400

    try:
        level_int = int(level)
    except ValueError:
        return jsonify({'status': 'error', 'message': 'Invalid level format'}), 400

    emoji = determine_emoji(level_int)
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO habits (date, smoking_level, emoji) VALUES (?, ?, ?)', (date, level_int, emoji))
            conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({'status': 'error', 'message': 'Entry for this date already exists'}), 409

    return jsonify({'status': 'success'})

# Route for exporting data to Excel
@app.route('/export', methods=['GET'])
def export_data() -> Any:
    try:
        conn = get_db_connection()
        data = pd.read_sql_query('SELECT * FROM habits', conn)
        conn.close()
        export_file = 'smoking_habits.xlsx'
        data.to_excel(export_file, index=False)
        return jsonify({'status': 'success', 'file': export_file})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
