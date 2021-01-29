import os
import pandas as pd
from flask import Flask

app = Flask(__name__)

def init(csv_files):
    dfs = []
    for f in csv_files:
        dfs.append(pd.read_csv(f))
    df = pd.concat(dfs, ignore_index = True)
    return df


csv_files = [
    os.path.join("assignment", "input_1.csv"),
    os.path.join("assignment", "input_2.csv"),
    os.path.join("assignment", "input_3.csv")
]

init(csv_files)

@app.route('/')
def hello_world():
    return 'Hello, World!'

