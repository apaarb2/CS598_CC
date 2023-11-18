from workload import Workload
from container import Container
from scheduler_interface import SchedulerInterface

class Simulator:
    def __init__(self, duration_of_experiment):
        self.duration_of_experiment = duration_of_experiment
        pass

    def gen_workloads(self, time):
        # TODO: make this generate randomly and based on time
        workloads = []
        workloads.append(Workload('a', 1, 9, 15, 0, 0, 1))
        workloads.append(Workload('a', 3, 9, 15, 2, 2, 3))
        workloads.append(Workload('a', 5, 9, 15, 2, 2, 6))

        workloads.append(Workload('b', 1, 20, 4, 0, 0, 1))
        return workloads

    
    def run(self, scheduler):
        num_containers_at_start = len(scheduler.get_containers())
        num_workloads_generated = 0

        for time in range(0, self.duration_of_experiment):
            for workload in self.gen_workloads(time):
                num_workloads_generated += 1
                scheduler.process(workload)

            # Progress time for every container so that it
            # may recompute current mem/cpu load
            for container in scheduler.get_containers():
                container.tick()

            # TODO: call remove_container on scheduler to
            #       mimic crashes/network failures

        # Reporting logic below
        # TODO: add more here
        num_containers_at_end = len(scheduler.get_containers())
        print("-=-=-= end of run =-=-=-\n\
               containers grew from {} -> {},\n\
               num workloads generated = {}, \n\
              ".format(
                  num_containers_at_start,
                  num_containers_at_end,
                  num_workloads_generated))
        pass
