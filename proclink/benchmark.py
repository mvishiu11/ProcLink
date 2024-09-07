import time

class Benchmark:
    """
    A class to handle benchmarking for communication performance.

    Methods:
        start_latency_timer(): Starts a timer for latency measurement.
        stop_latency_timer(): Stops the timer and returns the measured latency.
        time_to_real_time(start_time, message_time): Calculates the delay in processing in real-time.
    """

    def __init__(self):
        self.start_time = None

    def start_latency_timer(self):
        """
        Starts the latency timer.
        """
        self.start_time = time.time()

    def stop_latency_timer(self):
        """
        Stops the latency timer and returns the elapsed time.
        
        Returns:
            float: The measured latency in seconds.
        """
        if self.start_time is None:
            raise ValueError("Latency timer was not started.")
        return time.time() - self.start_time

    def time_to_real_time(self, message_time):
        """
        Calculates the delay between the current time and the message timestamp.
        
        Args:
            message_time (float): The timestamp of when the message was sent.

        Returns:
            float: The time delay from real-time in seconds.
        """
        current_time = time.time()
        return current_time - message_time
