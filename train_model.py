import re
import string
from pathlib import Path

import datasets
import tensorflow as tf
import typer
from tensorflow.keras import Sequential
from tensorflow.keras.layers import (
    Dense,
    Embedding,
    GlobalAveragePooling1D,
    TextVectorization,
)

app = typer.Typer()


def stars_to_label(star: int) -> int:
    if star < 1:
        raise ValueError(star)
    if star > 5:
        raise ValueError(star)
    return star - 1


def to_tf_dataset(ds: datasets.Dataset) -> tf.data.Dataset:
    return tf.data.Dataset.from_tensor_slices(
        (
            ds["review_body"],
            [stars_to_label(star_rating) for star_rating in ds["stars"]],
        )
    ).batch(1)


def custom_standardization(input_data):
    lowercase = tf.strings.lower(input_data)
    punctuation = "[%s]" % re.escape(string.punctuation)
    return tf.strings.regex_replace(lowercase, punctuation, "")


@app.command()
def train(
    epochs: int = 10,
    embedding_dim: int = 16,
    vocab_size: int = 10_000,
    max_sequence_length: int = 100,
    version: int = 1,
):

    # https://huggingface.co/datasets/amazon_reviews_multi
    data = datasets.load_dataset("amazon_reviews_multi", "es")

    train_ds = to_tf_dataset(
        data["train"].shuffle(seed=42).select(range(10_000))
    )
    val_ds = to_tf_dataset(
        data["validation"].shuffle(seed=42).select(range(100))
    )

    vectorize_layer = TextVectorization(
        standardize=custom_standardization,
        max_tokens=vocab_size,
        output_mode="int",
        output_sequence_length=max_sequence_length,
    )
    text_ds = train_ds.map(lambda x, _: x)
    vectorize_layer.adapt(text_ds)

    model = Sequential(
        [
            vectorize_layer,
            Embedding(vocab_size, embedding_dim),
            GlobalAveragePooling1D(),
            Dense(embedding_dim, activation="relu"),
            Dense(5, activation="softmax"),
        ]
    )

    model.compile(
        optimizer="adam",
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
        metrics=["accuracy"],
    )

    model.summary()

    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs,
    )

    export_path = Path("models", "sentiment", str(version))
    tf.saved_model.save(model, str(export_path))


if __name__ == "__main__":
    app()
