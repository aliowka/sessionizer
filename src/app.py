import time
import logging
import pandas as pd
from flask import Flask, request
from flask_cors import CORS, cross_origin
from utils import create_sessions_from_input_data, read_data_from_csv_files


app = Flask(__name__,
            static_url_path='',
            static_folder='static')
cors = CORS(app)
app.logger.setLevel(logging.DEBUG)
app.config['CORS_HEADERS'] = 'Content-Type'

INPUT_DATA = None


@app.before_first_request
def init_input_data():
    """
    Initialize input data from csv files.
    Called once before first request
    """
    global INPUT_DATA
    INPUT_DATA = read_data_from_csv_files()


@app.route('/')
@cross_origin()
def index():
    """
    Returns index.html which contains ajax requests 
    for num_session with different sites. This will create 
    the sessions for those different sites and cache the 
    results, so that further requests will be fast. 

    Returns:
        str: html document
    """
    return open("static/index.html").read()


@app.route('/num_sessions')
@cross_origin()
def num_sessions():
    """
    Calculates num_session for a given site_url,
    uses create_sessions_from_input_data
    which is cached with memoization for the same site_url.
    ajax requests from main page will precompute those results
    to speedup further use.

    Returns:
        str: number of session for given site
    """
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
@cross_origin()
def median_session_length():
    """
    Calculates median of session length for given site_url.
    uses create_sessions_from_input_data,
    which is cached with memoization for the same site_url
    ajax requests from main page will precompute those 
    results to speedup futher use.

    Returns:
        str: median of session lenghes for given site
    """
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
@cross_origin()
def num_unique_visited_sites():
    """
    This method *currently* does not require any precomputations since it works 
    fast on provided input data.

    Returns:
        str: number of unique visited sites for specified visitor
    """
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
