PLATFORM: 
DistAlgo Version: 1.0.9
Python Version: 3.6.3
OS: Mac OS X 
Types of Hosts: 2 Laptops (Without any VMs)

INSTRUCTIONS:
Install Python 3.x
http://docs.python-guide.org/en/latest/starting/installation/
Install pip (Comes with Python 3.x)

Install DistAlgo:

Commands to install Distalgo:
pip install pyDistAlgo

Alternative methods to install Distalgo is available here:
https://github.com/DistAlgo/distalgo

To run individual distalgo program:
Command: python -m da <SOURCE>

To run project:
command: cd src
command: bash run.sh
This starts the pseudorandom workload for a single client.
Other possible workloads:
Single Client Workload
Multiple Client Workload


Limitations/Bugs of existing implementation:
1. Multihost - Since we run replicas on a container which is on a different host (on top of a VM), all timeouts needs to be larger than usual.
2. Retransmissions that occur after head or a non-head replica timeouts can sometimes cause multiple rounds of reconfigurations.
3. Trigger new_configuration(x) works only as failure[x,_]
4. Fails in parsing (c, m) pairs in configurations where c, m is more than one digit long
5. Consistency checks in client is not automated for all configurations. It is done manually.
6. Catchup messages from Olympus are not verified by replicas

CONTRIBUTIONS:

Contributions from Abhishek:
Setting up nodes on containers, checkpointing (with failure injection), Multihost setup, Replica node orchastration, infrastructure setup.

Contributions from Abhilash:
Reconfiguration - Algorithm and Implementation (with failure injection)

All other portions/cases - Pair Programming


MAIN FILES:
/src
	main.da
	client.da
	replica.da
	olympus.da

/log
	replica.log
	client.log
	olympus.log

/config
    config.txt
	forward_request_operation_change.txt
	multiple_client_workload.txt
	order_proof_verification.txt
	result_proof_verification.txt
	single_client_workload.txt
	stress_1000_3_10.txt
	stress_1000_7_10.txt
	stress_2000_11_1.txt



Numbers of non-blank non-comment lines of code - 2219
Algorithm: 1110
Test cases: 1109




LANGUAGE FEATURE USAGE. 
Count of
List comprehensions: 1
Map(Alternative to List comprehension): 8
Lambdas: 9
Dictionary comprehensions: 6
Set comprehensions: 0
Aggregations: 0
Quantifications: 2