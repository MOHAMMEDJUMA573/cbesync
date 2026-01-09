#use and official python image
FROM python:3.14.2-slim-bookworm

#set working directory in the container
WORKDIR /opt/project

#found in alot python docker files
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH .
ENV CSYNCSET_IN_DOCKER true

