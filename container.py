from workload import Workload

class Container:
    def __init__(self, container_id):
        self.id = container_id
        # print("Creating new container with id = ", self.id)
        self.cpu_limit = 100
        self.mem_limit = 100

        self.job_creation_cpu_cost = 10
        self.job_creation_mem_cost = 10
        
        self.cores = 1
        self.time = 0
        self.cpu_util_pct = 0  # cpu utilization %
        self.mem_util_pct = 0  # mem utilization %
        self.workloads = []

        self.job_names = []
        self.workload_runtimes = []

    def get_id(self):
        return self.id

    def get_job_names(self):
        return self.job_names
    
    def get_cores(self):
        return self.cores

    # called by process() in the scheduler implementation
    def process(self, workload):
        if self.is_overloaded():
            return False

        self.workloads.append(workload)

        # -1 since container will start processing only on tick
        workload.set_container_start_time(self.time - 1)
        return True

    def get_container_uptime(self):
        return self.time

    def get_num_active_workloads(self):
        return len(self.workloads)

    def is_overloaded(self):
        if self.cpu_util_pct > 80:
            return True
        if self.mem_util_pct > 80:
            return True
        return False

    # Process next round of simulation
    def tick(self):
        # measure cost of workloads at this point in time
        processing_workloads = []
        cpu_cost = 0
        mem_cost = 0
        new_job_names = []

        overloaded = False
        for workload in self.workloads:

            if overloaded:
                processing_workloads.append(workload)
                continue

            # create new job and do not process the workload if new job seen
            if workload.job_name not in self.job_names:
                processing_workloads.append(workload)

                if workload.job_name in new_job_names:
                    continue

                # print("creating job: ", workload.job_name, " on container ", self.id)
                cpu_cost += self.job_creation_cpu_cost
                mem_cost += self.job_creation_mem_cost
                new_job_names.append(workload.job_name)
                continue

            cpu, mem = workload.tick()
            cpu_cost += cpu
            mem_cost += mem
            if workload.is_active():
                processing_workloads.append(workload)
            else:
                self.workload_runtimes.append(
                        self.time - workload.container_start_time)

            if cpu_cost > 80 or mem_cost > 80:
                overloaded = True
                continue



        # add newly observed jobs to supported job names
        for new_job_name in new_job_names:
            self.job_names.append(new_job_name) 

        # update current cpu and mem utils
        self.cpu_util_pct = 100 * cpu_cost / self.cpu_limit
        self.mem_util_pct = 100 * mem_cost / self.mem_limit

        # Update workloads to only contain active ones
        self.workloads = processing_workloads


        # # Print final state for this round
        # print("t_{}:container_{}: active_jobs={},done_jobs={},cpu={},mem={}".format(
        #     self.time, self.id, self.get_num_active_workloads(), 
        #     len(self.workload_runtimes),
        #     self.cpu_util_pct, self.mem_util_pct))

        # move time forward
        self.time += 1  
