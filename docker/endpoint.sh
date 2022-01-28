#!/bin/bash

set -ue

nginx &

tensorflow_model_server \
  --rest_api_port=8501 \
  --model_name=sentiment \
  --model_base_path=/models/sentiment &

wait
