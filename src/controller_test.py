import asyncio
import pytest
from unittest.mock import patch, Mock
from nats.aio.client import Client as NATS
from src.controller import Controller
from proto_files.task_pb2 import TaskMessage, ResultMessage

controller = Controller()


@patch.object(NATS, 'connect')
def test_controller_connect_to_nats(mock_connect):
    asyncio.run(controller.connect_to_nats())
    mock_connect.assert_called_once_with(servers=["nats://0.0.0.0:4222"], pending_size=65536)

@pytest.mark.asyncio
def test_controller_create_task():
    asyncio.run(controller.connect_to_nats())
    operation = "add"
    operand1 = 5
    operand2 = 10
    timeout_seconds = 2

    controller.tasks = {}
    asyncio.run(controller.create_task(operation, operand1, operand2, timeout_seconds))

    task_id = list(controller.tasks.keys())[0]
    task = controller.tasks[task_id]
    print("#############################################", controller.tasks[task_id])
    # Assert the task properties
    assert task["status"] == "QUEUED"
    assert task["description"] == ""
    assert task["result"] is None


@pytest.mark.asyncio
async def test_controller_handle_result_with_complete_task():
    msg = NATS()
    msg.subject = 'result_queue'
    msg.data = b'\n$f68a2ddc-ded5-4221-b84c-5df0fcb853f1\x12\x04DONE\x1a\x1cTask completed successfully. \xc0\xee\x9a\x02'
    msg.reply = ''

    mock_result = ResultMessage()
    mock_result.ParseFromString(msg.data)

    sample_id = 'f68a2ddc-ded5-4221-b84c-5df0fcb853f1'
    sample_status = "DONE"
    sample_description = "Task completed successfully."
    sample_result = 4634432

    assert mock_result.id == sample_id
    assert mock_result.status == sample_status
    assert mock_result.description == sample_description
    assert mock_result.result == sample_result


@pytest.mark.asyncio
async def test_controller_handle_result_with_failed_task():
    msg = NATS()
    msg.subject = 'result_queue'
    msg.data = b'\n$2e07d79d-c9e8-4580-b7c6-95d4fc0b44b6\x12\x06FAILED\x1a&Unsupported operation for this worker.'
    msg.reply = ''

    mock_result = ResultMessage()
    mock_result.ParseFromString(msg.data)

    sample_id = '2e07d79d-c9e8-4580-b7c6-95d4fc0b44b6'
    sample_status = "FAILED"
    sample_description = "Unsupported operation for this worker."

    assert mock_result.id == sample_id
    assert mock_result.status == sample_status
    assert mock_result.description == sample_description


@pytest.mark.asyncio
async def test_controller_handle_result_with_queue_task():
    msg = NATS()
    msg.subject = 'result_queue'
    msg.data = b'\n%q33a4ddc-ded5-4221-b84c-5df0fcb653f33\x12\x06QUEUED\x1a\x0eTask in Queue.'
    msg.reply = ''

    mock_result = ResultMessage()
    mock_result.ParseFromString(msg.data)

    sample_id = 'q33a4ddc-ded5-4221-b84c-5df0fcb653f33'
    sample_status = "QUEUED"
    sample_description = "Task in Queue."

    assert mock_result.id == sample_id
    assert mock_result.status == sample_status
    assert mock_result.description == sample_description



@pytest.mark.asyncio
async def test_controller_handle_result_with_running_task():
    msg = NATS()
    msg.subject = 'result_queue'
    msg.data = b'\n%r23a4ddc-ded5-4221-b84c-5df0fcb853f33\x12\x07RUNNING\x1a\rTask running.'
    msg.reply = ''

    mock_result = ResultMessage()
    mock_result.ParseFromString(msg.data)

    sample_id = 'r23a4ddc-ded5-4221-b84c-5df0fcb853f33'
    sample_status = "RUNNING"
    sample_description = "Task running."

    assert mock_result.id == sample_id
    assert mock_result.status == sample_status
    assert mock_result.description == sample_description





if __name__ == '__main__':
    pytest.main([__file__])
