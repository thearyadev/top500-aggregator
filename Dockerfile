FROM python:3.10-slim-bullseye
WORKDIR /t500-aggregator
COPY . .

RUN pip install poetry==1.3.2
RUN poetry install --with=dev; exit 0
RUN poetry run pytest
ENTRYPOINT poetry run hypercorn --bind 0.0.0.0:8000 server:app
