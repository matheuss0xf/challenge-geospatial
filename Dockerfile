FROM python:3.12.6-slim

RUN apt-get update && apt-get install -y \
    gcc \
    make \
    libsqlite3-mod-spatialite \
    spatialite-bin \
    sqlite3 \
    curl \
    && rm -rf /var/lib/apt/lists/*

ENV SPATIALITE_PATH=/usr/lib/x86_64-linux-gnu/mod_spatialite.so

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-root

COPY . .

RUN chmod +x ./scritps/init_db_spatial.sh

CMD ["/bin/bash", "-c", "./scritps/init_db_spatial.sh && python main.py"]

