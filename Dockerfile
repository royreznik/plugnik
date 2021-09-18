FROM python:3.9-slim as python-base

ENV PYTHONUNBUFFERED=1 \
PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.1.7 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"


ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

FROM python-base as builder-base
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
     curl \
    build-essential

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -

WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

RUN poetry install --no-dev

FROM python-base as production
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
RUN mkdir /tmp/plugins/
RUN echo "<plugins></plugins>" > /updatePlugins.xml
RUN mkdir -p /app/settings/
RUN echo "{}" > /app/settings/plugin_manager.json

COPY server/ /app/server/

WORKDIR /app/

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "80"]