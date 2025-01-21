FROM python:3.12.8-alpine3.21
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt
COPY main.py .
CMD ["python3", "./main.py"]
