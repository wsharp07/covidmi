FROM python:3.7.7-slim

COPY requirements.txt /
COPY bin /bin
RUN pip3 install -r /requirements.txt

COPY app /app
WORKDIR /

ENTRYPOINT ["./bin/start.sh"]