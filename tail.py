from constants import *
from message import *
from timer import Timer


class Tail:
    def __init__(self, config, previous_r=None, next_r=None):
        self.id = uuid.uuid4()
        self.running_state = config.init_object
        self.mode = config.mode  # Mode
        self.history = []  # ordered sequence
        self.previous = previous_r
        self.next = next_r
        self.cache = {}
        self.timer = Timer(config.timeout)
        self.configuration_id = self.configuration_id
        self.olympus = config.olympus
        self.type = Type.TAIL
        self.type = Type.INTERNAL

    def is_consistent(self, order_statements):
        slots_consistent = all(order_statements[0]['slot'] == order_statement['slot'] for order_statement in order_statements)
        operations_consistent = all(order_statements[0]['operation'] == order_statement['operation'] for order_statement in order_statements)
        
        if slots_consistent and operations_consistent:
            return true
        else:
            return false

    def verify_order_proof(self, RequestShuttle):
        order_proof = RequestShuttle['order_proof']
        return is_consistent(order_proof['order_statements'])

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
        client, operation = request
        # verify client         # TODO: error case
        # drop request if verify failed
        # return cached result if any
        if (client, operation) in self.cache and self.cache is not None:
            # send result to client
            self.send_cached_result(client, operation)
        # recognizes the operation
        elif (client, operation) in self.cache:
            self.handle_recognized_operation(client, operation)
        else:
            self.handle_new_request(request)

    def handle_new_request(self, request):
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
            reconfigure_request = ReconfigureRequest()
            send(reconfigure_request, to=self.olympus)
            return

        # cancel_timer on valid result          # TODO: error case
        timer.stop()

    def send_cached_result(self, client, operation):
        result = self.cache[(client, operation)]
        send((result, result_proof), request.client)

    def handle_recognized_operation(self, client, operation):
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

    def receive_request_shuttle(self, request):
        client = request.client
        # verify client
        operation = request.operation
        # return result if <client_id, operation, result> in cache
        # verify order_proof
        verification_failed = verify_order_proof(request)
        if verification_failed:
            reconfigure_request = ReconfigureRequest()
            send(reconfigure_request, to=self.olympus)
            return
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
        # TODO: Handle in response handler
        # send <result, result_proof> to client
        # result, result_shuttle = get result shuttle and result from cache
        send((result, result_proof), request.client)
        # forward result_proof ack to previous
        send(result_shuttle, self.previous)

    def receive_wedge_request(self, request):
        # Create a new wedge statement
        wedgeStatement = ('wedged', self.id, self.running_state, self.history)
        # Send the statement to Olympus
        send(wedgeStatement, to=self.olympus)
        # set the replica state to Immutable
        self.mode = 'IMMUTABLE'

#TODO: Checkpoint timer not declared in class variables
    def receive_catchup_messages(self, request):
        # wait until all order proofs are in replica's history
        await(all(order_proof in self.history for order_proof in request))
        # send running state message to Olympus
        send(self.running_state, to=olympus)


    def receive_checkpoint_request(self, request):
        request[self.id] = (hash(self.running_state), checkpoint_slot)
        result_checkpoint = request[self.id]
        if result_checkpoint[checkpoint_slot] >= len(self.history):
            self.history = self.history[-checkpoint_slot:]
            del request[self.id]
        send(request, to=self.previous)