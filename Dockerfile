FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -ms /bin/sh -u 1001 app

RUN mkdir src
COPY pyproject.toml README.md .
RUN pip install --no-cache-dir .

COPY --chown=app:app . /app

USER app

EXPOSE 3001

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "3001"]
