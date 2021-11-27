from run import configure_routes
from flask import Flask, render_template


def test_home_page():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the status is 200
    """
    app = Flask(__name__, template_folder='../../templates')
    configure_routes(app)
    test_client = app.test_client()

    response = test_client.get('/')
    assert response.status_code == 200

def test_ticket_details_page():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/ticket' page is requested (GET)
    THEN check that the status is 200
    """
    app = Flask(__name__, template_folder='../../templates')
    configure_routes(app)
    test_client = app.test_client()

    response = test_client.get('/ticket?id=1')
    assert response.status_code == 200

def test_404_error_page():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/error' page(incorrect route) is requested (GET)
    THEN check that the status is 404
    """
    app = Flask(__name__, template_folder='../../templates')
    configure_routes(app)
    test_client = app.test_client()

    response = test_client.get('/error')
    assert response.status_code == 404