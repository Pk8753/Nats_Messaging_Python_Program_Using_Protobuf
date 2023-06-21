# Nats_Messaging_Python_Program_Using_Protobuf
The project aims to develop a task distributor system using Python. The system consists of a controller node and multiple worker nodes. The end user interacts with the system through a Command-Line Interface (CLI). The system utilizes Protocol Buffers (protobuf) for efficient serialization and deserialization of task messages exchanged between the controller and worker nodes. This ensures fast and reliable communication between the components, enabling seamless distribution and execution of tasks in a distributed environment.

## Introduction

This project is a Python application that showcases the usage of the pytest framework for testing, along with Dockerfiles and Docker Compose for containerization and orchestration.

The project provides a sample Python application with modular code structure and unit tests implemented using pytest. It also includes Dockerfiles to build Docker images for the application and a Docker Compose file to simplify the setup and deployment of the project.


## Prerequisites

Make sure you have the following installed:

- Python 3.x
- Docker
- Docker Compose
- NATs
- Python virtual env
    ```shell
  > python3 -m venv venv
  > source venv/bin/activate


## Getting Started

- NATS server details [nats://0.0.0.0:4222]

1. **Clone the repository:**

   ```shell
   git clone https://github.com/Pk8753/Nats_Messaging_Python_Program_Using_Protobuf.git
   cd project
   

2. **Install the project dependencies:**
    ```shell
    pip install -r requirements.txt
   

3. **Convert .proto files in pb2.py :**
    ```shell
    Goto path src/proto_files. A new file task_pb2.py will create.
   
   RUN > protoc -I=. --python_out=. task.proto
   

4. **Run program locally:**
    ```shell
    Goto src folder and run below file sequentially. (Open three files in three different terminals)
   First start the nats server,after starts the worker listener andthen start controller.
   1. > python nats_server.p
   2. > python worker.py
   3. > python controller.py
   As soon as you run controller.py you will start noticing task getting published from 
   controller and task are getting subscriber at worker node using nats messaging model through protobuf serializing and
   deserializing. 
  

5. **Run the tests locally :**
    ```shell
   Goto src/ folder.
   1. To run all the test  # > python -m pytest -v
   2. To run specefic test file #>  python -m pytest controller_test.py -v
   
6. **Build the Docker image :**
    ```shell
   Goto parent folder (controller_&_worker).
   1. To build image from controller dockerfile  # >  docker build -t controller -f Dockerfile
   2. To run docker container #> docker run -it --rm controller 
   
   3. To build image from worker dockerfile  #>   docker build -t worker -f worker.Dockerfile 
   4. To run docker container #> docker run -it --rm worker 
   

7. **Build the Docker image for test run :**
    ```shell
   Goto parent folder (controller_&_worker).
   1. To build image from test dockerfile  # >  docker build -t test_run -f testrun.Dockerfile
   2. To run docker container #> docker run -it --rm test_run 
   

## Reports

- Goto src/reports folder to get test reports. It is using html reporter.






   



 