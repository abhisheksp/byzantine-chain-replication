class Client:
    # Initialize client with configuration
    def __init__(self, config):
        # Init with client with config
        # service details: {head}, {replicas}
        # timeout value
        # takes timer?
        # self.timeout = config.timeout
        self.olympus = config.olympus
        self.head = self.olympus.configuration.get_head()
        self.tail = self.olympus.configuration.get_tail()
        pass

    # Send Request
    def send(self, operation):
        # service details obtained from initial config
        # send <o> to service.head
        # init_timer      # TODO: request identifier
        # receive yield point
        # blocking_wait => valid result # TODO: | error | timeout
        pass

    # Receive
    def receive(self, response):
        # receive <result, result_proof>
        # verify result_proof
        pass

    def timer(self):
        # start_timer                   # TODO: model timer
        # timed_out? raise error
        # cancel_request? cancel_timer
        pass
