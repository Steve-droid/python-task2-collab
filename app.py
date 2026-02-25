import os
from datetime import datetime
from flask import Flask, render_template, request

app=Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/<room>', methods=['GET'])
def get_room(room='general'):
    return render_template('index.html')

@app.route('/api/chat/<room>', methods=['GET'])
def get_chat(room):
    filename = f"{room}.txt"
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return file.read()
    else:
        return ''
    

@app.route('/api/chat/<room>', methods=['POST'])
def post_chat(room):
    
    username = request.form.get('username')
    message = request.form.get('msg')

 
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    chat_line = f"[{current_time}] {username}: {message}\n"

    filename = f"{room}.txt"
    
    with open(filename, 'a') as file:
        file.write(chat_line)

    return "Message saved successfully", 201

if __name__ == '__main__': 
    app.run(debug=True)