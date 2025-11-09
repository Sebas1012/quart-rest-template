FROM python:3.14.0-alpine3.22

RUN apk add --no-cache \
    gcc \
    musl-dev \
    python3-dev \
    postgresql-dev \
    libffi-dev \
    openssl-dev

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir poetry && poetry install --no-root

EXPOSE 5000

CMD ["poetry", "run", "hypercorn", "app:create_app", "-b", "0.0.0.0:8000"]
