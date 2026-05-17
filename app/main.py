import time
from typing import List

import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel, Field
from prometheus_client import Histogram, generate_latest, CONTENT_TYPE_LATEST
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from starlette.responses import Response


app = FastAPI(title="Iris ML Service with Prometheus Monitoring")


LATENCY = Histogram(
    "request_latency_seconds",
    "Request latency",
)


iris = load_iris()
X, y = iris.data, iris.target

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
)

model.fit(X, y)


class IrisFeatures(BaseModel):
    features: List[float] = Field(
        ...,
        min_length=4,
        max_length=4,
        description="Iris features: sepal length, sepal width, petal length, petal width",
        example=[5.1, 3.5, 1.4, 0.2],
    )


@app.get("/")
def root():
    return {
        "service": "iris-ml-service",
        "status": "ok",
        "model": "RandomForestClassifier",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/predict")
def predict(payload: IrisFeatures):
    start = time.time()

    try:
        features = np.array(payload.features).reshape(1, -1)
        prediction = int(model.predict(features)[0])
        probabilities = model.predict_proba(features)[0]

        return {
            "prediction": prediction,
            "class_name": iris.target_names[prediction],
            "probabilities": {
                class_name: float(prob)
                for class_name, prob in zip(iris.target_names, probabilities)
            },
        }

    finally:
        LATENCY.observe(time.time() - start)


@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )
