# pull official base image
FROM python:3.7
ADD . /app
# set work directory
WORKDIR /app
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# install dependencies
RUN pip install --upgrade pip

RUN pip install -r requirements.txt
# copy project
EXPOSE 8000