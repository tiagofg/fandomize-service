FROM python:3.13-alpine AS builder
WORKDIR /app

RUN apk add --no-cache build-base

COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip && \
    pip wheel --no-cache-dir -r requirements.txt -w /wheels

FROM python:3.13-alpine
WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PORT=8000 \
    LOG_LEVEL=INFO

COPY --from=builder /wheels /wheels
COPY requirements.txt .
RUN pip install --no-cache-dir --no-index --find-links /wheels -r requirements.txt && \
    rm -rf /wheels

COPY app ./app
COPY prompts ./prompts
COPY logging.yaml .

RUN adduser -D -H appuser && chown -R appuser /app
USER appuser

EXPOSE ${PORT}
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--timeout-keep-alive", "180"]
