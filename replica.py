class Replica:
    def __init__(self, config, previous_r=None, next_r=None):
        self.running_state = config.init_object
        self.mode = config.mode     # ACTIVE, PENDING, OR IMMUTABLE
        self.history = []   # ordered sequence
        self.previous = previous_r
        self.next = next_r
        self.cache = {}

        if previous_r is None:
            self.type = 'HEAD'
        elif next_r is None:
            self.type = 'TAIL'
        else:
            self.type = 'INTERNAL'
        pass

    def receive(self, request):
        if self.mode == 'IMMUTABLE':
            # send <error>
            pass
        # call receive_request or receive_request_shuttle or receive_result_shuttle based on request type
        pass

    # raw request
    def receive_request(self, request):
        client = request.client
        # verify client         # TODO: error case
        operation = request.operation

        # return cached result if any
        if (client, operation) in self.cache and self.cache is not None:
            return self.cache[(client, operation)]
        # recognizes the operation
        elif (client, operation) in self.cache:
            # init_timer
            # -- receive result shuttle ack         # TODO: extract send response to client method
            # blocking_wait => valid result
            # cancel_timer on valid result          # TODO: error case
            # send <result, result_proof> to client
            # forward result_proof ack to previous if any
            return
        if self.type == 'HEAD':
            # create <slot, operation>
            # create request shuttle
            pass
        else:
            # forward to head # previous?
            # init_timer
            # -- receive result shuttle ack
            # blocking_wait => valid result
            # cancel_timer on valid result          # TODO: error case
            # send <result, result_proof> to client
            # forward result_proof ack to previous if any

            pass
        # common
        self.running_state, result = self.running_state(operation)
        # add sign(order_statement) to order_proof
        # add order_proof to history

        # cache <client_id, operation, _>
        self.cache[(client, operation)] = None

        # add sign(result_statement) to result_proof
        # forward Shuttle(<order_proof, result_proof>) if any
        # init_timer
        # -- receive result shuttle ack
        # blocking_wait => valid result
        # cancel_timer on valid result
        pass

    def receive_request_shuttle(self, request):
        client = request.client
        # verify client
        operation = request.operation
        # return result if <client_id, operation, result> in cache
        # common
        # verify order_proof
        self.running_state, result = self.running_state(operation)
        # add sign(order_statement) to order_proof
        # add order_proof to history
        self.cache[(client, operation)] = None
        # add sign(result_statement) to result_proof
        # forward Shuttle(<order_proof, result_proof>) if any
        if self.type == 'TAIL':
            # send <result, result_proof> to client
            # forward result_proof ack to previous
            pass
        else:
            # init_timer
            # -- receive result proof ack
            # blocking_wait => valid result
            # cancel_timer on valid result
            pass
        pass

    def receive_result_shuttle(self, result):
        # verify, Digital Signature verification
        client, operation = result.client, result.operation
        # cache <client_id, operation, result>
        self.cache[(client, operation)] = result
        # forward result_shuttle to previous if any
        pass

    def send(self, response, to):
        # send <response, to>
        pass
