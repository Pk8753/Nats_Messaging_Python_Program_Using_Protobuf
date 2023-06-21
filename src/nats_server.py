import subprocess

def start_nats_server():
    subprocess.run(["docker", "run", "-p", "0.0.0.0:4222:4222", "-ti", "--name", "nats-server", "nats"])

def stop_nats_server():
    subprocess.run(["docker", "stop", "nats-server"])
    subprocess.run(["docker", "rm", "nats-server"])

if __name__ == "__main__":
    start_nats_server()
    # stop_nats_server()