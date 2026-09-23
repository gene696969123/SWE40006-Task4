from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os
import socket

APP_NAME = os.getenv("APP_NAME", "SWE40006 Service")
APP_ENV = os.getenv("APP_ENV", "development")
OWNER = os.getenv("OWNER", "unset")

app = FastAPI(title=APP_NAME)


@app.get("/", response_class=HTMLResponse)
def index():
    return f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>{APP_NAME}</title></head>
<body style="font-family: sans-serif; margin: 3rem;">
  <h1>{APP_NAME}</h1>
  <p>Environment: {APP_ENV}</p>
  <p>Owner: {OWNER}</p>
  <p>Container host: {socket.gethostname()}</p>
  <p><a href="/health">/health</a></p>
</body>
</html>"""


@app.get("/health")
def health():
    return {
        "status": "ok",
        "app": APP_NAME,
        "environment": APP_ENV,
        "host": socket.gethostname(),
    }
