from enum import Enum
from message import *
from timer import Timer


class Mode(Enum):
    ACTIVE = 1
    PENDING = 2
    IMMUTABLE = 3


class Type(Enum):
    HEAD = 1
    INTERNAL = 2
    TAIL = 3


class Replica:
    def __init__(self, config, previous_r=None, next_r=None):
        self.running_state = config.init_object
        self.mode = config.mode  # Mode
        self.history = []  # ordered sequence
        self.previous = previous_r
        self.next = next_r
        self.cache = {}
        self.timer = Timer(config.timeout)
        self.configuration_id = self.configuration_id

        if next_r is None:
            self.type = Type.TAIL
        else:
            self.type = Type.INTERNAL

    def receive_handler(self, request):
        if self.mode == Mode.IMMUTABLE:
            # send <error>  # TODO: Sign?
            response = ErrorShuttle(request, 'Reconfiguration in progress')
            signed_response = sign(response)
            send(signed_response, to=request.client)
            return

        # call receive_request or receive_request_shuttle or receive_result_shuttle based on request type
        pass

    # raw request
    def receive_request(self, request):
        client = request.client
        # verify client         # TODO: error case
        operation = request.operation

        # return cached result if any
        if (client, operation) in self.cache and self.cache is not None:
            # send result to client
            result = self.cache[(client, operation)]
            send((result, result_proof), request.client)
        # recognizes the operation
        elif (client, operation) in self.cache:
            timer = self.timer.new_timer()
            timer.start()
            # -- receive result shuttle ack        # TODO: extract send response to client method
            client, operation = request.client, request.operation
            await(timer.timed_out() or ResultShuttle((client, operation), _) in received)
            if timer.timed_out():
                # TODO: Handle error case
                return
            # cancel_timer on valid result
            timer.stop()
            # send <result, result_proof> to client
            send((result, result_proof), request.client)
            # forward result_proof ack to previous if any
            send(result_proof, self.previous)
            return
        else:
            # forward to head # previous?
            send(request, to=self.previous)
            # init_timer
            timer = self.timer.new_timer()
            timer.start()
            # -- receive result shuttle ack
            client, operation = request.client, request.operation
            # blocking_wait => valid result
            await(timer.timed_out() or ResultShuttle((client, operation), _) in received)
            if timer.timed_out():
                # TODO: Handle error case
                return

            # cancel_timer on valid result          # TODO: error case
            timer.stop()
            # send <result, result_proof> to client
            result, result_shuttle = get
            result
            shuttle and result
            from cache
            send((result, result_proof), request.client)
            # forward result_proof ack to previous if any
            if self.previous:
                send(result_shuttle, self.previous)

    def receive_request_shuttle(self, request):
        client = request.client
        # verify client
        operation = request.operation
        # return result if <client_id, operation, result> in cache
        # verify order_proof
        self.running_state, result = self.running_state(operation)
        order_statement = OrderStatement(request, slot, operation)
        signed_order_statement = sign(order_statement)
        order_statements = request.order_proof.orderstatments + [signed_order_statement]
        # add sign(order_statement) to order_proof
        order_proof = OrderProof(request, slot, operation, self.configuration_id, order_statements)
        # add order_proof to history
        self.history.append(order_proof)
        self.cache[(client, operation)] = None
        # add sign(result_statement) to result_proof
        result_statement = ResultStatement(request, slot, operation)
        signed_result_statement = sign(result_statement)
        result_statements = request.order_proof.orderstatments + [signed_result_statement]
        result_proof = ResultProof(request, slot, operation, self.configuration_id, result_statements)
        # send <result, result_proof> to client
        send(result, result_proof, to=client)
        # forward result_proof ack to previous
        send(ResultShuttle(), to=self.previous)     #TODO: verify


    # TODO: consistency
    def receive_result_shuttle(self, result):
        # verify, Digital Signature verification
        client, operation = result.client, result.operation
        # cache <client_id, operation, result>
        self.cache[(client, operation)] = result
        # forward result_shuttle to previous
        pass

