from flask import Flask, jsonify

from .database import get_services
from .logger import log
from .scheduler import initialize_check_schedulers


def create_app():
    """Service Status indicator API"""
    app = Flask(__name__)

    log('Initialize checking schedulers')
    initialize_check_schedulers('services.json', 60)

    @app.route('/services')
    def services():
        """Return the list of services along with there status"""
        return jsonify(get_services())

    log('Listening ...')
    return app


if __name__ == '__main__':
    create_app().run()
