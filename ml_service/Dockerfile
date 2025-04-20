FROM python:3.12-slim

WORKDIR /ml_service
COPY . .

RUN pip install --upgrade pip
RUN pip install -r /common/requirements.txt

CMD ["python", "worker.py"]