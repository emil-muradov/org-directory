FROM python:3.13-slim

ENV PYTHONPATH "${PYTHONPATH}:/app/src"

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -ms /bin/sh -u 1001 app

WORKDIR /app

RUN mkdir src

COPY pyproject.toml README.md .

RUN pip install --upgrade pip && pip install .

COPY --chown=app:app . /app

USER app

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "3001", "--reload"]
