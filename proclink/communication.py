import zmq
import os

class Communication:
    """
    A class to handle inter-process communication using ZMQ with support for both
    TCP and IPC (Unix Domain Sockets).
    
    Attributes:
        context: The ZMQ context object used to create sockets.
    """

    def __init__(self):
        """
        Initializes the ZMQ context.
        """
        self.context = zmq.Context()

    def _check_ipc_support(self):
        """
        Checks if IPC (Unix Domain Sockets) are supported on the current system.

        Returns:
            bool: True if IPC is supported, False otherwise.
        """
        return os.name != 'nt'  # IPC is unavailable on Windows systems

    def create_publisher(self, protocol="tcp", address="127.0.0.1", port="5555"):
        """
        Create a ZMQ publisher socket using the specified protocol (TCP/IPC).
        
        Args:
            protocol (str): The communication protocol, either 'tcp' or 'ipc'.
            address (str): The IP address or path for IPC.
            port (str): The port for TCP communication (ignored for IPC).

        Returns:
            zmq.Socket: The publisher socket.
        """
        socket = self.context.socket(zmq.PUB)

        if protocol == "tcp":
            socket.bind(f"tcp://{address}:{port}")
        elif protocol == "ipc" and self._check_ipc_support():
            socket.bind(f"ipc://{address}")
        else:
            raise ValueError("IPC is not supported on this system. Use TCP instead.")

        return socket

    def create_subscriber(self, protocol="tcp", address="127.0.0.1", port="5555", topics=None):
        """
        Create a ZMQ subscriber socket and subscribe to specific topics.
        
        Args:
            protocol (str): The communication protocol, either 'tcp' or 'ipc'.
            address (str): The IP address or path for IPC.
            port (str): The port for TCP communication (ignored for IPC).
            topics (list): List of topics to subscribe to.

        Returns:
            zmq.Socket: The subscriber socket.
        """
        if topics is None:
            topics = []

        socket = self.context.socket(zmq.SUB)

        if protocol == "tcp":
            socket.connect(f"tcp://{address}:{port}")
        elif protocol == "ipc" and self._check_ipc_support():
            socket.connect(f"ipc://{address}")
        else:
            raise ValueError("IPC is not supported on this system. Use TCP instead.")

        for topic in topics:
            socket.setsockopt_string(zmq.SUBSCRIBE, topic)
        
        return socket

    def send(self, socket, topic, message, non_blocking=False):
        """
        Send a message to a specific topic.

        Args:
            socket (zmq.Socket): The ZMQ socket to send the message.
            topic (str): The topic to send the message under.
            message (str): The message to send.
            non_blocking (bool): Whether to send in non-blocking mode.
        """
        socket.send_string(f"{topic} {message}", flags=zmq.NOBLOCK if non_blocking else 0)

    def receive(self, socket, non_blocking=False):
        """
        Receive a message from the socket.

        Args:
            socket (zmq.Socket): The ZMQ socket to receive the message from.
            non_blocking (bool): Whether to receive in non-blocking mode

        Returns:
            str: The received message.
        """
        return socket.recv_string(flags=zmq.NOBLOCK if non_blocking else 0)

    def close(self):
        """
        Close the ZMQ context and sockets to clean up resources.
        """
        self.context.term()
