from scheduler_interface import SchedulerInterface

class SchedulerRoundRobin(SchedulerInterface):
    def __init__(self, containers):
        super().__init__(containers)
        self.idx = 0

    def reset_implementation(self):
        self.idx = 0

    def process(self, workload):

        for i in range(0, len(self.containers)):
            self.idx += 1 
            self.idx = self.idx % len(self.containers)

            if self.containers[self.idx].process(workload):
                return  # container accepted process request

        # print("ERROR: no containers, requested new one")
        self.request_new_container()
