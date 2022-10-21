# pythonのバージョンは任意
FROM python:3.8

WORKDIR /usr/src/app
ENV FLASK_APP=app

COPY /src/requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
