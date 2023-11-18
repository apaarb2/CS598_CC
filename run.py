from simulator import Simulator
from container import Container
from scheduler_roundrobin import SchedulerRoundRobin
from scheduler_hermod import SchedulerHermod
from scheduler_cypress import SchedulerCypress
from scheduler_ccc import SchedulerCCC

seed_containers = [Container(0), Container(1)]

simulator = Simulator(
        seed_containers = seed_containers,
        num_to_generate = 100,
        generation_time = 30,
        distribution = "UNIFORM",
        job_names = ['a', 'b'],
        input_sizes = [1, 3, 5])

simulator.run(SchedulerRoundRobin([]))
