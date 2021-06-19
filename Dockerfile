FROM python:3.7.9-buster

ENV PYTHONUNBUFFERED 1
RUN mkdir -p /home/project/app
WORKDIR /home/project/app

RUN apt-get clean && apt-get update && apt-get install -y locales
RUN sed -i -e \
  's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen \
   && locale-gen

ENV LANG ru_RU.UTF-8
ENV LANGUAGE ru_RU:ru
ENV LC_LANG ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8

COPY requirements.txt /home/project/app
RUN pip install --no-cache-dir -r requirements.txt
