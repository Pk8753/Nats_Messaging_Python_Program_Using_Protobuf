import asyncio
import uuid
import time
import random
from nats.aio.client import Client as NATS
from proto_files.task_pb2 import TaskMessage, ResultMessage


class Controller:
    def __init__(self):
        self.tasks = {}
        self.worker_nodes = {"worker1": True,
                             "worker2": True,
                             "worker3": True}
        self.nats_client = NATS()

    async def connect_to_nats(self):
        # await self.nats_client.connect(servers=["nats://0.0.0.0:4222"])
        options = {
            "servers": ["nats://0.0.0.0:4222"],
            "pending_size": 65536  # Set an appropriate pending size value
        }
        await self.nats_client.connect(**options)

    async def handle_result(self, msg):
        print("->", type(msg))
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", msg.data)
        result = ResultMessage()
        result.ParseFromString(msg.data)
        task_id = result.id
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%",task_id)
        if task_id in self.tasks:
            task = self.tasks[task_id]
            task["status"] = result.status
            task["description"] = result.description
            task["result"] = result.result

            if task["status"] == "DONE":
                print("@@@@@@@@@@@@@@@@@@@@@@@-Controller Subscribe From Worker-@@@@@@@@@@@@@@@@@@@@@@@")
                print(f"Task {task_id} completed successfully.")
                print("Task_Description", task['description'])
                print("Task_Result", task['result'])
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            else:
                print(f"Task {task_id} is {task['status']}. Reason: {task['description']}")

            del self.tasks[task_id]

    async def publish_task(self, task):
        await self.nats_client.publish("task_queue", task.SerializeToString())

    async def create_task(self, operation, operand1, operand2, timeout_seconds):
        task_id = str(uuid.uuid4())
        task = TaskMessage(
            id=task_id,
            operation=operation,
            operand1=operand1,
            operand2=operand2,
            timeout_seconds=timeout_seconds
        )

        self.tasks[task_id] = {
            "status": "QUEUED",
            "description": "",
            "result": None
        }

        await self.publish_task(task)

    async def run(self):
        await self.connect_to_nats()
        await self.nats_client.subscribe("result_queue", cb=self.handle_result)

        while True:
            num_workers = len(self.worker_nodes)
            num_available = sum(self.worker_nodes.values())

            print(f"Number of worker nodes: {num_workers}")
            print(f"Number of available worker nodes: {num_available}")

            for worker_id, is_available in self.worker_nodes.items():
                status = "AVAILABLE" if is_available else "UNAVAILABLE"
                print(f"Worker {worker_id}: {status}")

            print()

            await asyncio.sleep(1)
            print("Enter task details:")

            operations = ["add", "subtract", "multiply", "divide"]
            operation = random.choice(operations)
            operand1 = random.randint(1, 1000)
            operand2 = random.randint(1, 10000)
            timeout_seconds = random.randint(1, 10)

            print("==================================Input=======================================")
            print(
                "Operation : {} | Operand1 : {} | Operand2 : {} | TimeOut : {} |".format(operation, operand1, operand2,
                                                                                         timeout_seconds))
            print("==============================================================================")
            available_workers = [worker_id for worker_id, is_available in self.worker_nodes.items() if is_available]
            if not available_workers:
                print("No available workers. Task will be Queued")
                await self.create_task(operation, operand1, operand2, timeout_seconds)
            else:
                worker_id = random.choice(available_workers)
                self.worker_nodes[worker_id] = False  # Set worker status to unavailable
                print("Create TASK when to worker is available")
                await self.create_task(operation, operand1, operand2, timeout_seconds)

            await asyncio.sleep(1)

            # self.worker_nodes[worker_id] = True     # Set worker status to available


if __name__ == "__main__":
    controller = Controller()
    asyncio.run(controller.run())
