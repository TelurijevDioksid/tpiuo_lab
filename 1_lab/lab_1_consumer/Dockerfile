FROM python:3.9-alpine

WORKDIR /app

ADD lab_1_consumer/lab_1_consumer.py /app

RUN pip install azure-eventhub

CMD ["python", "lab_1_consumer.py"]