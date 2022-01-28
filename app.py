import os
from datetime import datetime

import pandas as pd
import requests
import streamlit as st

ENDPOINT_URL = os.environ["ENDPOINT_URL"]


def call_model(text: str):
    response = requests.post(
        url=ENDPOINT_URL,
        json={"signature_name": "serving_default", "instances": [text]},
        timeout=5,
    )
    if not response.ok:
        raise ValueError(response.content)
    return response.json()


text = st.text_input("text", "¡Me encanta este producto!")

with st.spinner():
    t_start = datetime.now()
    predictions = call_model(text)["predictions"][0]
    t_end = datetime.now()

# predictions = [round(p, 3) for p in predictions]

df = pd.DataFrame(
    [
        {"stars": "*" * (i + 1), "probability": p}
        for i, p in enumerate(predictions)
    ]
).set_index("stars")

st.table(df)


st.markdown(
    f"Processed request in {(t_end - t_start).total_seconds()} seconds."
)