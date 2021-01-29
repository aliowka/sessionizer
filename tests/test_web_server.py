import flask_unittest
from server import app


class TestFoo(flask_unittest.ClientTestCase):
    app = app

    def test_basic_run(self, client):
        response = client.get('/')
        assert response.status_code == 200

    def test_num_sessions(self, client):

        test_cases = (
            # site_url,     expected_response
            ('www.s_1.com', 'Num sessions for site www.s_1.com = 3684'),
            ('www.s_2.com', 'Num sessions for site www.s_2.com = 3632'),
            ('www.s_3.com', 'Num sessions for site www.s_3.com = 3640'),
            ('www.s_4.com', 'Num sessions for site www.s_4.com = 3584'),
            ('www.s_5.com', 'Num sessions for site www.s_5.com = 3623'),
            ('www.s_6.com', 'Num sessions for site www.s_6.com = 3712'),
            ('www.s_7.com', 'Num sessions for site www.s_7.com = 3598'),
            ('www.s_8.com', 'Num sessions for site www.s_8.com = 3683'),
            ('www.s_9.com', 'Num sessions for site www.s_9.com = 3730'),
            ('www.s_10.com', 'Num sessions for site www.s_10.com = 3674')
        )

        for test_case in test_cases:
            site_url, expected_response = test_case
            response = client.get('/num_sessions?site_url=%s' % site_url)
            assert response.data == expected_response

    def test_meidan_session_length(self, client):
        test_cases = (
            # site_url,     expected_response
            ('www.s_1.com', 'median session length = 1353.0'),
            ('www.s_2.com', 'median session length = 1341.5'),
            ('www.s_3.com', 'median session length = 1392.5'),
            ('www.s_4.com', 'median session length = 1361.5'),
            ('www.s_5.com', 'median session length = 1375.0'),
            ('www.s_6.com', 'median session length = 1374.0'),
            ('www.s_7.com', 'median session length = 1318.5'),
            ('www.s_8.com', 'median session length = 1353.0'),
            ('www.s_9.com', 'median session length = 1326.5'),
            ('www.s_10.com', 'median session length = 1329.0')
        )

        for test_case in test_cases:
            site, expected_response = test_case
            response = client.get('/median_session_length?site_url=%s' % site)
            assert response.data == expected_response

    def test_num_unique_visited_sites(self, client):
        test_cases = (
            # vosotor_id,     expected_response
            ('1', 'Num of unique sites for visitor_1=3'),
            ('2', 'Num of unique sites for visitor_2=2'),
            ('3', 'Num of unique sites for visitor_3=2'),
            ('4', 'Num of unique sites for visitor_4=4'),
            ('5', 'Num of unique sites for visitor_5=4'),
            ('6', 'Num of unique sites for visitor_6=1'),
            ('7', 'Num of unique sites for visitor_7=3'),
            ('8', 'Num of unique sites for visitor_8=3'),
            ('9', 'Num of unique sites for visitor_9=2'),
            ('10', 'Num of unique sites for visitor_10=4')
        )

        for test_case in test_cases:
            site, expected_response = test_case
            response = client.get('/num_unique_visited_sites?visitor_id=%s' % site)
            assert response.data == expected_response
