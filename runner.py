import logging

from flask import Flask

import config
from api import bp
from helpers import ApiException, generate_error_response
from model_client import ModelClient


def create_and_init_app():
    """
    Initialize flask app instance.
    """
    app = Flask(__name__)
    app.model_client = ModelClient(config.model_server_uri, config.model_name)
    app.register_blueprint(bp)
    app.register_error_handler(
        code_or_exception=ApiException, f=generate_error_response)
    return app


logging.basicConfig(level=logging.INFO)
app = create_and_init_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config.dev_port)
