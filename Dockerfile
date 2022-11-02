FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONNUNBUFFERED 1

WORKDIR /code

# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get -y --no-install-recommends install build-essential && \
    rm -rf /var/lib/apt/lists/*

# hadolint ignore=DL3013
RUN pip install --no-cache-dir -U pip-tools pip
COPY requirements.in dev-requirements.in /code/

# hadolint ignore=DL3042
RUN pip-compile -o requirements.txt requirements.in && \
    pip-compile -o dev-requirements.txt dev-requirements.in && \
    pip-sync dev-requirements.txt requirements.txt \
              --pip-args "--no-cache-dir --no-deps"

COPY entrypoint.sh manage.py /code/
RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["sh", "./entrypoint.sh"]

EXPOSE 8000
