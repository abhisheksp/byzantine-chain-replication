from message import *
from constants import *
from timer import Timer


class Head:
    def __init__(self, config, previous_r=None, next_r=None):
        self.id = uuid.uuid4()
        self.running_state = config.init_object
        self.mode = config.mode  # Mode
        self.history = []  # ordered sequence
        self.previous = previous_r
        self.next = next_r
        self.cache = {}
        self.timer = Timer(config.timeout)
        self.type = Type.HEAD
        self.olympus = config.olympus
        self.configuration_id = self.configuration_id

        # TODO: async?
        checkpoint()

    def generate_slot(self):
        # generates increasing id
        pass

    def receive_handler(self, request):
        if self.mode == Mode.IMMUTABLE:
            # send <error>  # TODO: Sign?
            response = ErrorShuttle(request, 'Reconfiguration in progress')
            send(response, to=request.client)
            return

        # call receive_request or receive_request_shuttle or receive_result_shuttle based on request type
        pass

    # raw request
    def receive_request(self, request):
        client, operation = request.client, request.operation
        # verify client         # TODO: error case
        # if invalid client, drop request
        # return cached result if any
        if (client, operation) in self.cache and self.cache is not None:
            # send result to client
            self.send_cached_result(client, operation)
        # recognizes the operation
        elif (client, operation) in self.cache:
            self.handle_recognized_operation(client, operation)
        # new raw request
        else:
            self.handle_new_request(request)

    def send_cached_result(self, client, operation):
        result = self.cache[(client, operation)]
        send((result, result_proof), request.client)

    def handle_recognized_operation(self, client, operation):
        timer = self.timer.new_timer()
        timer.start()
        # -- receive result shuttle ack        # TODO: extract send response to client method
        # client, operation = request.client, request.operation
        await(timer.timed_out() or ResultShuttle((client, operation), _) in received)
        if timer.timed_out():
            send(ReconfigureRequest(), to=self.olympus)
            return
        # cancel_timer on valid result
        timer.stop()
        # send <result, result_proof> to client
        send((result, result_proof), request.client)

    def handle_new_request(self, request):
        client, operation = request
        self.running_state, result = self.running_state(operation)
        # create <slot, operation>
        slot = self.generate_slot()
        order_statement = OrderStatement(request, slot, operation)
        # create request shuttle
        # add sign(order_statement) to order_proof
        signed_order_statement = sign(order_statement)
        order_proof = OrderProof(request, slot, operation, self.configuration_id, [signed_order_statement])
        # add order_proof to history
        self.history.append(order_proof)

        # add sign(result_statement) to result_proof
        result_statement = ResultStatement(request, slot, operation)
        signed_result_statement = sign(result_statement)
        result_proof = ResultProof(request, slot, operation, self.configuration_id, [signed_result_statement])

        # forward Shuttle(<order_proof, result_proof>) if any
        shuttle = Shuttle(request, order_proof, result_proof)
        send(shuttle, to=self.next)
        # cache <client_id, operation, _>
        self.cache[(client, operation)] = None

        # init_timer
        timer = self.timer.new_timer()
        timer.start()
        # -- receive result shuttle ack
        # blocking_wait => valid result
        await(timer.timed_out() or ResultShuttle((client, operation), _) in received)
        if timer.timed_out():
            reconfigure_request = ReconfigureRequest()
            send(reconfigure_request, to=self.olympus)
            return
        # cancel_timer on valid result
        timer.stop()

    def receive_result_shuttle(self, result):
        # verify, Digital Signature verification
        client, operation = result.client, result.operation
        # cache <client_id, operation, result>
        self.cache[(client, operation)] = result

    def receive_wedge_request(self, request):
        # Create a new wedge statement
        wedgeStatement = ('wedged', self.id, self.running_state, self.history)
        # Send the statement to Olympus
        send(wedgeStatement,to=self.olympus)
        # set the replica state to Immutable
        self.mode = 'IMMUTABLE'

    def receive_catchup_messges(self, request):
        #wait until all order proofs are in replica's history
        await(all(order_proof in self.history for order_proof in request))
        #send running state message to Olympus
        send(self.running_state,to=olympus)

# TODO: Checkpoint timer not declared in class variables
    def checkpoint(self):
        while true:
            checkpoint_shuttle = {}
            checkpoint_slot = 100
            checkpoint_shuttle[self.id] = (hash(self.running_state), checkpoint_slot)
            send(checkpoint_shuttle, to=self.next)
            sleep(checkpoint_timer)
    
    def receive_checkpoint_result(self, result):
        result_checkpoint = result[self.id]
        if result_checkpoint[checkpoint_slot] >= len(self.history):
            self.history = self.history[-checkpoint_slot:]
            del result[self.id]
