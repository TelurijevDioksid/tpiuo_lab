FROM python:3.9-alpine

WORKDIR /app

COPY lab_1_consumer/requirements.txt /app

RUN pip install -r requirements.txt

ADD lab_1_consumer/lab_1_consumer.py /app

CMD ["python", "lab_1_consumer.py"]