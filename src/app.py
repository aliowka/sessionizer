import time
import logging
import pandas as pd
from flask import Flask, request
from utils import create_sessions_from_input_data, read_data_from_csv_files

app = Flask(__name__,
            static_url_path='',
            static_folder='static')
app.logger.setLevel(logging.DEBUG)

INPUT_DATA = None


@app.before_first_request
def init_input_data():
    global INPUT_DATA
    INPUT_DATA = read_data_from_csv_files()


@app.route('/')
def index():
    return open("static/index.html").read()


@app.route('/num_sessions')
def num_sessions():
    site_url = request.args.get('site_url')

    if not site_url:
        return "site_url not provided", 400

    df = INPUT_DATA
    sessions_df = create_sessions_from_input_data(df, site_url)
    num_sessions = len(sessions_df.groupby('session_id'))
    result = "Num sessions for site %(site_url)s = %(num_sessions)s" % {
        "site_url": site_url,
        "num_sessions": num_sessions
    }
    return result


@app.route('/median_session_length')
def median_session_length():
    site_url = request.args.get('site_url')

    if not site_url:
        return "site_url not provided", 400

    df = INPUT_DATA
    sessions_df = create_sessions_from_input_data(df, site_url)
    median_session_length = sessions_df.groupby(
        'session_id').last().session_duration.median()
    result = "Median session length for site %(site_url)s = %(median_session_length)s" % {
        "site_url": site_url,
        "median_session_length": median_session_length
    }
    return result


@app.route('/num_unique_visited_sites')
def num_unique_visited_sites():
    visitor_id = request.args.get('visitor_id')

    if not visitor_id:
        return "visitor_id not provided", 400

    df = INPUT_DATA
    unique_sites = len(df[df.visitor_id == visitor_id].groupby(df.site_url))
    result = "Num of unique sites for %(visitor_id)s = %(unique_sites)s" % {
        "visitor_id": visitor_id,
        "unique_sites": unique_sites
    }
    return result
