FROM python:3.10-alpine
FROM ubuntu:20.04

LABEL "By"='Hiko'
# set environment variables
ENV FLASK_APP run.py
ENV DEBUG True

WORKDIR C:/Users/fedor/PycharmProjects/MyWorks/all_reviews

COPY requirements.txt .


# install python dependencies
RUN apt-get update && apt-get -y install sudo
RUN sudo apt-get -y install libpq-dev python3-dev && apt-get -y install python3-pip
RUN #pip3 install psycopg2
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY . .

# gunicorn
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "run:create_app()"]