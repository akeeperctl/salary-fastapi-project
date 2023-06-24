FROM python:3.11 as depedencies-stage
LABEL authors="Akeeper"

# Setup the temp directory to collect all depedencies
WORKDIR /tmp

# Run pip to install poetry at depedencies-stage
RUN pip install poetry

# Copy files to current WORKDIR (. defines current dir)
COPY pyproject.toml /tmp
COPY poetry.lock /tmp

# Run poetry to export all depedencies to requirements.txt
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.11 as latest-stage

WORKDIR /shiftproject_app

COPY --from=depedencies-stage /tmp/requirements.txt /shiftproject_app

RUN pip install --no-cache-dir --upgrade -r /shiftproject_app/requirements.txt

# Copy local directories to the current local directory of our docker image (/app)
COPY . /shiftproject_app

#CMD alembic upgrade head
CMD gunicorn src.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Install node packages, install serve, build the app, and remove dependencies at the end
#RUN npm install \
#    && npm install -g serve \
#    && npm run build \
#    && rm -fr node_modules

EXPOSE 8000

# Start the app using serve command
#CMD [ "serve", "-s", "build" ]