FROM python:3.10-slim-bullseye
WORKDIR /t500-aggregator
COPY . .

LABEL org.opencontainers.image.source=https://github.com/thearyadev/top500-aggregator
LABEL org.opencontainers.image.description="Docker image for t500 aggregator"
LABEL org.opencontainers.image.licenses=MIT

RUN pip install poetry==1.3.2
RUN poetry install --with=dev; exit 0

ENTRYPOINT poetry run hypercorn --bind 0.0.0.0:8000 server:app
