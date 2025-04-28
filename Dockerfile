# --- estágio de build --------------------------------------------------------
FROM python:3.13-alpine AS builder
WORKDIR /app

# Copie só o requirements para aproveitar o cache
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip && \
    pip wheel --no-cache-dir -r requirements.txt

# --- estágio final -----------------------------------------------------------
FROM python:3.13-alpine
WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    LOG_LEVEL=INFO \
    PORT=8000

# Copie pacotes já “wheelados” e instale rapidinho
COPY --from=builder /root/.cache/pip /root/.cache/pip
RUN pip install --no-cache-dir /root/.cache/pip/*.whl

# Copie seu código
COPY . .

# Exponha a porta que o Koyeb detectará
EXPOSE ${PORT}

# Comando de arranque --> saída vai para stdout
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
