from constants import *
from message import *
from timer import Timer


class Replica:
    def __init__(self, config, previous_r=None, next_r=None):
        self.id = uuid.uuid4()
        self.running_state = config.init_object
        self.mode = Mode.ACTIVE
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
        slots_consistent = all(order_statements[0]['slot'] == order_statement['slot']
                               for order_statement in order_statements)
        operations_consistent = all(order_statements[0]['operation'] == order_statement['operation']
                                    for order_statement in order_statements)
        
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
        
        # If replica is IMMUTABLE
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
        # Validate client
        if not valid_client():
            return
        
        # Send request to head along the chain
        send(request, to=self.previous)
        
        # Initialize and start timer
        timer = self.timer.new_timer()
        timer.start()
        -- receive result shuttle ack
        client, operation = request.client, request.operation
        
        # Wait until result shuttles comes back from tail or timer expires
        # Send 'reconfigure-request' to olympus if timer expires
        await(timer.timed_out() or ResultShuttle((client, operation), _) in received)
        if timer.timed_out():
            reconfigure_request = ReconfigureRequest()
            send(reconfigure_request, to=self.olympus)
            return
        timer.stop()

    def receive_request_shuttle(self, request_shuttle):
        # request is a shuttle containing orderproof and resultproofs
        # Extract client ID, operation, and request ID from orderproof
        client = request_shuttle.order_proof.client
        operation = request_shuttle.order_proof.operation
        request = request_shuttle.order_proof.operation
        
        # Validate received order_proof in shuttle
        verification_failed = verify_order_proof(request)
        if verification_failed:
            reconfigure_request = ReconfigureRequest()
            send(reconfigure_request, to=self.olympus)
            return

        # Apply operation to the running state and get result
        self.running_state, result = self.running_state(operation)

        # Create order_proof
        order_statement = OrderStatement(request, slot, operation)
        signed_order_statement = sign(order_statement)
        order_statements = request_shuttle.order_proof.orderstatments + [signed_order_statement]
        order_proof = OrderProof(request, slot, operation, self.configuration_id, order_statements)
        
        # add order_proof to history
        self.history.append(order_proof)

        # cache client ID and operation
        self.cache[(client, operation)] = None
        
        # add sign(result_statement) to result_proof
        result_statement = ResultStatement(request, slot, operation)
        signed_result_statement = sign(result_statement)
        result_statements = request.order_proof.orderstatments + [signed_result_statement]
        result_proof = ResultProof(request, slot, operation, self.configuration_id, result_statements)
        
        # forward Shuttle to the next replica
        shuttle = Shuttle(request, order_proof, result_proof)
        send(shuttle, to=self.next)
        
        # Initialize and start timer
        timer = self.timer.new_timer()
        timer.start()
        -- receive result shuttle ack
        
        # Wait until result shuttle comes back from client or timer expires
        await(timer.timed_out() or ResultShuttle((client, operation), _) in received)

        # Send 'reconfigure-request' to Olympus if timed out
        if timer.timed_out():
            reconfigure_request = ReconfigureRequest()
            send(reconfigure_request, to=self.olympus)
            return
        timer.stop()

    def receive_result_shuttle(self, result_shuttle):
        # Perform Signature verification
        client, operation = result_shuttle.client, result_shuttle.operation
        
        # cache client_id, operation and result
        self.cache[(client, operation)] = result_shuttle.result
        # forward result_shuttle to previous

        # send <result, result_proof> to client
        send((result, result_proof), request.client)
        
        # forward result_shuttle to previous replica
        send(result_shuttle, self.previous)

    def receive_wedge_request(self, request):
        # Create a new wedge statement
        wedgeStatement = ('wedged', self.id, self.running_state, self.history)
        
        #Send the statement to Olympus
        send(wedgeStatement,to=self.olympus)
        
        #set the replica state to Immutable
        self.mode = Mode.IMMUTABLE

    def receive_catchup_messages(self, request):
        #wait until all order proofs are in replica's history
        await(all(order_proof in self.history for order_proof in request))
        #send running state message to Olympus
        send(self.running_state,to=olympus)

    def receive_checkpoint_request(self, checkpoint_shuttle):
        # Replica hashes its running state and adds it to checkpoint shuttle
        # Send shuttle to the next replica
        checkpoint_shuttle[self.id] = (hash(self.running_state), checkpoint_slot)
        send(checkpoint_shuttle, to=self.next)

    def receive_checkpoint_result(self, result_checkpoint_shuttle):
        result_checkpoint = result_checkpoint_shuttle[self.id]
        # If replica's history is greater than the checkpoint slot,
        # truncate history and remove checkpoint entry from the shuttle
        if result_checkpoint[checkpoint_slot] >= len(self.history):
            self.history = self.history[-checkpoint_slot:]
            del result_checkpoint_shuttle[self.id]
        send(result_checkpoint_shuttle, to=self.previous)
