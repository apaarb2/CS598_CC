from scheduler_interface import SchedulerInterface
from random import choice

class SchedulerCCC(SchedulerInterface):
    def __init__(self, containers):
        super().__init__(containers)
        self.name = "CCC"
        self.container_load = {}  # To keep track of container load

    def reset_implementation(self):
        # Reset the state for a new experiment
        self.container_load = {}

    def process(self, workload):
        if not self.containers:
            self.request_new_container()

        selected_container = self.select_container(workload)

        if not selected_container.process(workload):
            # Try processing with other containers
            for container in self.containers:
                if container != selected_container and container.process(workload):
                    return  # Successfully processed with an alternate container

            # If all containers are unable to process, request a new one
            self.request_new_container()
            self.containers[-1].process(workload)  # Process workload with the newly created container


    def select_container(self, workload):
        # Step 1: Prefer containers with the workload already present
        for container in self.containers:
            if workload.job_name in container.get_job_names() and not container.is_overloaded():
                return container

        # Step 2: Use containers with least load considering input size
        # Update container_load to consider both number of workloads and their input sizes
        self.update_container_loads(workload)

        # Select the container with the least load that can handle the workload
        least_loaded_container = min(self.container_load, key=self.container_load.get)
        return next(container for container in self.containers if container.get_id() == least_loaded_container)

    def update_container_loads(self, new_workload):
        for container in self.containers:
            total_input_size = sum(w.input_size for w in container.workloads)
            # Load calculation can be adjusted based on how you want to weigh input size
            load = total_input_size + new_workload.input_size
            self.container_load[container.get_id()] = load
