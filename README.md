# MNIST API

MNIST API is a classifier for handwritten digits. Main purpose of the API is to take a JPEG-encoded image of a handwritten digit and returns a JSON-encoded response containing an integer value of the received digit.

## 1. Endpoints

### /classify

Classify given image into a numeric value.

#### Request

POST request of content-type `image/jpeg` which includes JPEG-encoded image in the request body.

#### Response

JSON request with the following structure:
```
{
  "data": {
    "digit": <number>
  }
}
```
where `<number>` is an integer between 0 and 9, inclusive.

#### Example

Assuming that file `7.jpg` exists in the current directory and the API is up and running on `localhost` on port `5000`., request can be made using `curl` with the following command:
```
curl -XPOST --data-binary "@7.jpg" http://localhost:5000/classify
```
Images for testing are available in `resources` subdir.

## 2. Running in dev environment

### Install dependencies

API is implemented using Python 3. Dependencies can be installed using `pip`. Position into `api` subdir and run the following command:
```
pip3 install -r requirements.txt
```

### Run API

Position into `api` subdir and run the following command:
```
python3 runner.py
```
After that, API is available on `localhost:5000`

## 3. Building for production

API can be built for production using docker. Position into `api` subdir and run the following command:
```
docker build -t mnist .
```
The command above will produce a docker image named `mnist`. In order to push it to a docker registry additional commands are required:
```
docker tag mnist <registry_uri>/mnist:<tag>
docker push <registry_uri>/mnist:<tag>
```
## 4. Configuration

Service can be configured using JSON config file and/or environment variables. The following table lists all config options

| JSON key         | env variable name      | default        | description                                         |
|------------------|------------------------|----------------|-----------------------------------------------------|
|`model_server_uri`|`MNIST_MODEL_SERVER_URI`|`localhost:8500`|Tensorflow Model Server URI in format `<host>:<port>`|
|`model_name`      |`MNIST_MODEL_NAME`      |`mnist`         |Name of the model on Model Server                    |

If JSON config file is used, an env variable `MNIST_CONFIG` should contain a path to the config file.

## 5. Running

Here are the example `docker run` commands that can be used to run the service using docker, assuming that service is built into image named `mnist`. That is just an example. The service will work with any orchestration tool that can provide the same parameters.

### With default config

```
docker run -p 8080:8080 mnist
```

Afther the command above, API will be available on port `8080`

### Configured through env vars

HINT: Be mindful of container namespacing. Each container has its own complete namespace, including networking. That means, `localhost` in one container is not the same in the other, and not one container
will have it the same as your default system namespace. Luckily, the Dockerfile of this API will build its image in a way that its http server, in this case, `uWSGI`, will listen on all the network
interfaces of the container so when sending http requests, it's enough to expose the ports like in the example below. This will setup port-forwarding from your system's loopback device, i.e.
`localhost:8080` to the container network interface on port 8080. Since `uWSGI` is setup to listen on all of the container's interfaces, it will surely catch the request. In order for the API container to
"see" the model container an additional component will have to be created and specified if you're creating the containers using the docker CLI like in the examples.

```
docker run -e MNIST_MODEL_SERVER_URI=<docker_dns_of_model_server_container>:8500 -e MNIST_MODEL=mnist -p 8080:8080 mnist
```

### Configured through JSON config file

First, create a JSON file on path `/tmp/config.json` with the following contents:
```
{
  "model_server_uri": "localhost:8500",
  "model_name": "mnist"
}
```
Then run the following command:
```
docker run -e MNIST_CONFIG=/config.json -v /tmp/config.json:/config.json:ro -p 8080:8080 mnist
```
