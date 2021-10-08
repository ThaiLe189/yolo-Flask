FROM python:3.6

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential

RUN pip install -r requirements.txt

COPY app/
WORKDIR /app
# ADD . /app
# RUN pip install -r requirements.txt

# EXPOSE 5000

ENV PORT 8080

# CMD ["python", "restapi.py", "--port=5000"]
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app