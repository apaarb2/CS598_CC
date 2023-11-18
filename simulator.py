from copy import deepcopy
from numpy import random, percentile
from random import randint
from math import ceil
from workload import Workload
from scheduler_interface import SchedulerInterface

class Simulator:
    def __init__(
            self,
            seed_containers,
            num_to_generate,
            generation_time,
            distribution,
            workload_profiles):
        self.seed_containers = seed_containers
        self.num_to_generate = num_to_generate
        self.generation_time = generation_time
        self.workload_profiles = workload_profiles

        self.batches = []

        self.distribution = distribution
        if self.distribution == "UNIFORM":
            batch_size = ceil(self.num_to_generate / self.generation_time)
            self.batches = [batch_size] * self.generation_time
        elif self.distribution == "RANDOM_NORMAL":
            x = random.normal(size=(self.generation_time))
            minV = -1 * min(x)
            x = [i + minV for i in x]
            sumV = sum(x)
            x = [i / sumV for i in x]
            x = [ceil(self.num_to_generate * i) for i in x]
            self.batches = x
        elif self.distribution == "RANDOM_EXPONENTIAL":
            x = random.exponential(size=(self.generation_time))
            minV = -1 * min(x)
            x = [i + minV for i in x]
            sumV = sum(x)
            x = [i / sumV for i in x]
            x = [ceil(self.num_to_generate * i) for i in x]
            self.batches = x
        else:
            raise Exception("unimplemented")

        pass

    def gen_workloads(self, time):
        if time >= self.generation_time:
            return []

        batch_size = self.batches[time]
        
        workloads = []
        for i in range(0, batch_size):
            workload = deepcopy(self.workload_profiles[
                randint(0, len(self.workload_profiles) - 1)])
            workloads.append(workload)

        return workloads

    
    def run(self, scheduler):
        time = 0

        scheduler.reset_implementation()
        scheduler.reset()
        for container in self.seed_containers:
            _id = container.get_id()
            container.__init__(_id) # reset the container with old id
            scheduler.add_new_container(container)

        num_containers_at_start = len(scheduler.get_containers())

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
        containers = scheduler.get_containers()
        num_containers_at_end = len(containers)

        aggregate_workload_runtimes = []
        job_name_to_num_containers = {}
        for container in containers:
            for job_name in container.get_job_names():
                if job_name not in job_name_to_num_containers:
                    job_name_to_num_containers[job_name] = 0
                job_name_to_num_containers[job_name] += 1

            aggregate_workload_runtimes += container.workload_runtimes

        print("-=-=-= Summary for {} =-=-=-\n\
Spec:\n\
  * {} workloads -> {} distr over {} time \n\
  * with {} unique workloads\n\
Result:\n\
  * Total time to process = {} time units,\n\
  * Containers grew by {} (from {} to {}),\n\
  * Distributions of jobs across containers = {}, \n\
  * {} workloads' runtime distribution is as follows:\n\
  p0, p10, p50, p75, p90, p100\n\
  {}, {}, {}, {}, {}, {}\n\
              ".format(
                  scheduler.name,
                  self.num_to_generate,
                  self.distribution,
                  self.generation_time,
                  len(self.workload_profiles),
                  time,
                  num_containers_at_end - num_containers_at_start,
                  num_containers_at_start,
                  num_containers_at_end,
                  job_name_to_num_containers,
                  len(aggregate_workload_runtimes),
                  percentile(aggregate_workload_runtimes, 0),
                  percentile(aggregate_workload_runtimes, 10),
                  percentile(aggregate_workload_runtimes, 50),
                  percentile(aggregate_workload_runtimes, 75),
                  percentile(aggregate_workload_runtimes, 90),
                  percentile(aggregate_workload_runtimes, 100),
                  ))
        pass
