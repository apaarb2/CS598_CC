from simulator import Simulator
from container import Container
from scheduler_roundrobin import SchedulerRoundRobin

seed_containers = [Container(0), Container(1)]

simulator = Simulator(30)
simulator.run(SchedulerRoundRobin(seed_containers))
