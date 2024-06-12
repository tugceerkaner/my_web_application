from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import psycopg2
from psycopg2 import sql
import time
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        logger.info("Connection successful")
        break
    except psycopg2.OperationalError:
        logger.error("PostgreSQL connection failed, will retry...")
        time.sleep(5)
else:
    logger.critical("PostgreSQL connection could not be established, terminating the program...")
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
    try:
        data = request.get_json()
        value1 = data['value1']
        value2 = data['value2']

        cur.execute(sql.SQL("INSERT INTO data (value1, value2) VALUES (%s, %s)"), [value1, value2])
        conn.commit()

        return jsonify({'message': 'Data submitted successfully!'})
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        return jsonify({'message': 'An error occurred while submitting data'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
