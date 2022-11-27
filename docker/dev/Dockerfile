FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONNUNBUFFERED 1

WORKDIR /code

# install C dependences
# for libsass and pygraphviz
# hadolint ignore=DL3008
RUN apt-get update && \
  apt-get -y --no-install-recommends install build-essential \
  graphviz \
  graphviz-dev && \
  rm -rf /var/lib/apt/lists/*

# install pip-tools and pip
# hadolint ignore=DL3013
RUN pip install --no-cache-dir -U pip-tools pip
COPY requirements/requirements.in requirements/dev-requirements.in /code/

# install python dependences
# hadolint ignore=DL3042
RUN pip-compile -o requirements.txt requirements.in && \
  pip-compile -o dev-requirements.txt dev-requirements.in && \
  pip install --no-cache-dir --no-deps -r dev-requirements.txt

# expose port
EXPOSE 8000
