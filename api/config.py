import os
import sys
import json
from voluptuous import Schema


# model server uri in format host:port
model_server_uri = "localhost:9000"

# name of the model
model_name = "mnist"


_schema = Schema({
    "model_server_uri": str,
    "model_name": str
})


def _update(config):
    """
    Validate given config values and apply them.

    :param config: dict, config values to set
    """
    config = _schema(config)
    for key, value in config.items():
        if value is not None:
            setattr(sys.modules[__name__], key, value)


def _update_from_json():
    """
    Update config with values from JSON file. File path is expected to be in
    env var MNIST_CONFIG.
    """
    config_file_path = os.environ.get("MNIST_CONFIG", "")
    if os.path.isfile(config_file_path):
        with open(config_file_path, "r") as f:
            _update(json.load(f))


def _update_from_env():
    """
    Update config with values from env vars.
    """
    env_config = {
        "model_server_uri": os.environ.get("MNIST_MODEL_SERVER_URI"),
        "model_name": os.environ.get("MNIST_MODEL_NAME")
    }
    _update({key: val for key, val in env_config.items() if val is not None})


_update_from_json()
_update_from_env()
