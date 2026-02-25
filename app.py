import os
import time
from datetime import datetime
from flask import Flask, render_template, request
import mysql.connector

app=Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get('DB_HOST'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('MYSQL_ROOT_PASSWORD'),
        database=os.environ.get('DB_NAME')
    )

def init_db():
    retries = 5
    while retries > 0:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    room VARCHAR(50) NOT NULL,
                    username VARCHAR(50) NOT NULL,
                    message TEXT NOT NULL,
                    created_at DATETIME NOT NULL
                )
            ''')
            conn.commit()
            cursor.close()
            conn.close()
            print("Database connected and table ready!")
            break
        except mysql.connector.Error as err:
            print(f"Database not ready yet, retrying in 3 seconds... ({err})")
            retries -= 1
            time.sleep(3)

init_db()

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/<room>', methods=['GET'])
def get_room(room='general'):
    return render_template('index.html')

@app.route('/api/chat/<room>', methods=['GET'])
def get_chat(room):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM messages WHERE room = %s ORDER BY created_at ASC", (room,))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    chat_history = ""
    for row in rows:
        formatted_time = row['created_at'].strftime("%Y-%m-%d %H:%M:%S")
        chat_history += f"[{formatted_time}] {row['username']}: {row['message']}\n"
        
    return chat_history

    

@app.route('/api/chat/<room>', methods=['POST'])
def post_chat(room):
    
    username = request.form.get('username')
    message = request.form.get('msg')

    current_time = datetime.now()

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO messages (room, username, message, created_at) VALUES (%s, %s, %s, %s)",
        (room, username, message, current_time)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return "Message saved successfully", 201


if __name__ == '__main__': 
    app.run(debug=True, host='0.0.0.0')