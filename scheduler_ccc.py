from scheduler_interface import SchedulerInterface

# Cloud Computing Capstone Scheduler
class SchedulerCCC(SchedulerInterface):
    def __init__(self, containers):
        super().__init__(containers)
        pass

    def reset_implementation(self):
        pass

    def process(self, workload):
        # NOTE: call self.request_new_container() if there are
        #       no available containers. 
        pass
