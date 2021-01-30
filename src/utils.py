import os
from flask import abort
import pandas as pd
from memoization import cached


def read_data_from_csv_files():
    """
    This called once on the first request received.

    Returns:
        pandas.DataFrame: Single document containinig data from provided csv files.
        The fields are the same as in csv files.
    """
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

    return data_frame


@cached(max_size=5000)
def create_sessions_from_input_data(df, site_url):
    """Based on provided input and site url, creates a separate DataFrame
    containing sessions information such as session_ids and session_duration. 
    Apperantly creating a separate DataFrame is much faster than updating 
    the existing one.

    Args:
        df (pandas.DataFrame): input data
        site_url (str): site to aggregate

    Returns:
        pandas.DataFrame: Table of visits, sorted by 2 dimensions - site_url and visitor_id, 
        containing session_id and session_duration fields:

            site_url	visitor_id	session_id	timestamp	session_duration
        0	www.s_1.com	visitor_1	    1	1347845487	    0
        1	www.s_1.com	visitor_1       1	1347845963	    476
        2	www.s_1.com	visitor_1	    1	1347846347	    860
        3	www.s_1.com	visitor_1000	2	1347845105	    0
        4	www.s_1.com	visitor_1000	2	1347845507	    402
        5	www.s_1.com	visitor_1000	2	1347846003	    898
        6	www.s_1.com	visitor_10000	3	1347881571	    0
        7	www.s_1.com	visitor_10000	3	1347882003	    432
        8	www.s_1.com	visitor_10000	3	1347882465	    894
        9	www.s_1.com	visitor_1002	4	1347866280	    0
        10	www.s_1.com	visitor_1002	4	1347866722	    442
        11	www.s_1.com	visitor_1002	4	1347867226	    946
        12	www.s_1.com	visitor_1002	4	1347867490	    1210
        13	www.s_1.com	visitor_1002	4	1347868210	    1930
        14	www.s_1.com	visitor_1002	4	1347868480	    2200
        15	www.s_1.com	visitor_1002	4	1347869050	    2770
        16	www.s_1.com	visitor_1002	5	1347888253	    0
        17	www.s_1.com	visitor_1002	5	1347888722	    469
        18	www.s_1.com	visitor_1009	6	1347881004	    0
        19	www.s_1.com	visitor_1009	6	1347881365	    361
        20	www.s_1.com	visitor_1009	6	1347881838	    834
        21	www.s_1.com	visitor_1009	6	1347882389	    1385
        22	www.s_1.com	visitor_1020	7	1347859159	    0
        23	www.s_1.com	visitor_1020	7	1347859743	    584
        24	www.s_1.com	visitor_1021	8	1347845076	    0
        25	www.s_1.com	visitor_1021	8	1347845547	    471
        26	www.s_1.com	visitor_1021	8	1347846064	    988
        27	www.s_1.com	visitor_1021	8	1347846303	    1227
        28	www.s_1.com	visitor_1021	8	1347846846	    1770
        29	www.s_1.com	visitor_1021	8	1347847548	    2472
        30	www.s_1.com	visitor_1025	9	1347859802	    0

        ...
    """
    grouped = df[df.site_url == site_url].groupby('visitor_id')

    if len(grouped) == 0:
        abort(404)

    sessions = []
    session_id = 0

    for group in grouped.groups:
        site_visitor_visits = grouped.get_group(group).sort_values('timestamp')
        """	site_visitor_visits contains only visits of a single visitor to a site,
        sorted by timestamp, it has the following form:

                visitor_id	site_url	page_view_url	timestamp
        4160	visitor_1	www.s_1.com	www.s_1.com/page_1	1347845487
        7047	visitor_1	www.s_1.com	www.s_1.com/page_2	1347845963
        8905	visitor_1	www.s_1.com	www.s_1.com/page_3	1347846347
        """
        # The code below iterates through the site_visitor_visits 
        # (visits a single visitor to a site) and attaches 
        # session_ids and session_duration fields to each visit based on timestamp.
        session_id += 1
        session_start = site_visitor_visits.iloc[0].timestamp
        prev_timestamp = session_start
        for visit in site_visitor_visits.iterrows():
            session_duration = visit[1].timestamp - session_start

            # If prev visit occured more than 30 min ago, start new session
            if visit[1].timestamp - prev_timestamp > 60 * 30:
                session_id += 1
                session_start = visit[1].timestamp
                session_duration = 0
            
            prev_timestamp = visit[1].timestamp
            
            # add the result to a simple list
            sessions.append((visit[1].site_url, visit[1].visitor_id,
                             session_id, visit[1].timestamp, session_duration))
    
    # create pandas DataFrame from a list of sessions collected before 
    sessions_df = pd.DataFrame.from_records(
        sessions, columns=['site_url',
                           'visitor_id',
                           'session_id',
                           'timestamp',
                           'session_duration'])
    return sessions_df
