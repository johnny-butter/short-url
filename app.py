from flask import Flask
from views import ui, api_v1_url
from settings import settings


def create_app():
    app = Flask(__name__)

    # Setting endpoints
    app.register_blueprint(ui)
    app.register_blueprint(api_v1_url, url_prefix='/v1')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host=settings.FLASK_HOST, port=settings.FLASK_PORT)
