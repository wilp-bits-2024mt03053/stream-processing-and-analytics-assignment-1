FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY consumer.py /app/consumer.py

ENV PYTHONUNBUFFERED=1

CMD ["python", "-u", "consumer.py"]



