import os
import logging
import pandas as pd
from flask import Flask, request, make_response
from utils import sessionize_data


app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

INPUT_DATA = None


@app.before_first_request
def init_input_data():
    global INPUT_DATA
    csv_files = [
        os.path.join("assignment", "input_1.csv"),
        os.path.join("assignment", "input_2.csv"),
        os.path.join("assignment", "input_3.csv")
    ]
    data_frame = pd.DataFrame()
    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        df.columns = ["visitor_id", "site_url", "page_view_url", "timestamp"]
        data_frame = data_frame.append(df, ignore_index=True)

    INPUT_DATA = data_frame


@app.route('/')
def index():
    return "Ok, I'm up and running"


@app.route('/num_sessions')
def num_sessions():
    site_url = request.args.get('site_url')

    sessions_df = sessionize_data(INPUT_DATA, site_url)
    
    num_sessions = len(sessions_df.groupby('session_id'))
    
    result = "Num sessions for site %(site_url)s = %(num_sessions)s" % {
        "site_url": site_url,
        "num_sessions": num_sessions
    }

    response = make_response(result, 200)
    response.mimetype = "text/plain"
    response.data.decode("utf-8")
    return result


@app.route('/median_session_length')
def median_session_length():
    site_url = request.args.get('site_url')

    sessions_df = sessionize_data(INPUT_DATA, site_url)
    
    median_session_length = sessions_df.groupby('session_id').last().session_duration.median()
    
    result = "Median session length for site %(site_url)s = %(median_session_length)s" % {
        "site_url": site_url,
        "median_session_length": median_session_length
    }

    return result