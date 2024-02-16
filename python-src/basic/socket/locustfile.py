from locust import User, task, between
import time
import socket
from basic.payload import builder

class BasicClientUser(User):
    wait_time = between(1, 2)  # Time between tasks

    def on_start(self):
        """
        Initialize the client.
        """
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect(("127.0.0.1", 2000))
        except Exception as e:
            print(f"Failed to connect: {e}")
            self.environment.runner.quit()  # Stop the test if cannot connect

    def on_stop(self):
        """
        Clean up when the user stops.
        """
        if self.client:
            self.client.close()

    def report_success(self, request_type, name, response_time, response_length):
        """
        Helper method to report successful requests to Locust.
        """
        self.environment.events.request.fire(
            request_type=request_type,
            name=name,
            response_time=response_time,
            response_length=response_length,
            exception=None,
            context={},
            user=self
        )

    def report_failure(self, request_type, name, response_time, exception):
        """
        Helper method to report failed requests to Locust.
        """
        self.environment.events.request.fire(
            request_type=request_type,
            name=name,
            response_time=response_time,
            response_length=0,
            exception=exception,
            context={},
            user=self
        )

    @task
    def send_message(self):
        """
        The task performed by the user.
        """
        bldr = builder.BasicBuilder()
        message = bldr.encode("full_stack_alchemists", "public", "Hello from Locust!")
        start_time = time.time()

        try:
            self.client.sendall(bytes(message, "utf-8"))
            response = self.client.recv(1024)
            end_time = time.time()

            # Calculate request time in milliseconds
            request_time = int((end_time - start_time) * 1000)
            self.report_success("TCP", "send_message", request_time, len(response))
        except Exception as e:
            self.report_failure("TCP", "send_message", 0, str(e))
