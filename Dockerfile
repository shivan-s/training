FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONNUNBUFFERED 1

WORKDIR /code

# hadolint ignore=DL3013
RUN pip install --no-cache-dir -U pip-tools pip
COPY pyproject.toml /code/

# hadolint ignore=DL3042
RUN pip-compile --output-file=requirements.txt pyproject.toml && \
pip-compile --extra=dev --output-file=dev-requirements.txt pyproject.toml && \
pip-sync dev-requirements.txt requirements.txt

COPY entrypoint.sh manage.py /code/
RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["sh", "./entrypoint.sh"]

EXPOSE 8000
