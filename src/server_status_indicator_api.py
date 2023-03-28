from flask import Flask, jsonify


from .database import get_services
from .scheduler import initialize_check_schedulers


def create_app():
    """Service Status indicator API"""
    app = Flask(__name__)

    initialize_check_schedulers('services.json', 60)

    @app.route('/services')
    def services():
        """Return the list of services along with there status"""
        return jsonify(get_services())

    print('Listening ...')
    return app


if __name__ == '__main__':
    create_app().run()
