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
        self.mode = config.mode     # Mode
        self.history = []   # ordered sequence
        self.previous = previous_r
        self.next = next_r
        self.cache = {}
        self.timer = Timer(config.timeout)

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
        # drop request if verify failed
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
                reconfigure_request = ReconfigureRequest()
                send(reconfigure_request, to=self.olympus)
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
                reconfigure_request = ReconfigureRequest()
                send(reconfigure_request, to=self.olympus)
                return

            # cancel_timer on valid result          # TODO: error case
            timer.stop()
            # send <result, result_proof> to client
            result, result_shuttle = get result shuttle and result from cache
            send((result, result_proof), request.client)
            # forward result_proof ack to previous if any
            if self.previous:
                send(result_shuttle, self.previous)


    def receive_request_shuttle(self, request):
        client = request.client
        # verify client
        operation = request.operation
        # return result if <client_id, operation, result> in cache
        # common
        # verify order_proof
        if verification_failed:
            reconfigure_request = ReconfigureRequest()
            send(reconfigure_request, to=self.olympus)
            return
        self.running_state, result = self.running_state(operation)
        # add sign(order_statement) to order_proof
        # add order_proof to history
        self.cache[(client, operation)] = None
        # add sign(result_statement) to result_proof
        result_statement = ResultStatement(request, slot, operation)
        signed_result_statement = sign(result_statement)
        result_statements = request.order_proof.orderstatments + [signed_result_statement]
        result_proof = ResultProof(request, slot, operation, self.configuration_id, result_statements)
        # forward Shuttle(<order_proof, result_proof>)
        shuttle = Shuttle(request, order_proof, result_proof)
        send(shuttle, to=self.next)
        # cache <client_id, operation, _>
        self.cache[(client, operation)] = None
        timer = self.timer.new_timer()
        timer.start()
        # -- receive result shuttle ack
        # blocking_wait => valid result
        await(timer.timed_out() or ResultShuttle((client, operation), _) in received)
        if timer.timed_out():
            # TODO: Handle error case
            # verify order_proof
            reconfigure_request = ReconfigureRequest()
            send(reconfigure_request, to=self.olympus)
            return
        # cancel_timer on valid result
        timer.stop()

    # TODO: consistency
    def receive_result_shuttle(self, result):
        # verify, Digital Signature verification
        client, operation = result.client, result.operation
        # cache <client_id, operation, result>
        self.cache[(client, operation)] = result
        # forward result_shuttle to previous
        pass

#TODO: Add self.id and self.olympus
    def receive_wedge_request(self, request):
        # Create a new wedge statement
        wedgeStatement = ('wedged', self.id, self.running_state, self.history)
        #Send the statement to Olympus
        send(wedgeStatement,to=self.olympus)
        #set the replica state to Immutable
        self.mode = 'IMMUTABLE'


    def receive_catchup_messges(self, request):
        #wait until all order proofs are in replica's history
        await(all(order_proof in self.history for order_proof in request))
        #send running state message to Olympus
        send(self.running_state,to=olympus)
