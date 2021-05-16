FROM python:3.6-slim-buster

WORKDIR /code

COPY requirements.txt .

RUN apt-get update -y

RUN apt-get install -y git

RUN pip3 install -r requirements.txt

ENV TZ=Asia/Singapore
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get install -y tzdata

RUN dpkg-reconfigure -f noninteractive tzdata

COPY . .

EXPOSE 5000

CMD [ "python3","-u","server.py"]

