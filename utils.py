import pandas as pd
from memoization import cached


@cached(max_size=1000)
def sessionize_data(df, site_url):
    grouped = df[df.site_url == site_url].groupby('visitor_id')

    sessions = []
    session_id = 0

    for group in grouped.groups:
        site_visitor_visits = grouped.get_group(group).sort_values('timestamp')
        session_start = site_visitor_visits.iloc[0].timestamp
        session_id += 1
        prev_timestamp = session_start
        for visit in site_visitor_visits.iterrows():
            session_duration = visit[1].timestamp - session_start

            if visit[1].timestamp - prev_timestamp > 60 * 30:
                session_id += 1
                session_start = visit[1].timestamp
                session_duration = 0
            prev_timestamp = visit[1].timestamp
            sessions.append((visit[1].site_url, visit[1].visitor_id,
                             session_id, visit[1].timestamp, session_duration))

    sessions_df = pd.DataFrame.from_records(
        sessions, columns=['site_url',
                           'visitor_id',
                           'session_id',
                           'timestamp',
                           'session_duration'])
    return sessions_df
