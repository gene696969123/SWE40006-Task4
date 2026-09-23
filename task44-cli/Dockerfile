FROM python:3.12-slim

RUN useradd --create-home --uid 1001 appuser

WORKDIR /app

COPY analyse.py .

RUN mkdir -p /data && chown appuser:appuser /data

USER appuser

VOLUME ["/data"]

ENTRYPOINT ["python", "analyse.py"]
CMD ["--input", "/data/readings.csv", "--output", "/data/summary.txt"]
