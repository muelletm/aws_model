# Using the official tensorflow serving image from docker hub as base image
FROM tensorflow/serving

# Installing NGINX, used to rever proxy the predictions from SageMaker to TF Serving
RUN apt-get update && apt-get install -y --no-install-recommends nginx

# Copy our model folder to the container
COPY models models

# Copy NGINX configuration to the container
COPY docker/nginx.conf /etc/nginx/nginx.conf

ADD docker/endpoint.sh endpoint.sh

RUN chmod +x endpoint.sh

EXPOSE 8080

# starts NGINX and TF serving pointing to our model
ENTRYPOINT ./endpoint.sh
