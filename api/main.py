import os
from typing import List, Tuple

import requests
from fastapi import FastAPI
from pydantic import BaseModel

TENSORFLOW_SERVER_URL = os.environ["TENSORFLOW_SERVER_URL"]


app = FastAPI()


class InferenceRequest(BaseModel):
    texts: List[str]


_Prediction = List[Tuple[str, float]]


class InferenceResponse(BaseModel):
    predictions: List[_Prediction]


def call_model(endpoint: str, texts: List[str]) -> List[List[float]]:
    response = requests.post(
        url=TENSORFLOW_SERVER_URL + endpoint,
        json={"signature_name": "serving_default", "instances": texts},
        timeout=5,
    )
    if not response.ok:
        raise ValueError(response.content)
    return response.json()


@app.get("/")
def root():
    return "Sentiment Model API"


@app.post("/sentiment", response_model=InferenceResponse)
def sentiment(request: InferenceRequest) -> InferenceResponse:
    """Calls the sentiment model."""
    result = call_model(
        endpoint="/v1/models/sentiment/versions/1:predict", texts=request.texts
    )
    probs_list = result["predictions"]
    predictions = []
    for probs in probs_list:
        pred = [(str(i + 1), p) for i, p in enumerate(probs)]
        predictions.append(pred)
    return InferenceResponse(predictions=predictions)
