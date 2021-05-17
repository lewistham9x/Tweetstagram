FROM python:3.8-slim-buster

WORKDIR /code

COPY requirements.txt .

RUN apt-get clean -y
RUN apt-get update -y

RUN apt-get install -y git

RUN pip3 install -r requirements.txt

ENV TZ=Asia/Singapore
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get install -y tzdata

RUN dpkg-reconfigure -f noninteractive tzdata

EXPOSE 5000

RUN pip3 install gunicorn

COPY . .


RUN chmod +x ./gunicorn.sh

CMD [ "./gunicorn.sh"]

