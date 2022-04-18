FROM python:3.7

ENV PYTHONUNBUFFERED=1

RUN mkdir ai2021mis

COPY . /ai2021mis

WORKDIR /ai2021mis

RUN pip3 install -r requirements2.txt
RUN pip3 install opencv-python-headless