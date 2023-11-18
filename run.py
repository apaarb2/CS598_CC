from simulator import Simulator
from container import Container
from scheduler_roundrobin import SchedulerRoundRobin
from scheduler_hermod import SchedulerHermod
from scheduler_cypress import SchedulerCypress
from scheduler_ccc import SchedulerCCC
from workload import Workload

seed_containers = [Container(0), Container(1)]
workloads = [
        Workload('a', 1, 9, 15, 0, 0, 1),
        Workload('b', 1, 15, 9, 0, 0, 1),
        Workload('c', 3, 8, 8, 1, 1, 3),
        Workload('d', 1, 1, 1, 0, 0, 1),
        Workload('d', 3, 1, 2, 3, 3, 3),
        Workload('d', 9, 2, 6, 1, 1, 9),
        Workload('e', 10, 1, 10, 1, 2, 10),
        Workload('e', 15, 1, 13, 1, 3, 15),
        ]

e_uniform = Simulator(
        seed_containers = seed_containers,
        num_to_generate = 2000,
        generation_time = 100,
        distribution = "UNIFORM",
        workload_profiles = workloads)

e_normal = Simulator(
        seed_containers = seed_containers,
        num_to_generate = 2000,
        generation_time = 100,
        distribution = "RANDOM_NORMAL",
        workload_profiles = workloads)

e_exp = Simulator(
        seed_containers = seed_containers,
        num_to_generate = 2000,
        generation_time = 100,
        distribution = "RANDOM_EXPONENTIAL",
        workload_profiles = workloads)

# TODO: Include other schedulers
e_uniform.run(SchedulerRoundRobin([]))
e_uniform.run(SchedulerCCC([]))
e_normal.run(SchedulerRoundRobin([]))
e_normal.run(SchedulerCCC([]))
e_exp.run(SchedulerRoundRobin([]))
e_exp.run(SchedulerCCC([]))
