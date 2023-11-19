from scheduler_interface import SchedulerInterface
from random import choice
from math import ceil

class SchedulerCypress(SchedulerInterface):
    def __init__(self, containers):
        super().__init__(containers)
        self.name = "cypress"
        self.queue = []
        # to prevent division by 0 errors
        self.epsilon = 1e-5
        pass

    def reset_implementation(self):
        pass

    def process(self, workload):
        if not self.containers:
            self.request_new_container()
        self.queue.append(workload)
        # Proactive scaling
        # Input size should be proportional to workload duration
        # Get current sustainable workload projection for each container
        container_sustainable_workload_projection = [(sum(
            workload.workload_duration for workload in container.workloads) / (((container.cpu_util_pct / 100) + (container.mem_util_pct / 100) + self.epsilon) / 2)) for container in self.containers if container.get_num_active_workloads()]
        avg_workload = 120 # set default average workload
        if container_sustainable_workload_projection:
            # Calculate average workload capacity across available pods
            avg_workload = sum(container_sustainable_workload_projection) / len(container_sustainable_workload_projection)
            # Subtract current load to see available capacity
            container_available_capacity = sum([workload - sum(workload.workload_duration for workload in container.workloads) for container, workload in zip(self.containers, container_sustainable_workload_projection)])
            # Calculate required capacity based on queue
            required_capacity = sum([queued.workload_duration for queued in self.queue])
            if required_capacity > container_available_capacity:
                # calculate how many new containers are needed based on required capacity and sustainable workload projection
                self.request_new_container()

        # Input size sensitive request batching
        next_queue = []
        while self.queue:
            item = self.queue.pop(0)
            try:
                selected_container = self.select_container(item, avg_workload)
                if not selected_container.process(item):
                    self.request_new_container()
                    # If the container is overloaded, queue it
                    next_queue.append(workload)
            except:
                self.request_new_container()
                next_queue.append(item)
        
        self.queue = next_queue

    def select_container(self, workload, avg_workload):
        # Implementing a strategy for cypress input size aware scheduling
        input_size = workload.workload_duration
        
        # Use the current workload duration divided by utilization to get the projected total container load
        # Cypress uses first fit bin packing, so we want to find the first container that can fit the projected load
        return next(container for container in self.containers if not container.is_overloaded() and (avg_workload == 0 or (avg_workload >= input_size + sum(workload.workload_duration for workload in container.workloads))))
