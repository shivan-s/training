FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONNUNBUFFERED 1

WORKDIR /code

# install C dependences
# for libsass (bulma css frontend)
# hadolint ignore=DL3008
RUN apt-get update && \
  apt-get -y --no-install-recommends install build-essential && \
  rm -rf /var/lib/apt/lists/*

# install python dependences
# install pip-tools and pip
# hadolint ignore=DL3013
RUN pip install --no-cache-dir -U pip-tools pip
COPY requirements/requirements.in /code/

# hadolint ignore=DL3042
RUN pip-compile -o requirements.txt requirements.in && \
  pip install --no-cache-dir --no-deps -r requirements.txt

# run entry scripts
COPY . .
ENTRYPOINT ["sh", "-c", "/code/docker-entrypoint.sh"]
