from flask import Flask
app = Flask(__name__)

def init_from_csv():
    pass

@app.route('/')
def hello_world():
    return 'Hello, World!'

