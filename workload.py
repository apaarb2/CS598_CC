class Workload:
    
    # NOTE: It is important to model workloads such that
    #       the input_size is proportional to workload_duration
    #       That is a core assumption of this paper.

    def __init__(self, job_name, input_size, creation_cpu, creation_mem, runtime_cpu, runtime_mem, duration):
        self.job_name = job_name
        self.input_size = input_size
        self.creation_cpu_cost = creation_cpu
        self.creation_mem_cost = creation_mem
        self.runtime_cpu_cost = runtime_cpu
        self.runtime_mem_cost = runtime_mem
        self.workload_duration = duration
        self.time = 0

    def container_start_time(self, t):
        self.container_start_time = t
    
    # Called by container.py in tick()
    def is_active(self):
        if self.time >= self.workload_duration:
            return False
        return True

    # Called by container.py in tick()
    def tick(self):
        retVal = ()
        if self.time == 0:
            retVal = (self.creation_cpu_cost, self.creation_mem_cost)
        else:
            retVal = (self.runtime_cpu_cost, self.runtime_mem_cost)
        self.time += 1
        return retVal
