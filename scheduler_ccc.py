from scheduler_interface import SchedulerInterface
from random import choice

class SchedulerCCC(SchedulerInterface):
    def __init__(self, containers):
        super().__init__(containers)
        self.container_load = {}  # To keep track of container load

    def reset_implementation(self):
        # Reset the state for a new experiment
        self.container_load = {}

    def process(self, workload):
        # If no containers are available, request a new one
        if not self.containers:
            self.request_new_container()

        # Container selection strategy
        selected_container = self.select_container(workload)

        # Process the workload in the selected container
        if not selected_container.process(workload):
            # If the container is overloaded, request a new one and retry
            self.request_new_container()
            choice(self.containers).process(workload)

    def select_container(self, workload):
        # Implementing a strategy that merges Hermod and Cypress approaches
        # Step 1: Prefer containers with the workload already present
        # Step 2: If not found, use containers with least load considering input size

        for container in self.containers:
            if workload.job_name in container.get_job_names():
                return container

        # Calculate load considering the input size (Cypress approach)
        # This is a placeholder for the actual logic, which should consider the workload's input size
        for container in self.containers:
            self.container_load[container.get_id()] = container.get_num_active_workloads()

        # Select the container with the least load
        least_loaded_container = min(self.container_load, key=self.container_load.get)
        return next(container for container in self.containers if container.get_id() == least_loaded_container)
