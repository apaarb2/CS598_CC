from scheduler_interface import SchedulerInterface

class SchedulerHermod(SchedulerInterface):
    def __init__(self, containers):
        super().__init__(containers)
        self.idx = 0


    def process(self, workload):
        # NOTE: call self.request_new_container() if there are
        #       no available containers. 
        pass
