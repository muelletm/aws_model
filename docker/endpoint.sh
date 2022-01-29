#!/bin/bash

set -ue

echo "tensorflow_model_server"
tensorflow_model_server \
  --rest_api_port=8501 \
  --model_name=sentiment \
  --model_base_path=/models/sentiment &
sleep 5

export TENSORFLOW_SERVER_URL="http://localhost:8501"

echo "fastapi"
uvicorn api.main:app --host 0.0.0.0 --port=8080 &
sleep 5

echo "done"
wait
