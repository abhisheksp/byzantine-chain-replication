from constants import *
from message import *
from timer import Timer


class Replica:
    def __init__(self, config, previous_r=None, next_r=None):
        self.id = uuid.uuid4()
        self.running_state = config.init_object
        self.mode = config.mode     # Mode
        self.history = []   # ordered sequence
        self.previous = previous_r
        self.next = next_r
        self.cache = {}
        self.timer = Timer(config.timeout)
        self.olympus = config.olympus
        self.configuration_id = self.configuration_id
        self.type = Type.INTERNAL

    def handle_non_active_mode(self):
        if self.mode == Mode.IMMUTABLE:
            # replica is immutable, send error back to client  
            response = ErrorShuttle(request, 'Error')
            send(sign(response), to=request.client)

    def is_consistent(self, order_statements):
        slots_consistent = all(order_statements[0]['slot'] == order_statement['slot'] for order_statement in order_statements)
        operations_consistent = all(order_statements[0]['operation'] == order_statement['operation'] for order_statement in order_statements)
        
        return slots_consistent and operations_consistent

    def verify_order_proof(self, RequestShuttle):
        order_proof = RequestShuttle['order_proof']
        return is_consistent(order_proof['order_statements'])

    def valid_client(self, request):
        # Check client signature
        # Returns True if client is verified, returns false otherwise 

    # raw request
    def receive_request(self, request):
        client, operation = request
        # verify client
        # drop request if verify failed
        if not valid_client():
            return
        
        # If head is IMMUTABLE
        handle_non_active_mode()
        
        # Replica has the result in its cache
        if (client, operation) in self.cache and self.cache is not None:
            self.send_cached_result(client, operation)

        # Replica recognizes the operation from this client (client ID was cached before)
        elif (client, operation) in self.cache:
            self.handle_recognized_operation(client, operation)
        
        # Replica does not recognize this operation
        else:
            self.handle_new_request(request)

    def send_cached_result(self, client, operation):
        # Get result stored in cache and send it to the client
        result = self.cache[(client, operation)]
        send((result, result_proof), request.client)

    def handle_recognized_operation(self, client, operation):
        timer = self.timer.new_timer()
        timer.start()
        -- receive result shuttle ack  

        # Wait till result shuttle comes back from tail or timer expires        
        await(timer.timed_out() or ResultShuttle((client, operation), _) in received)
        if timer.timed_out():
            reconfigure_request = ReconfigureRequest()
            send(reconfigure_request, to=self.olympus)
            return
        timer.stop()

    def handle_new_request(self, request):
        # request is a tuple of client and operation
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

    def receive_request_shuttle(self, request):
        client = request.client
        # verify client
        operation = request.operation
        # return result if <client_id, operation, result> in cache
        # common
        # verify order_proof
        verification_failed = verify_order_proof(request)
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

        # send <result, result_proof> to client
        # result, result_shuttle = get result shuttle and result from cache
        # TODO: Handle this in receive handlers
        send((result, result_proof), request.client)
        # forward result_proof ack to previous if any
        send(result_shuttle, self.previous)

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

    def receive_checkpoint_request(self, request):
        request[self.id] = (hash(self.running_state), checkpoint_slot)
        send(request, to=self.next)


    def receive_checkpoint_result(self, result):
        result_checkpoint = result[self.id]
        if result_checkpoint[checkpoint_slot] >= len(self.history):
            self.history = self.history[-checkpoint_slot:]
            del result[self.id]
        send(result, to=self.previous)
