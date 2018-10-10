FROM python:2.7

RUN mkdir  /mf
RUN mkdir /input
RUN mkdir /input/HETRA
RUN mkdir /input/EHR
RUN mkdir /output

ARG ACCESS_KEY
ARG SECRET_KEY

ENV AWS_ACCESS_KEY_ID=$ACCESS_KEY
ENV AWS_SECRET_ACCESS_KEY=$SECRET_KEY

COPY . /mf

RUN pip install -r /mf/requirements.txt