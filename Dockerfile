FROM python:3.11.4-slim-buster

WORKDIR /

# set environment variables to default value, if coming in from env then below default values will not override these ARGs
ARG APP_ENV=prod
ARG APP_PORT=80

# set env variables
# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1


# Install Poetry
RUN pip install "poetry==1.6.1"
RUN poetry config virtualenvs.create false 

# Copy poetry.lock* in case it doesn't exist in the repo
# Also, doing this in this way will cache installing dependencies unless changes to pyproject.toml
COPY ./pyproject.toml ./poetry.lock* /

# Allow installing dev dependencies to run tests when in dev environment
RUN if [ "$APP_ENV" == "dev" ] ; then \
    poetry install --no-root ; \
    else \
    poetry install --no-root --no-dev ; \
    fi


# copy project
COPY . .
ENV PYTHONPATH=/


RUN chmod +x ./scripts/startup.sh
RUN chmod +x ./scripts/prestart.sh
RUN chmod +x ./scripts/db/db_check.py


HEALTHCHECK CMD curl --fail http://0.0.0.0:${APP_PORT}/urs/health/ || exit 1

EXPOSE ${APP_PORT}


CMD ["./scripts/startup.sh"]