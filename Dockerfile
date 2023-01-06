FROM python:3.10-alpine
LABEL "Mars"='SpaceX'
LABEL "By"='Hiko'
# set environment variables
ENV FLASK_APP run.py
ENV DEBUG True

WORKDIR C:/Users/fedor/PycharmProjects/MyWorks/all_reviews

COPY requirements.txt .


# install python dependencies
RUN apk update && apk upgrade && apk add bash
RUN pip3 install -r requirements.txt


COPY . .

RUN flask db init
RUN flask db migrate
RUN flask db upgrade

# gunicorn
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "run:app"]