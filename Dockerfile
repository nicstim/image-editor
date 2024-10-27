FROM python:3.9

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY app/requirements.txt .


RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5050