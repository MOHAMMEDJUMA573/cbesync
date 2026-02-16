#use and official python image
FROM python:3.12-slim-bookworm

# Create a virtual environment
RUN python -m venv /opt/venv

# Set the virtual environment as the current location
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PATH=/opt/venv/bin:$PATH

# Upgrade pip
RUN pip install --upgrade pip

#found in alot python docker files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=.
ENV CSYNCSET_IN_DOCKER=true


# Install os dependencies for our mini vm
RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        # for postgres
        libpq-dev \
        # for Pillow
        libjpeg-dev \
        # for CairoSVG
        libcairo2-dev \
        # build tools
        gcc \
        build-essential; \
    apt-get clean; \
    rm -rf /var/lib/apt/lists/*

# Create the mini vm's code directory
RUN mkdir -p /code
RUN mkdir -p /local

# Set the working directory to that same code directory
WORKDIR /code


# Copy the requirements file into the container
COPY requirements.txt /tmp/requirements.txt

# Install the Python project requirements
RUN pip install -r /tmp/requirements.txt

# copy the project code into the container's working directory
COPY ./src /code
#COPY ./src/staticfiles /code/staticfiles


#variable required during buildtime
ARG DJANGO_DEBUG=0
ENV DJANGO_DEBUG=${DJANGO_DEBUG}

# set the Django default project name
ARG PROJ_NAME="project"

# create a bash script to run the Django project
# this script will execute at runtime when
# the container starts and the database is available
RUN printf "#!/bin/bash\n" > paracord_runner.sh && \
    printf "set -e\n\n" >> paracord_runner.sh && \
    printf "WORKERS=${GUNICORN_WORKERS:-2}" >> paracord_runner.sh && \
    printf "PORT=\"\${PORT:-8080}\"\n\n" >> paracord_runner.sh && \
    printf "python manage.py collectstatic --noinput\n" >> paracord_runner.sh && \
    # printf "python manage.py migrate --noinput\n" >> paracord_runner.sh && \
    printf "exec gunicorn project.wsgi --workers 2 --bind 0.0.0.0:8080 \n" >> paracord_runner.sh
# make the bash script executable
RUN chmod +x ./paracord_runner.sh

# Clean up apt cache to reduce image size
RUN apt-get remove --purge -y \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

    # Run the Django project via the runtime script
# when the container starts
CMD ./paracord_runner.sh