# ---------- Fase de build ----------
FROM python:3.13-alpine AS builder
WORKDIR /app

# Copiamos só o requirements para aproveitar o cache
COPY requirements.txt .

# Gera wheels em /wheels (diretório certo!)
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip && \
    pip wheel --no-cache-dir -r requirements.txt -w /wheels

# ---------- Fase final ----------
FROM python:3.13-alpine
WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    PORT=8000 \
    LOG_LEVEL=INFO

# Copia wheels gerados e instala rapidamente sem baixar nada
COPY --from=builder /wheels /wheels
COPY requirements.txt .
RUN pip install --no-cache-dir --no-index --find-links /wheels -r requirements.txt && \
    rm -rf /wheels

# Copia o código da aplicação
COPY . .

EXPOSE ${PORT}
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
