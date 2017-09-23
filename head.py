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
        self.current_slot_id = 0
        # Head initiates checkpointing
        checkpoint()

    def generate_slot(self):
        self.current_slot_id += 1
        return self.current_slot_id

    def handle_non_active_mode(self):
        if self.mode == Mode.IMMUTABLE:
            # replica is immutable, send error back to client  
            response = ErrorShuttle(request, 'Error')
            send(sign(response), to=request.client)

    def valid_client(self, request):
        # Check client signature
        # Returns True if client is verified, returns false otherwise 

    # raw request
    def receive_request(self, request):
        client, operation = request.client, request.operation
        if not valid_client(): 
            #drop request
            return

        # If head is IMMUTABLE
        handle_non_active_mode()

        # return cached result if any
        if (client, operation) in self.cache and self.cache is not None:
            # send result to client
            self.send_cached_result(client, operation)
        # Head recognizes the operation from this client (client ID was cached before)
        elif (client, operation) in self.cache:
            self.handle_recognized_operation(client, operation)
        # Handle new request from client
        else:
            self.handle_new_request(request)

    def send_cached_result(self, client, operation):
        # get result stored in cache and send it to the client
        result = self.cache[(client, operation)]
        send((result, result_proof), request.client)

    def handle_recognized_operation(self, client, operation):
        timer = self.timer.new_timer()
        timer.start()
        -- receive result shuttle ack 
        # Wait till result shuttle comes back from tail or timer expires        
        await(timer.timed_out() or ResultShuttle((client, operation), _) in received)
        if timer.timed_out():
            send(ReconfigureRequest(), to=self.olympus)
            return
        timer.stop()

    def handle_new_request(self, request):
        # request is a tuple of client and operation
        client, operation = request
        self.running_state, result = self.running_state(operation)
        
        # Head generates slots for new operations
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

        # cache client_id and operation
        self.cache[(client, operation)] = None
        
        # Forward Shuttle to next replica
        shuttle = Shuttle(request, order_proof, result_proof)
        send(shuttle, to=self.next)
        
        # Initialize and start timer
        timer = self.timer.new_timer()
        timer.start()
        
        -- receive result shuttle ack
        
        # Wait untill result shuttle comes back from the tail or timer expires
        # Send 'reconfigure-request' to olympus if timer expires
        await(timer.timed_out() or ResultShuttle((client, operation), _) in received)
        if timer.timed_out():
            reconfigure_request = ReconfigureRequest()
            send(reconfigure_request, to=self.olympus)
            return
        timer.stop()

    def receive_result_shuttle(self, result):
        # Signature verification
        client, operation = result.client, result.operation
        
        # cache client_id, operation and result
        self.cache[(client, operation)] = result
        
        # send <result, result_proof> to client
        send((result, result_proof), request.client)

    def receive_wedge_request(self, request):
        # Create a new wedge statement
        wedgeStatement = ('wedged', self.id, self.running_state, self.history)
        
        # Send wedge statement to Olympus
        send(wedgeStatement,to=self.olympus)
        
        # set the replica mode to Immutable
        self.mode = Mode.IMMUTABLE

    def receive_catchup_messages(self, request):
        # Wait until all order proofs are in replica's history
        await(all(order_proof in self.history for order_proof in request))
        # Send running state message to Olympus
        send(self.running_state,to=olympus)


    def checkpoint(self):
        # Assumed chekpoint slot = 100
        while True:
            # Head creates and sends checkpoint shuttle along the chain
            checkpoint_shuttle = {}
            checkpoint_slot = 100
            checkpoint_shuttle[self.id] = (hash(self.running_state), checkpoint_slot)
            send(checkpoint_shuttle, to=self.next)
            sleep(checkpoint_timer)
    
    def receive_checkpoint_result(self, result):
        result_checkpoint = result[self.id]
        # If head's history is greater than the checkpoint slot,
        # truncate history and remove checkpoint entry from the shuttle
        if result_checkpoint[checkpoint_slot] >= len(self.history):
            self.history = self.history[-checkpoint_slot:]
            del result[self.id]
