FROM python:3.10-slim-bullseye
WORKDIR t500-aggregator
COPY . .

RUN pip install poetry==1.3.2
RUN poetry install; exit 0
#ENTRYPOINT poetry run uvicorn server:app --host 0.0.0.0
RUN gunicorn -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 server:app
#RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y