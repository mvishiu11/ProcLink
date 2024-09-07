# ProcLink

**ProcLink** is a modular and extensible process communication package designed for real-time inter-process communication using ZeroMQ (ZMQ) in Python. The package offers a robust architecture with error handling, protocol support for both TCP and IPC (Unix Domain Sockets), and real-time performance benchmarking. It is particularly suited for use cases where multiple processes must work together efficiently on the same or different machines.

## Features
- **Flexible Communication Protocols**: Supports both TCP and IPC protocols for inter-process communication.
- **Process Management**: Includes a process manager for starting, joining, and terminating multiple processes safely and efficiently.
- **Benchmarking**: Built-in benchmarking for measuring latency and performance in real-time communication scenarios.
- **Error Handling**: Graceful error handling and shutdown for all processes.
- **Modular and Extensible**: Designed with extensibility in mind, allowing easy integration into various projects and use cases.

## Architecture

The **ProcLink** architecture is built around three main components: `ProcessManager`, `Communication`, and `Benchmark`. Each of these components is designed to handle a specific aspect of process communication and management, ensuring a clean separation of concerns and ease of use.

### Components Overview

1. **`ProcessManager`** (in `process.py`):
    - Manages the lifecycle of multiple processes, including creation, starting, joining, and termination.
    - Handles graceful shutdowns in case of errors or user interrupts.
    - Ensures that processes run concurrently and are terminated safely when needed.

    ```python
    from proclink.process import ProcessManager

    process_manager = ProcessManager()
    process_manager.create_process(target=some_function)
    process_manager.run()  # Starts and joins all processes
    ```

2. **`Communication`** (in `communication.py`):
    - Manages inter-process communication using ZMQ, allowing processes to exchange messages via TCP or IPC.
    - Supports publisher-subscriber patterns where publishers send messages on specific topics and subscribers listen to those topics.
    - Provides both blocking and non-blocking message sending and receiving.

    ```python
    from proclink.communication import Communication

    comm = Communication()
    pub_socket = comm.create_publisher(protocol="tcp", port="5555")
    sub_socket = comm.create_subscriber(protocol="tcp", port="5555", topics=["example_topic"])

    comm.send(pub_socket, "example_topic", "Hello, World!")
    message = comm.receive(sub_socket)
    ```

3. **`Benchmark`** (in `benchmark.py`):
    - Provides tools for measuring the latency of messages and real-time performance.
    - Measures the time difference between message sending and receiving, allowing for precise tracking of communication delays.

    ```python
    from proclink.benchmark import Benchmark

    benchmark = Benchmark()
    benchmark.start_latency_timer()
    # Send message
    latency = benchmark.stop_latency_timer()
    print(f"Message latency: {latency} seconds")
    ```

## Installation

ProcLink is designed to be easy to integrate into your projects. You can clone this repository and install it locally using `pip`:

```bash
git clone
cd proclink
pip install .
```

## Usage Example

Here’s a simple example that demonstrates how to use **ProcLink** to manage multiple processes and exchange messages between them:

### Example: Simple Publisher-Subscriber

```python
import time
from proclink.process import ProcessManager
from proclink.communication import Communication

# Publisher process
def publisher_process():
    comm = Communication()
    pub_socket = comm.create_publisher(protocol="tcp", port="5555")
    for i in range(5):
        comm.send(pub_socket, "topic", f"Message {i}")
        time.sleep(1)

# Subscriber process
def subscriber_process():
    comm = Communication()
    sub_socket = comm.create_subscriber(protocol="tcp", port="5555", topics=["topic"])
    while True:
        message = comm.receive(sub_socket)
        print(f"Received: {message}")

if __name__ == "__main__":
    process_manager = ProcessManager()
    process_manager.create_process(target=publisher_process)
    process_manager.create_process(target=subscriber_process)
    process_manager.run()
```

A more detailed example and additional use cases can be found in the `examples` directory of the repository.

## Detailed Explanation of Core Modules

### 1. `ProcessManager`

The `ProcessManager` class simplifies managing multiple processes, including creating, starting, joining, and terminating processes. This ensures processes are managed cleanly and efficiently, with error handling and graceful termination when necessary.

Key Methods:
- `create_process(target, args=())`: Creates and registers a new process.
- `run()`: Starts all processes and handles errors.
- `terminate_all()`: Terminates all running processes.

### 2. `Communication`

The `Communication` class uses ZMQ to handle communication between processes. It supports both TCP and IPC protocols, allowing for flexible message passing based on your environment. It also handles the creation of publisher and subscriber sockets.

Key Methods:
- `create_publisher(protocol, address, port)`: Creates a publisher socket.
- `create_subscriber(protocol, address, port, topics)`: Creates a subscriber socket and subscribes to topics.
- `send(socket, topic, message)`: Sends a message with a specified topic.
- `receive(socket)`: Receives a message.

### 3. `Benchmark`

The `Benchmark` class provides tools for measuring latency and time-to-real-time delays in communication. It can track the time between sending and receiving messages, helping you monitor and optimize the performance of your system.

Key Methods:
- `start_latency_timer()`: Starts the timer for measuring latency.
- `stop_latency_timer()`: Stops the timer and returns the elapsed time.
- `time_to_real_time(message_time)`: Calculates the delay in processing.

## Requirements
- Python 3.8+
- `pyzmq` for ZeroMQ communication
- `multiprocessing` for process management

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.