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


Limitations of existing implementation:
1. When the result shuttle propogates upstream from the tail back to the head, change_operation() and change_result() triggers do not raise reconfigure request.
2. Forward request trigger does not verify failures for change_result() and drop_result_statement(). However, these failures can be detected by the algorithm itself. 
3. Intermittent error: "Does not resolve names" when running multiple_client_workload. Reason is not yet clear to us.


CONTRIBUTIONS (not entirely accurate): 

Contributions from Abhishek:
Replica - Handling client request. Signature Verification. Order Proofs, Result Proofs, Order Proof Validation
Main process setup. 
Designing all clases required in the project classes.
Failure Injection 6 cases


Contributions from Abhilash:
Olympus, Client: Handling and receiving requests. Signature Verifications at the client side. Creating process and keys.
Failure Injection 6 cases.
Logging
Documentation

All other portions/cases - Pair Programming


MAIN FILES:
/src
	main.da
	client.da
	replica.da
	olympus.da

/log
	main.log
	client.log

/config
	_____

CODE SIZE.  
Numbers of non-blank non-comment lines of code -
Algorithm: ___
Other: ____
Total:  ____


LANGUAGE FEATURE USAGE. 
Count of
List comprehensions (Python): ______
Dictionary comprehensions (Python): ________
Set comprehensions (DistAlgo): ________
Aggregations and quantifications (DistAlgo): ______