import json
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request
from views import error_handler, ui, api_v1_url
from settings import settings


json_formatter = logging.Formatter(
    "{\"time\":\"%(asctime)s\", \"func\": \"%(funcName)s\", \"level\": \"%(levelname)s\", \"message\": %(message)s}"
)
file_handler = RotatingFileHandler("logs/app.log", maxBytes=5000000, backupCount=5)
file_handler.setFormatter(json_formatter)


def create_app():
    app = Flask(__name__)

    # Setting endpoints
    app.register_blueprint(ui)
    app.register_blueprint(api_v1_url, url_prefix='/v1')

    # Setting error handler
    app.register_blueprint(error_handler)

    # Setting logger
    app.logger.setLevel(eval(f'logging.{settings.LOG_LEVEL.upper()}'))
    if settings.FLASK_ENV == 'production':
        app.logger.addHandler(file_handler)

    @app.after_request
    def after_request(response):
        log_data = {
            'req_url': request.base_url,
            'req_data': request.values.to_dict(),
            'resp_content_type': response.content_type,
        }
        if response.content_type == 'application/json':
            log_data['resp_data'] = json.loads(response.data)
        app.logger.info(json.dumps(log_data))
        return response

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host=settings.FLASK_HOST, port=settings.FLASK_PORT)
