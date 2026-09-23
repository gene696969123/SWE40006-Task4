FROM python:3.12-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


FROM python:3.12-slim

RUN useradd --create-home --uid 1001 appuser

WORKDIR /app

COPY --from=builder /install /usr/local
COPY main.py .

USER appuser

ENV APP_NAME="SWE40006 Task 4.3" \
    APP_ENV="production" \
    OWNER="Jin Shang"

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
