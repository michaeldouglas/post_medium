FROM python:3.13-slim

# Dependências do sistema
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Instala uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# PATH CORRETO do uv
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

# Copia arquivos de dependência primeiro (cache)
COPY pyproject.toml ./
# COPY uv.lock ./  # se existir

# Instala dependências
RUN uv pip install --system .

# Copia o código
COPY . .

EXPOSE 8000

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]