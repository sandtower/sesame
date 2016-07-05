FROM ubuntu
MAINTAINER tangbo
RUN apt-get update \
    && apt-get install -y python \
    && apt-get install -y python-pip python-dev build-essential \
    && apt-get install -y zlib1g-dev \
    && apt-get install -y libxml2-dev \
    && apt-get install -y libxslt1-dev 

RUN pip install --upgrade pip \
    && pip install --upgrade virtualenv \
    && pip install cython \
    && pip install  tornado \
    && pip install lxml \
    && pip install Pandas \
    && pip install tushare

#ADD ../../sesame_bak /project/sesame

#CMD echo hello world
