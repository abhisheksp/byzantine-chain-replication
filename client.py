import uuid

from message import Request
from timer import Timer
from DistAlgoStub import *


class Client:
    # Initialize client with configuration
    def __init__(self, config):
        # generate unique id for each client
        self.id = uuid.uuid4()
        self.timer = Timer(config.timeout)
        self.olympus = config.olympus
        self.configuration = config.olympus.get_configuration()
        self.head = self.configuration.get_head()
        self.tail = self.configuration.get_tail()

    # Send Request
    def send_handler(self, operation):
        # send request to head
        # request uniquely identifies a client, request combination
        request = Request(self.id, operation)
        send(request, to=self.head)

        # init_timer
        timer = self.timer.new_timer()
        timer.start()
        # -- receive yield point
        # await until time out or received
        await(timer.timed_out() or (request, _) in received)

        # timeout
        if timer.timed_out():    # TODO: | error
            self.configuration.broadcast_request((self, operation))
        else:
            timer.stop()

    # Receive
    def receive_handler(self, response):
        receive(response)
        # verify result_proof
