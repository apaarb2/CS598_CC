from numpy import random
from random import randint
from math import ceil
from workload import Workload
from scheduler_interface import SchedulerInterface

class Simulator:
    def __init__(self, seed_containers, num_to_generate, generation_time, distribution, job_names, input_sizes):
        self.seed_containers = seed_containers
        self.num_to_generate = num_to_generate
        self.generation_time = generation_time

        self.batches = []

        if distribution == "UNIFORM":
            batch_size = ceil(self.num_to_generate / self.generation_time)
            self.batches = [batch_size] * self.generation_time
        elif distribution == "RANDOM_NORMAL":
            x = random.normal(size=(self.generation_time))
            minV = -1 * min(x)
            x = [i + minV for i in x]
            sumV = sum(x)
            x = [i / sumV for i in x]
            x = [ceil(self.num_to_generate * i) for i in x]
            self.batches = x
        elif distribution == "RANDOM_EXPONENTIAL":
            x = random.exponential(size=(self.generation_time))
            minV = -1 * min(x)
            x = [i + minV for i in x]
            sumV = sum(x)
            x = [i / sumV for i in x]
            x = [ceil(self.num_to_generate * i) for i in x]
            self.batches = x
        else:
            raise Exception("unimplemented")

        self.job_names = job_names
        self.input_sizes = input_sizes
        pass

    def gen_workloads(self, time):
        if time >= self.generation_time:
            return []

        batch_size = self.batches[time]
        
        workloads = []
        for i in range(0, batch_size):
            job = self.job_names[
                    randint(0, len(self.job_names) - 1)]
            input_size = self.input_sizes[
                    randint(0, len(self.input_sizes) - 1)]
            workloads.append(Workload(job, input_size, 9, 15, 0, 0, input_size))
        return workloads

    
    def run(self, scheduler):
        time = 0

        scheduler.reset_implementation()
        scheduler.reset()
        for container in self.seed_containers:
            scheduler.add_new_container(container)

        num_containers_at_start = len(scheduler.get_containers())

        # for time in range(0, time):
        num_workloads_generated = 0
        num_active_workloads = 0

        while num_active_workloads > 0 or num_workloads_generated < self.num_to_generate:

            # Generate workloads
            for workload in self.gen_workloads(time):
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

            time += 1

            # print("t_{}, #container={}, #workloads={}".format(
            #     time, len(scheduler.get_containers()),
            #     num_workloads_generated))

        # Reporting logic below
        # TODO: add more here
        containers = scheduler.get_containers()
        num_containers_at_end = len(containers)

        job_name_to_num_containers = {}
        for container in containers:
            for job_name in container.get_job_names():
                if job_name not in job_name_to_num_containers:
                    job_name_to_num_containers[job_name] = 0
                job_name_to_num_containers[job_name] += 1

        print("-=-=-= end of run =-=-=-\n\
               processed {} workloads in {} time units,\n\
               containers grew from {} -> {},\n\
               job_name_to_num_containers = {}, \n\
              ".format(
                  num_workloads_generated,
                  time,
                  num_containers_at_start,
                  num_containers_at_end,
                  job_name_to_num_containers))
        pass
