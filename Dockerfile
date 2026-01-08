FROM python:3.11-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends graphviz \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml ./
RUN pip install --no-cache-dir \
    fastapi \
    graphviz \
    pycparser \
    python-multipart \
    uvicorn \
    vsdx

COPY api ./api
COPY furohen ./furohen
COPY web ./web

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
