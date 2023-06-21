import asyncio
import pytest
from nats.aio.client import Client as NATS
from proto_files.task_pb2 import TaskMessage, ResultMessage
from worker import Worker


@pytest.mark.asyncio
async def test_worker_handle_task_addition():
    loop = asyncio.get_event_loop()
    nats_client = NATS()
    await nats_client.connect(servers=["nats://0.0.0.0:4222"], pending_size=65536)

    worker_id = "worker1"
    supported_operations = ["add"]
    worker = Worker(worker_id, supported_operations)
    await worker.connect_to_nats()

    task_id = "task1"
    task_message = TaskMessage(
        id=task_id,
        operation="add",
        operand1=10,
        operand2=5,
        timeout_seconds=3
    )
    result_message = ResultMessage()
    msg = NATS()
    msg.subject = 'result_queue'
    msg.data = task_message.SerializeToString()
    msg.reply = ''

    task = loop.create_task(worker.handle_task(msg))

    async def message_handler(msg):
        await result_message.ParseFromString(msg.data)
        assert result_message.id == task_id
        assert result_message.status == "DONE"
        assert result_message.description == "Task completed successfully."
        assert result_message.result == 15

    RESULT = await nats_client.subscribe("result_queue", cb=message_handler)

    await asyncio.sleep(1)
    await nats_client.unsubscribe(RESULT)
    await nats_client.flush()
    await asyncio.wait_for(task, timeout=5)

    await nats_client.close()


@pytest.mark.asyncio
async def test_worker_handle_task_subtract():
    loop = asyncio.get_event_loop()
    nats_client = NATS()
    await nats_client.connect(servers=["nats://0.0.0.0:4222"], pending_size=65536)

    worker_id = "worker1"
    supported_operations = ["add"]
    worker = Worker(worker_id, supported_operations)
    await worker.connect_to_nats()

    task_id = "task1"
    task_message = TaskMessage(
        id=task_id,
        operation="subtract",
        operand1=10,
        operand2=5,
        timeout_seconds=3
    )
    result_message = ResultMessage()
    msg = NATS()
    msg.subject = 'result_queue'
    msg.data = task_message.SerializeToString()
    msg.reply = ''

    task = loop.create_task(worker.handle_task(msg))

    async def message_handler(msg):
        await result_message.ParseFromString(msg.data)
        assert result_message.id == task_id
        assert result_message.status == "DONE"
        assert result_message.description == "Task completed successfully."
        assert result_message.result == 5

    RESULT = await nats_client.subscribe("result_queue", cb=message_handler)

    await asyncio.sleep(1)
    await nats_client.unsubscribe(RESULT)
    await asyncio.wait_for(task, timeout=5)

    await nats_client.close()


@pytest.mark.asyncio
async def test_worker_handle_task_multiply():
    loop = asyncio.get_event_loop()
    nats_client = NATS()
    await nats_client.connect(servers=["nats://0.0.0.0:4222"], pending_size=65536)

    worker_id = "worker1"
    supported_operations = ["add"]
    worker = Worker(worker_id, supported_operations)
    await worker.connect_to_nats()

    task_id = "task1"
    task_message = TaskMessage(
        id=task_id,
        operation="multiply",
        operand1=10,
        operand2=5,
        timeout_seconds=3
    )
    result_message = ResultMessage()
    msg = NATS()
    msg.subject = 'result_queue'
    msg.data = task_message.SerializeToString()
    msg.reply = ''

    task = loop.create_task(worker.handle_task(msg))

    async def message_handler(msg):
        await result_message.ParseFromString(msg.data)
        assert result_message.id == task_id
        assert result_message.status == "DONE"
        assert result_message.description == "Task completed successfully."
        assert result_message.result == 50

    RESULT = await nats_client.subscribe("result_queue", cb=message_handler)

    await asyncio.sleep(1)
    await nats_client.unsubscribe(RESULT)
    await asyncio.wait_for(task, timeout=5)

    await nats_client.close()

