from scheduler_interface import SchedulerInterface
from random import choice
import numpy as np

class SchedulerHermod(SchedulerInterface):
    def __init__(self, containers):
        super().__init__(containers)
        self.name = "hermod"
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
            self.select_container(self.containers).process(workload)

    def select_container(self, workload):
        # Implementing a strategy that is locality aware and uses hybrid load balancing
        # Step 1: If low load, consolidate workloads in the same container for efficiency
        # Step 2: If high load (all containers loaded), use containers with least load
        # Step 3: If multiple workers are equally loaded, select the one with a warm container already to consolidate

        # Decide if we are in a low or high load scenario
        # If any of the containers have avilable cores, we are in a low load scenario
        if any(container.get_num_active_workloads() < container.get_cores()
                for container in self.containers):
            # in that case, consolidate workloads in the same container for efficiency
            return next(container for container in self.containers if container.get_num_active_workloads() < container.get_cores())
        else:
            self.container_load = {container.get_id(): container.get_num_active_workloads() for container in self.containers}
            least_loaded_container = min(self.container_load, key=self.container_load.get)
            return next(container for container in self.containers if container.get_id() == least_loaded_container)
