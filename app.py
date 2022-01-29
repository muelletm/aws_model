import os
from datetime import datetime
from typing import List, Tuple

import pandas as pd
import requests
import streamlit as st

ENDPOINT_URL = os.environ["ENDPOINT_URL"].strip("/")


def sentiment(text: str):
    response = requests.post(
        url=ENDPOINT_URL + "/sentiment",
        json={"texts": [text]},
        timeout=5,
    )
    if not response.ok:
        raise ValueError(response.content)
    return response.json()


st.set_page_config("Sentiment Model Demo", page_icon="🤖")

st.markdown("## Sentiment Model Demo")

text = st.text_input(
    "text", "Funciona bien, pero para el precio me esperaba más."
)

with st.spinner():
    t_start = datetime.now()
    predictions: List[Tuple[str, float]] = sentiment(text)["predictions"][0]
    t_end = datetime.now()

df = pd.DataFrame(
    [{"stars": "⭐" * int(stars), "probability": p} for stars, p in predictions]
).set_index("stars")

mode = st.sidebar.selectbox("mode", ["table", "bar_chart"], index=1)

if mode == "table":
    st.table(df)
elif mode == "bar_chart":
    st.bar_chart(df)
else:
    raise NotImplementedError(mode)

st.markdown(
    f"Processed request in {(t_end - t_start).total_seconds()} seconds."
)
