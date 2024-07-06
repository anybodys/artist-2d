# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.10-slim as base

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True


FROM base AS python-deps

# Install pipenv and compilation dependencies
RUN pip install pipenv
RUN apt-get update && apt-get install -y --no-install-recommends gcc

# Install python dependencies in /.venv
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy


FROM base AS runtime

# Copy virtual env from python-deps stage
COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

# Create and switch to a new user
RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /home/appuser/entrypoint.sh
RUN chmod a+x /home/appuser/entrypoint.sh

# Install application into container
COPY . ./

# run entrypoint.sh
ENTRYPOINT ["/home/appuser/entrypoint.sh"]

ENV PORT=8000

# Sets the url path prefix.
#ENV SCRIPT_NAME=/api
