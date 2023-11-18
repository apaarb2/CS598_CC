from random import randint
from math import ceil
from workload import Workload
from container import Container
from scheduler_interface import SchedulerInterface

class Simulator:
    def __init__(self, num_to_generate, generation_time):
        self.num_to_generate = num_to_generate
        self.generation_time = generation_time
        self.time = 0
        pass

    def gen_workloads(self, time):
        if time > self.generation_time:
            return []

        batch_size = ceil(self.num_to_generate / self.generation_time)
        
        workloads = []
        input_sizes = [1, 3, 5]
        jobs = ['a', 'b']

        for i in range(0, batch_size):
            job = jobs[randint(0, len(jobs) - 1)]
            input_size = input_sizes[randint(0, len(input_sizes) - 1)]
            workloads.append(Workload(job, input_size, 9, 15, 0, 0, input_size))

        return workloads

    
    def run(self, scheduler):
        num_containers_at_start = len(scheduler.get_containers())

        # for time in range(0, self.time):
        num_workloads_generated = 0
        num_active_workloads = 0

        while num_active_workloads > 0 or num_workloads_generated < self.num_to_generate:

            # Generate workloads
            for workload in self.gen_workloads(self.time):
                scheduler.process(workload)
                num_workloads_generated += 1

            # Progress time for every container so that it
            # may recompute current mem/cpu load
            num_active_workloads = 0
            for container in scheduler.get_containers():
                container.tick()
                num_active_workloads = container.get_num_active_workloads()

            # TODO: call remove_container on scheduler to
            #       mimic crashes/network failures

            self.time += 1

            print("t_{}, #container={}, #workloads={}".format(
                self.time, len(scheduler.get_containers()),
                num_workloads_generated))

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
