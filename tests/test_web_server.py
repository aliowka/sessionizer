import flask_unittest
from web_server import app, init_from_csv


class TestFoo(flask_unittest.ClientTestCase):
    # Assign the `Flask` app object
    app = app

    def setUp(self, client):
        pass

    def tearDown(self, client):
        # Perform tear down after each test, using client
        pass

    def test_foo_with_client(self, client):
        # Use the client here
        # Example request to a route returning "hello world" (on a hypothetical app)
        rv = client.get('/')
        assert rv.status_code == 200
