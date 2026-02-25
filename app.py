import os
from flask import Flask, render_template

app=Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/api/chat/<room>', methods=['GET'])
def get_chat(room):
    filename = f"{room}.txt"
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return file.read()
    else:
        return ''

if __name__ == '__main__': 
    app.run(debug=True)