# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.11.9
FROM python:${PYTHON_VERSION} as base

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y supervisor && rm -rf /var/lib/apt/lists/*

COPY supervisord.conf /etc/supervisor/supervisord.conf

COPY . .

EXPOSE 8000

EXPOSE 7860

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]