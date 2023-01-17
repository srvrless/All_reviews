FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt /app
RUN pip install --upgrade pip &&  python -m pip install -r requirements.txt

COPY . /app

EXPOSE 8080

CMD ['python','run.py']