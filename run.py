from simulator import Simulator
from container import Container
from scheduler_roundrobin import SchedulerRoundRobin
from scheduler_hermod import SchedulerHermod
from scheduler_cypress import SchedulerCypress
from scheduler_ccc import SchedulerCCC

seed_containers = [Container(0), Container(1)]

simulator = Simulator(30)
simulator.run(SchedulerRoundRobin(seed_containers))
