FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir .

EXPOSE 3001

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "3001"]
