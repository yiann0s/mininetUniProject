# mininetUniProject
A simulation of a network topology of mobile nodes where a video is being transmitted.
The library used is a fork of mininet, an emulator for Software Defined Networking.
Running different senarios, user performs network tests.

Project - Walkthrough
    4 cars, 2 eNodeBs, 1 RSU (Road Side Unit), ovs, controller,
client (safety center)

The experiment has 3 phases:
    Phase 1: 3-hop V2V communication between the cars (in-
band controlling) & V2I connectivity between car3 and
eNodeB1
    Phase 2: V2I communication between car0 and RSU, eNodeB2
    Phase 3: V2I communication between car0 eNodeB2

   Task 1: Run the scenario described in the paper (IEEE-
Access 2017 – From theory to Experimental Evaluation:
Resource Management in Software-Defined Vehicular
Networks)

   Calculate measurements: Throughput, Packet loss, jitter,
latency for each phase
    Use bonding of interfaces in car0 if you want
    
   Task 2: Run in the same topology but with one car using
bicasting
    Calculate measurements: Throughput, Packet loss, jitter,
latency

Measurements performed include the output of iperf, ifconfig and ping commands.

