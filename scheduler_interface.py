from container import Container

class SchedulerInterface:
    def __init__(self, containers):
        pass

    # Called by simulator.py before new experiment run
    # For the implementation to clear any existing state
    def reset_implementation(self):
        raise Exception("must override") 

    # Called by simulator.py before new experiment run
    def reset(self):
        self.containers = []
        self.container_id = 0

    # Called by simulator.py for new container turn-up
    def add_new_container(self, container):
        self.containers.append(container)
        self.container_id += 1

    # Called by simulator.py to mimic container failure
    def remove_container(self, container_id):
        self.containers = [c for c in self.containers if container_id != c.get_id()]   

    def request_new_container(self):
        container = Container(self.container_id)
        self.containers.append(container)
        self.container_id += 1

    def get_containers(self):
        return self.containers

    # TODO: child classes must override this
    def process(self, workload):
        # WHAT: scheduler should pick a container, 
        #       the scheduler must call process on selected
        #       container.
        raise Exception("must override") 
