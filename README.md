# CS598_CC

## To Run:
`python run.py`

## To define experiments:
1. Create a new simulator in `run.py`
2. For each desired scheduler, call `run` on the created simulator

## Simulator Metrics Tracked
* overall simulation latency (helps measure overhead costs incurred such as new job pin up and new container spin up)
* containers consumed (helps measure aggregate system cost)
* containers consumer per job (helps measure per-job costs)
* workload time distribution (helps observe long tail latencies of workloads)

## Files
* README.md : This file
* run.py    : Defines all experiments and runs them
* simulator.py : Core simulator that orchestrates containers, workloads over time intervals
* \_\_init__.py  : empty file (for imports)
* container.py : Mimics a container that is capable of housing multiple types of jobs on demand
* workload.py  : Defines the specifications of a workload and how it should be simulated
* scheduler_interface.py  : Base class that defines how a scheduler is to be implemented along with common helpers
* scheduler_ccc.py        : New solution implemented for Cloud Computing Capstone (CCC) class
* scheduler_cypress.py    : Implementation of cypress paper
* scheduler_hermod.py     : Implementation of hermod paper
* scheduler_roundrobin.py : Naive round robin based scheduler

