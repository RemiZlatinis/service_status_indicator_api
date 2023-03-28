import os
from flask import Flask, jsonify, request

from .database import get_services
from .logger import log, error
from .scheduler import initialize_check_schedulers

TOKEN = os.environ.get("SERVICE_STATUS_INDICATOR_API_TOKEN", None)

if not TOKEN:
    error("SERVICE_STATUS_INDICATOR_API_TOKEN environment variable not set")
    exit(1)


def create_app():
    """Service Status Indicator API"""
    app = Flask(__name__)

    log('Initialize checking schedulers')
    initialize_check_schedulers('services.json', 60)

    @app.route('/services')
    def services():
        """Return the list of services along with there status"""
        # Check if is an authenticated request
        token = request.headers.get('Authorization')
        if token != f'Token {TOKEN}':
            return jsonify({'error': 'Unauthorized access'}), 401

        return jsonify(get_services())

    log('Listening ...')
    return app


if __name__ == '__main__':
    create_app().run()
