import numpy as np
from PIL import Image
from flask import jsonify


class ApiException(Exception):
    """
    Encapsulates info about the error response that should be sent
    to the client. Raise during api request handling.
    """

    def __init__(self, message, http_code=400):
        """
        :param message: str, message returned in the response
        :param http_code: int, HTTP status code of the response
        """
        self.message = message
        self.http_code = http_code

    def __str__(self):
        return self.message


def generate_error_response(exception):
    """
    Generate JSON serialized api error response out of given exception.

    :param exception: `Exception`, exception.
    :return: Flask Response object
    """
    body = {"message": str(exception)}

    resp = jsonify({"error": body})
    resp.status_code = 400 if not hasattr(exception, "http_code") \
        else exception.http_code

    return resp


def generate_ok_response(data, http_code=200):
    """
    Generate API response with data. Creates dict with 'data' key with
    `data` object as value, dict is jsonified and returned as a response.

    :param data: dict, resposne data
    :param http_code: int, standard HTTP response code
    :returns: Flask Response object
    """
    resp = jsonify({"data": data})
    resp.status_code = http_code
    return resp


def preprocess_jpeg_image(data, shape):
    """
    Resize given image into target shape and convert it to grayscale. Return as
    a numpy ndarray.

    :param data: BytesIO, jpeg encoded image
    :param shape: tuple (int, int), target image shape
    :returns: np.ndarray, decoded image
    """
    img = Image.open(data)
    img.load()

    if img.format != "JPEG":
        raise Exception("Image must be JPEG encoded")

    # convert to grayscale
    img = img.convert("L")

    # scale to given shape
    img = img.resize(shape, Image.ANTIALIAS)

    decoded_img = np.asarray(img)
    if decoded_img.ndim < 2:
        raise Exception("Failed to decode JPEG image")

    return decoded_img
