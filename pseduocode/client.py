import uuid
from time import sleep

from message import Request
from timer import Timer
from DistAlgoStub import *
from functools import reduce


class Client:
    # Initialize client with configuration
    def __init__(self, config):
        # Generate unique id for each client
        self.id = uuid.uuid4()
        self.timer = Timer(config.timeout)
        self.heartbeat_interval = config.heartbeat_interval
        self.olympus = config.olympus
        self.configuration = config.olympus.get_configuration()
        self.head = self.configuration.get_head()
        self.tail = self.configuration.get_tail()

    # Send request to head
    def send_handler(self, operation):
        # Request uniquely identifies a client, request combination
        request = Request(self.id, operation)
        send(request, to=self.head)

        # start timer
        timer = self.timer.new_timer()
        timer.start()

        -- receive yield point
        # Await until time out or received a response
        await(timer.timed_out() or (request, _) in received)

        # If timeout occurs, retransmit request (broadcast)
        if timer.timed_out():
            self.configuration.broadcast_request((self, operation))
        else:
            timer.stop()

    # Receive result from replica(s)
    def receive_handler(self, response):
        result, result_proof = response
        # Verify result_proof
        quorum_count = config.replica_count/2 + 1
        for  result_statements in result_proof:
            if consistent_results_count(result_statements) < quorum_count:
                # Retransmit(broadcast) in case of validation failure
                self.configuration.broadcast_request((self, operation))
            else:
                # First Result is returned back to the application
                return result_statements[0]

    def configuration_heartbeat(self):
        # heartbeat_interval defines the intervals in which configuration
        # needs to be validated
        while True:
            operation = (HeartBeat, self.configuration)
            request = Request(self.id, operation)
            send(request, to=self.olympus)
            sleep(self.heartbeat_interval)

    def receive_reconfigure_handler(self, response):
        new_configuration = response
        self.configuration = new_configuration
        self.head = self.configuration.get_head()
        self.tail = self.configuration.get_tail()

    # Compute number of consistent result statements in the result proof
    def consistent_results_count(self, result_statements):
        def reducer(result_statement):
            return int(check_statement.slot == result_statement.slot
                       and check_statement.operation == result_statement.operation)
        return reduce(lambda x, y: x + reducer(y), result_statements, 0)
