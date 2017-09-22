import uuid

from message import Request
from timer import Timer
from DistAlgoStub import *


class Client:
    # Initialize client with configuration
    def __init__(self, config):
        # Generate unique id for each client
        self.id = uuid.uuid4()
        self.timer = Timer(config.timeout)
        self.olympus = config.olympus
        self.configuration = config.olympus.get_configuration()
        self.head = self.configuration.get_head()
        self.tail = self.configuration.get_tail()
    
    # Compute number of consistent result statemens in the result proof 
    def consistent_results_count(self, result_statements):
        count = 0
        check_statement = result_statements[0]
        for result_statement in result_statements:
            if check_statement.slot == result_statements.slot and check_statement.operation == result_statements.operation:
                count++
        return count


    # Send request to head
    def send_handler(self, operation):
        # Request uniquely identifies a client, request combination
        request = Request(self.id, operation)
        send(request, to=self.head)

        # Initialize  and timer
        timer = self.timer.new_timer()
        timer.start()

        -- receive yield point
        # Await until time out or received a response
        await(timer.timed_out() or (request, _) in received)

        # If timeout occurs, retransmit request (broadcast)
        if timer.timed_out():    # TODO: | error
            self.configuration.broadcast_request((self, operation))
        else:
            timer.stop()

    # Receive result from replica(s)
    def receive_handler(self, response):
        result, result_proof = response
        # Verify result_proof
        for  result_statements in result_proof:
        if(consistent_results_count(result_statements) < (config.replica_count)/2 + 1):
            # Retransmit(broadcast) in case of validation failure 
            self.configuration.broadcast_request((self, operation))
        else:
            # First Result is returned back to the application
            return result_statements[0]

