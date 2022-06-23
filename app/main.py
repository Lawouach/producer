import time
from typing import Dict

from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor  # type: ignore
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(root_path="/producer")
FastAPIInstrumentor.instrument_app(app)
Instrumentator().instrument(app).expose(app)

latency = 0.0


def get_latency() -> float:
    return latency


def set_latency(value: float) -> None:
    global latency
    latency = value


@app.get("/producer")
def index() -> Dict[str, str]:
    if latency > 0:
        time.sleep(latency)
    return {"Hello": "The World"}


@app.get("/producer/health")
def health() -> str:
    return ""


@app.get("/producer/inject/latency")
def inject_latency(value: float = 0) -> str:
    set_latency(value)
    return ""
