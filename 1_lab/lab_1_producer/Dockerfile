FROM python:3.9-alpine

WORKDIR /app

COPY lab_1_producer/requirements.txt /app

RUN pip install -r requirements.txt

ADD lab_1_producer/lab_1_producer.py /app

CMD ["python", "lab_1_producer.py"]