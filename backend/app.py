from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import psycopg2
from psycopg2 import sql
import time

app = Flask(__name__)
CORS(app)

db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')

DATABASE_URL = f"host='{db_host}' port='{db_port}' dbname='{db_name}' user='{db_user}' password='{db_password}'"

conn = None
for i in range(10):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        print("Connection successful")
        break
    except psycopg2.OperationalError:
        print("PostgreSQL connection failed, will retry...")
        time.sleep(5)
else:
    print("PostgreSQL connection could not be established, terminating the program...")
    exit(1)

cur = conn.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS data (
        id SERIAL PRIMARY KEY,
        value1 TEXT NOT NULL,
        value2 TEXT NOT NULL
    )
''')
conn.commit()


@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    value1 = data['value1']
    value2 = data['value2']

    cur.execute(sql.SQL("INSERT INTO data (value1, value2) VALUES (%s, %s)"), [value1, value2])
    conn.commit()

    return jsonify({'message': 'Data submitted successfully!'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
