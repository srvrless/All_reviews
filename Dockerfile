FROM python:3.10-slim
LABEL "By"='Hiko'
ENV FLASK_APP run.py


WORKDIR /app
ADD . /app

RUN apt-get update && apt-get -y install libpq-dev gcc && pip install psycopg2
COPY requirements.txt /cs_account/
RUN pip3 install -r requirements.txt
COPY . .

# gunicorn
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "run:create_app()","--reload"]