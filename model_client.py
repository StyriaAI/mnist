import tensorflow as tf
import numpy as np
from grpc import insecure_channel
from tensorflow.python.framework import tensor_util
from tensorflow_serving.apis.predict_pb2 import PredictRequest
from tensorflow_serving.apis.prediction_service_pb2 import (
    PredictionServiceStub)

INPUT_NAME = "image"
OUTPUT_NAME = "classes"
GRAPH_SIGNATURE_NAME = "classify"
SIGNATURE_DEF_KEY = "signature_def"


class ModelClient(object):
    """
    Client for Tensorflow Model Server.
    """
    def __init__(self, model_server_uri, model_name, timeout=10):
        """
        Initialize ModelClient instance.

        :param model_server_uri: str, model server uri in format 'host:port'
        :param model_name: str, name of the model
        :param timeout: str, model server timeout in seconds
        """
        channel = insecure_channel(target=model_server_uri)
        self.stub = PredictionServiceStub(channel=channel)
        self.model_name = model_name
        self.timeout = timeout

    def classify(self, img):
        """
        Classify given image using Model Server.

        :param img: np.ndarray, image to classify
        """
        batch = np.array([img.astype(np.float32) / 255])
        request = PredictRequest()
        tensor_proto = tf.make_tensor_proto(batch)
        request.inputs[INPUT_NAME].CopyFrom(tensor_proto)
        request.model_spec.name = self.model_name
        request.model_spec.signature_name = GRAPH_SIGNATURE_NAME

        response = self.stub.Predict(request, self.timeout)

        tensor_proto = response.outputs[OUTPUT_NAME]
        classes = tensor_util.MakeNdarray(tensor_proto)

        assert classes.shape == (1,)
        return int(classes[0])
