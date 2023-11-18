from simulator import Simulator
from container import Container
from scheduler_roundrobin import SchedulerRoundRobin
from scheduler_hermod import SchedulerHermod
from scheduler_cypress import SchedulerCypress
from scheduler_ccc import SchedulerCCC
from workload import Workload

seed_containers = [Container(0), Container(1)]

simulator = Simulator(
        seed_containers = seed_containers,
        num_to_generate = 2000,
        generation_time = 100,
        distribution = "UNIFORM",
        workload_profiles = [
            Workload('a', 1, 9, 15, 0, 0, 1),
            Workload('b', 1, 9, 15, 0, 0, 1),
            Workload('a', 3, 9, 15, 0, 0, 3),
            Workload('b', 3, 9, 15, 0, 0, 3),
            Workload('a', 5, 9, 15, 0, 0, 5),
            Workload('b', 5, 9, 15, 0, 0, 5),
            ])

simulator.run(SchedulerRoundRobin([]))
simulator.run(SchedulerCCC([]))
