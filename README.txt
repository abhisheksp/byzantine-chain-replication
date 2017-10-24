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
1. When the result shuttle propagates upstream from the tail back to the head, change_operation() and change_result() triggers do not raise reconfigure request.
2. Forward request trigger does not verify failures for change_result() and drop_result_statement(). However, these failures can be detected by the algorithm itself. 
3. Heisenbug: WARNING: Caught exception while processing router message from <..>. Happens rarely and not reproducible.

CONTRIBUTIONS:

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
    config.txt
	forward_request_operation_change.txt
	multiple_client_workload.txt
	order_proof_verification.txt
	result_proof_verification.txt
	single_client_workload.txt
	stress_1000_3_10.txt
	stress_1000_7_10.txt
	stress_2000_11_1.txt

CODE SIZE.
-------------------------------------------------------------------------------
Language                     files          blank        comment           code
-------------------------------------------------------------------------------
Python                          19            222            153            816
DAL                              4             75              0            611
Bourne Shell                    15             16              0            122
Markdown                         1              0              0              2
-------------------------------------------------------------------------------
SUM:                            39            313            153           1551
-------------------------------------------------------------------------------

Numbers of non-blank non-comment lines of code - 1551
Algorithm: 434
Other: 1117
Total:  1551



LANGUAGE FEATURE USAGE. 
Count of
List comprehensions: 0
Map(Alternative to List comprehension): 7
Lambdas: 7
Dictionary comprehensions: 4
Set comprehensions: 0
Aggregations: 0
Quantifications: 2