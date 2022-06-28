from datetime import datetime
import secrets
import time
from typing import Dict

from fastapi import FastAPI, Response
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor  # type: ignore
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.responses import JSONResponse


app = FastAPI()
FastAPIInstrumentor.instrument_app(app)
Instrumentator().instrument(app).expose(app)

latency = 0.0
error_code = 0


def get_latency() -> float:
    return latency


def set_latency(value: float) -> None:
    global latency
    latency = value


def get_error() -> float:
    return error_code


def set_error(code: int) -> None:
    global error_code
    error_code = code


@app.get("/producer")
def index() -> JSONResponse:
    if latency > 0:
        time.sleep(latency)

    if error_code > 0:
        return JSONResponse(content="", status_code=error_code)

    return JSONResponse(
        {"secret": secrets.token_hex(), "ts": datetime.utcnow().isoformat()},
    )


@app.get("/health")
def health() -> str:
    return ""


@app.get("/producer/inject/latency")
def inject_latency(value: float = 0) -> str:
    set_latency(value)
    return ""


@app.get("/producer/inject/error")
def inject_error(code: int = 0) -> str:
    set_error(code)
    return ""
