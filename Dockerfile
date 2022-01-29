# Using the official tensorflow serving image from docker hub as base image
FROM python:3.8

# Installing NGINX, used to rever proxy the predictions from SageMaker to TF Serving

RUN echo "deb [arch=amd64] http://storage.googleapis.com/tensorflow-serving-apt stable tensorflow-model-server tensorflow-model-server-universal" | tee /etc/apt/sources.list.d/tensorflow-serving.list 

RUN curl https://storage.googleapis.com/tensorflow-serving-apt/tensorflow-serving.release.pub.gpg | apt-key add -

RUN apt-get update 

RUN apt-get install -y --no-install-recommends tensorflow-model-server

# Copy our model folder to the container
COPY models models

ADD requirements.txt requirements.txt

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

ADD docker/endpoint.sh endpoint.sh

COPY api api

RUN chmod +x endpoint.sh

EXPOSE 8080

# starts NGINX and TF serving pointing to our model
ENTRYPOINT ./endpoint.sh
