import asyncio
import random
import time
from nats.aio.client import Client as NATS
from proto_files.task_pb2 import TaskMessage, ResultMessage

class Worker:
    def __init__(self, worker_id, supported_operations):
        self.worker_id = worker_id
        self.supported_operations = supported_operations
        self.nats_client = NATS()
        self.is_available = True
        self.task_status={}

    async def connect_to_nats(self):
        await self.nats_client.connect(servers=["nats://0.0.0.0:4222"])

    async def handle_task(self, msg):
        task = TaskMessage()
        task.ParseFromString(msg.data)
        print("@@@@@@@@@@@@@@@@@@@@@@@-Worker Subscribe From Controller-@@@@@@@@@@@@@@@@@@@@@@@")
        print("Task_ID",task.id)
        print("Task Operation",task.operation)
        print("Operand_1",task.operand1)
        print("Operand_2",task.operand2)
        print("TimeOut",task.timeout_seconds)
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

        if task.operation in self.supported_operations:
            print(f"Worker {self.worker_id} received task: {task.id}")
            self.task_status[task.id] = "RUNNING"

            await asyncio.sleep(task.timeout_seconds)

            if task.timeout_seconds > 5:
                if task.id in self.task_status and self.task_status[task.id] == "RUNNING":
                    result_message = ResultMessage(
                        id=task.id,
                        status="RUNNING",
                        description="Task running.",
                        result=0
                    )
                    await self.nats_client.publish("result_queue", result_message.SerializeToString())
                    return

            if task.operation == "add":
                result = task.operand1 + task.operand2
                print(result)
            elif task.operation == "subtract":
                result = task.operand1 - task.operand2
                print(result)
            elif task.operation == "multiply":
                result = task.operand1 * task.operand2
                print(result)
            elif task.operation == "divide":
                if task.operand1 == 0 or task.operand2 == 0:
                    result_message = ResultMessage(
                        id=task.id,
                        status="FAILED",
                        description="Division by zero error.",
                        result=None
                    )
                    await self.nats_client.publish("result_queue", result_message.SerializeToString())
                    return
                else:
                    result = task.operand1 // task.operand2
                    print(result)

            result_message = ResultMessage(
                id=task.id,
                status="DONE",
                description="Task completed successfully.",
                result=result
            )
        else:
            result_message = ResultMessage(
                id=task.id,
                status="FAILED",
                description="Unsupported operation for this worker.",
                result=0
            )
        print("----------------------->", result_message.SerializeToString())
        await self.nats_client.publish("result_queue", result_message.SerializeToString())
        return result_message.SerializeToString()

    async def run(self):
        await self.connect_to_nats()
        await self.nats_client.subscribe("task_queue", cb=self.handle_task)

        while True:
            await asyncio.sleep(5)


if __name__ == "__main__":
    worker_id = ["worker"]
    supported_operations = ["add", "subtract", "multiply", "divide"]

    worker = Worker(worker_id, supported_operations)
    asyncio.run(worker.run())
