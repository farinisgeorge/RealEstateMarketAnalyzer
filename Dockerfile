FROM python:3.10

# WORKDIR /api/zillowDataCollector/baseCollector

RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD [ "python3", "api/zillowDataCollector/baseCollector.py"]