from proclink.communication import Communication
from proclink.process import ProcessManager
from proclink.benchmark import Benchmark
import time

def publisher_process(protocol="tcp"):
    comm = Communication()
    benchmark = Benchmark()

    if protocol == "tcp":
        pub_socket = comm.create_publisher(protocol=protocol, port="5556")
    elif protocol == "ipc":
        pub_socket = comm.create_publisher(protocol=protocol, address="/tmp/drone_pub")
    else:
        raise ValueError("Invalid protocol specified.")

    # Delay to ensure the subscriber has connected
    time.sleep(1)

    msg_count = 0
    while True:
        message_time = time.time()
        benchmark.start_latency_timer()
        comm.send(pub_socket, "drone_status", f"status update {msg_count} at {message_time}")
        latency = benchmark.stop_latency_timer()
        print(f"Sent message #{msg_count} with latency: {latency} seconds")
        msg_count += 1
        time.sleep(1)

def subscriber_process(protocol="tcp"):
    comm = Communication()
    benchmark = Benchmark()

    if protocol == "tcp":
        sub_socket = comm.create_subscriber(protocol=protocol, port="5556", topics=["drone_status"])
    elif protocol == "ipc":
        sub_socket = comm.create_subscriber(protocol=protocol, address="/tmp/drone_pub", topics=["drone_status"])
    else:
        raise ValueError("Invalid protocol specified.")

    while True:
        message = comm.receive(sub_socket)
        print(f"Received: {message}")
        message_time = float(message.split()[-1])
        real_time_delay = benchmark.time_to_real_time(message_time)
        print(f"Time behind real-time: {real_time_delay} seconds")
        time.sleep(1)

if __name__ == "__main__":
    protocol = "tcp"  # You can switch to "ipc" if desired

    # Register the publisher and subscriber processes in the process manager
    process_manager = ProcessManager()
    publisher = process_manager.create_process(target=publisher_process, args=(protocol,))
    subscriber = process_manager.create_process(target=subscriber_process, args=(protocol,))

    # Start the processes and manage their lifecycle
    process_manager.run()
