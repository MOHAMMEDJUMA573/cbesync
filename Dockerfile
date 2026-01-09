#use and official python image
FROM python:3.14.2-slim-bookworm

# Create a virtual environment
RUN python -m venv /opt/venv

# Set the virtual environment as the current location
ENV PATH=/opt/venv/bin:$PATH

# Upgrade pip
RUN pip install --upgrade pip

#found in alot python docker files
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH .
ENV CSYNCSET_IN_DOCKER true


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
    pip install \
        poetry==1.4.2 \
        virtualenvwrapper; \
    apt-get clean; \
    rm -rf /var/lib/apt/lists/*

# Create the mini vm's code directory
RUN mkdir -p /code

# Set the working directory to that same code directory
WORKDIR /code


# Copy the requirements file into the container
COPY requirements.txt /tmp/requirements.txt

# copy the project code into the container's working directory
COPY ./src /code
#COPY ./local /code #BET ONLY WORKS LOCALLY

# Install the Python project requirements
RUN pip install -r /tmp/requirements.txt

#variable required during buildtime
ARG DJANGO_SECRET_KEY
ENV DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}

ARG DJANGO_DEBUG=0
ENV DJANGO_DEBUG=${DJANGO_DEBUG}

ARG DATABASE_URL
ENV DATABASE_URL=${DATABASE_URL}

ARG CLOUDFLARE_R2_BUCKET
ENV CLOUDFLARE_R2_BUCKET=${CLOUDFLARE_R2_BUCKET}

ARG CLOUDFLARE_R2_ACCESS_KEY
ENV CLOUDFLARE_R2_ACCESS_KEY=${CLOUDFLARE_R2_ACCESS_KEY}

ARG CLOUDFLARE_R2_SECRET_KEY
ENV CLOUDFLARE_R2_SECRET_KEY=${CLOUDFLARE_R2_SECRET_KEY}

ARG CLOUDFLARE_R2_BUCKET_ENDPOINT
ENV CLOUDFLARE_R2_BUCKET_ENDPOINT=${CLOUDFLARE_R2_BUCKET_ENDPOINT}

# set the Django default project name
ARG PROJ_NAME="CbeSync"

#Expose the django port
EXPOSE 8000

#copy and install python dependencies
COPY ["poetry.lock", "pyproject.toml","./"]
RUN poetry install --no-root

#copy project files
COPY ["README.md","Makefile","./"]

#Expose django development server port
EXPOSE 8000

#set up the entry point
COPY scripts/entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh

ENTRYPOINT [ "entrypoint.sh" ]
