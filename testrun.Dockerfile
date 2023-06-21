FROM python:3.9

WORKDIR /test

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /test/src

RUN wget https://github.com/nats-io/nats-server/releases/download/v2.6.0/nats-server-v2.6.0-linux-amd64.zip && \
    unzip nats-server-v2.6.0-linux-amd64.zip && \
    rm nats-server-v2.6.0-linux-amd64.zip

EXPOSE 4222

CMD sh -c './nats-server-v2.6.0-linux-amd64/nats-server & python -m pytest -vv'

