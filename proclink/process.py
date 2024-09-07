import multiprocessing

class ProcessManager:
    """
    A class to manage multiple processes with error handling and protocol support.

    Attributes:
        processes (list): List of multiprocessing.Process objects.
    """

    def __init__(self):
        """
        Initializes the ProcessManager with an empty list of processes.
        """
        self.processes = []

    def create_process(self, target, args=()):
        """
        Creates a new process and appends it to the list of managed processes.

        Args:
            target (callable): The target function for the process.
            args (tuple): The arguments to pass to the target function.

        Returns:
            multiprocessing.Process: The created process.
        """
        process = multiprocessing.Process(target=target, args=args)
        self.processes.append(process)
        return process

    def start_all(self):
        """
        Starts all managed processes.
        """
        for process in self.processes:
            process.start()

    def join_all(self):
        """
        Joins all managed processes, ensuring they finish execution.
        """
        for process in self.processes:
            process.join()

    def terminate_all(self):
        """
        Terminates all managed processes in case of errors or shutdown.
        """
        for process in self.processes:
            if process.is_alive():
                process.terminate()

    def run(self):
        """
        Starts and manages all processes, including error handling.
        If any process fails, it gracefully shuts down all processes.
        """
        try:
            self.start_all()
            self.join_all()
        except KeyboardInterrupt:
            print("Terminating processes...")
            self.terminate_all()
        except Exception as e:
            print(f"Error encountered: {e}")
            self.terminate_all()
            raise e