@pytest.mark.asyncio
async def test_worker_handle_task_divide():
    loop = asyncio.get_event_loop()
    nats_client = NATS()
    await nats_client.connect(servers=["nats://0.0.0.0:4222"], pending_size=65536)

    worker_id = "worker1"
    supported_operations = ["add"]
    worker = Worker(worker_id, supported_operations)
    await worker.connect_to_nats()

    task_id = "task1"
    task_message = TaskMessage(
        id=task_id,
        operation="divide",
        operand1=10,
        operand2=5,
        timeout_seconds=3
    )
    result_message = ResultMessage()
    msg = NATS()
    msg.subject = 'result_queue'
    msg.data = task_message.SerializeToString()
    msg.reply = ''

    task = loop.create_task(worker.handle_task(msg))

    async def message_handler(msg):
        await result_message.ParseFromString(msg.data)
        assert result_message.id == task_id
        assert result_message.status == "DONE"
        assert result_message.description == "Task completed successfully."
        assert result_message.result == 2

    RESULT = await nats_client.subscribe("result_queue", cb=message_handler)

    await asyncio.sleep(1)
    await nats_client.unsubscribe(RESULT)
    await asyncio.wait_for(task, timeout=5)

    await nats_client.close()


@pytest.mark.asyncio
async def test_worker_handle_task_divide_by_zero():
    loop = asyncio.get_event_loop()
    nats_client = NATS()
    await nats_client.connect(servers=["nats://0.0.0.0:4222"], pending_size=65536)

    worker_id = "worker1"
    supported_operations = ["add"]
    worker = Worker(worker_id, supported_operations)
    await worker.connect_to_nats()

    task_id = "task1"
    task_message = TaskMessage(
        id=task_id,
        operation="divide",
        operand1=10,
        operand2=0,
        timeout_seconds=3
    )
    result_message = ResultMessage()
    msg = NATS()
    msg.subject = 'result_queue'
    msg.data = task_message.SerializeToString()
    msg.reply = ''

    task = loop.create_task(worker.handle_task(msg))

    async def message_handler(msg):
        await result_message.ParseFromString(msg.data)
        assert result_message.id == task_id
        assert result_message.status == "FAILED"
        assert result_message.description == "Division by zero error."
        assert result_message.result == None

    RESULT = await nats_client.subscribe("result_queue", cb=message_handler)

    await asyncio.sleep(1)
    await nats_client.unsubscribe(RESULT)
    await asyncio.wait_for(task, timeout=5)

    await nats_client.close()

@pytest.mark.asyncio
async def test_worker_handle_with_unsupported_operands():
    loop = asyncio.get_event_loop()
    nats_client = NATS()
    await nats_client.connect(servers=["nats://0.0.0.0:4222"], pending_size=65536)

    worker_id = "worker1"
    supported_operations = ["add"]
    worker = Worker(worker_id, supported_operations)
    await worker.connect_to_nats()

    task_id = "task1"
    task_message = TaskMessage(
        id=task_id,
        operation="ABC",
        operand1=10,
        operand2=2,
        timeout_seconds=3
    )
    result_message = ResultMessage()
    msg = NATS()
    msg.subject = 'result_queue'
    msg.data = task_message.SerializeToString()
    msg.reply = ''

    task = loop.create_task(worker.handle_task(msg))

    async def message_handler(msg):
        await result_message.ParseFromString(msg.data)
        assert result_message.id == task_id
        assert result_message.status == "FAILED"
        assert result_message.description == "Unsupported operation for this worker."
        assert result_message.result == 0

    RESULT = await nats_client.subscribe("result_queue", cb=message_handler)

    await asyncio.sleep(1)
    await nats_client.unsubscribe(RESULT)
    await asyncio.wait_for(task, timeout=5)

    await nats_client.close()

