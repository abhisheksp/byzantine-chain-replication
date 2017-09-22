from timer import Timer


class Client:
    # Initialize client with configuration
    def __init__(self, config):
        # Init with client with config
        # service details: {head}, {replicas}
        # timeout value
        # takes timer?
        self.timer = Timer(config.timeout)
        self.olympus = config.olympus
        self.configuration = config.olympus.get_configuration()
        self.head = self.configuration.get_head()
        self.tail = self.configuration.get_tail()
        pass

    # Send Request
    def send(self, operation):
        # send <o> to service.head
        # init_timer      # TODO: request identifier
        timer = self.timer.new_timer()
        timer.init_timer()
        # receive yield point
        # timeout yield point
        # -- blocking_wait #await until time out or received
        valid_result = None
        if valid_result:    # TODO: | error
            timer.cancel()
        else:
            # timeout
            self.configuration.broadcast_request((self, operation))
        pass

    # Receive
    def receive(self, response):
        # receive <result, result_proof>
        # verify result_proof
        pass

