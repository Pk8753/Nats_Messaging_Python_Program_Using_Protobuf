import asyncio
import pytest
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout

@pytest.mark.asyncio
async def test_nats_publish_subscribe():
    nc = NATS()
    await nc.connect(servers=["nats://0.0.0.0:4222"])

    received_messages = []

    async def message_handler(msg):
        subject = msg.subject
        data = msg.data.decode()
        received_messages.append(data)

    await nc.subscribe("test_subject", cb=message_handler)

    await nc.publish("test_subject", b'Hello, NATS!')
    await asyncio.sleep(1)  # Wait for message to be received

    await nc.close()

    assert len(received_messages) == 1
    assert received_messages[0] == 'Hello, NATS!'


@pytest.mark.asyncio
async def test_nats_request_reply():
    nc = NATS()
    await nc.connect(servers=["nats://0.0.0.0:4222"])

    received_reply = None

    async def request_handler(msg):
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        await nc.publish(reply, f'Reply to {data}'.encode())

    await nc.subscribe("test_subject", cb=request_handler)

    msg = await nc.request("test_subject", b'Hello, NATS!', timeout=1)
    received_reply = msg.data.decode()

    await nc.close()

    assert received_reply == 'Reply to Hello, NATS!'


@pytest.mark.asyncio
async def test_nats_unsubscribe():
    nc = NATS()
    await nc.connect(servers=["nats://0.0.0.0:4222"])
    received_messages = []
    async def message_handler(msg):
        subject = msg.subject
        data = msg.data.decode()
        received_messages.append(data)

    pankaj = await nc.subscribe("test_subject", cb=message_handler)
    await nc.unsubscribe(pankaj)

    await nc.publish("test_subject", b'Hello, NATS!')
    await asyncio.sleep(1)

    await nc.close()
    assert len(received_messages) == 0


@pytest.mark.asyncio
async def test_nats_connection():
    nc = NATS()
    await nc.connect(servers=["nats://0.0.0.0:4222"])
    assert nc.is_connected
    print("NATS server is connected : {}".format(nc.is_connected))
    await nc.close()
    assert not nc.is_connected
    print("NATS server is disconnected : {}".format(not nc.is_connected))


@pytest.mark.asyncio
async def test_nats_connection_closed_exception():
    nc = NATS()
    await nc.connect(servers=["nats://0.0.0.0:4222"])
    await nc.close()
    with pytest.raises(ErrConnectionClosed):
        await nc.publish("test_subject", b'Hello, NATS!')

@pytest.mark.asyncio
async def test_nats_timeout_exception():
    nc = NATS()
    await nc.connect(servers=["nats://0.0.0.0:4222"])
    with pytest.raises(ErrTimeout):
        await nc.request("nonexistent_subject", b'Hello, NATS!', timeout=1)

    await nc.close()
