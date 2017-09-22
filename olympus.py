from configuration import Configuration
from message import WedgeRequest


class Olympus:
    def __init__(self, config):
        self.config = config
        self.configuration = Configuration(config.config)

    def request_reconfiguration_handler(self):
        wedge_request = WedgeRequest()
        self.configuration.broadcast_request(wedge_request)
        -- wedge statement yield point
        # find Quorum
        quorum = self.find_quorum(wedge_statements)
        # found quorum
        # get initial_running_state from quorum
        config.initial_running_state = quorum.initial_running_state
        config.mode = mode.ACTIVE
        # same number of replicas
        self.configuration = Configuration(config)
    def selectQuorum(self, quorum_count):
        #return wedge statements of quorum_count number of replicas, randomly
        pass

    def receive_wedge_statement_handler(self, response):
        await(wedge_statements in received)
        

    def is_consistent(self, history1, history2):
        for order_proof1, order_proof2 in zip(history1, history2):
            if order_proof1.slot == order_proof2.slot and order_proof1.operation != order_proof2.operation:
                return False;
        return True;

    def find_quorum(self, wedge_statements):        
        replicas = self.configuration.replicas
        def find_quorum_util():
            quorum_count  = (self.replica_count/2) + 1
            current_quorum = selectQuorum(quorum_count)
            longest_history_wedge_statement = max(current_quorum, key=history)
            other_wedge_statements= wedge_statements - longest_history_wedge_statement
            for wedge_statement in other_wedge_statements:
                if not is_consistent(wedge_statement.history, longest_history_wedge_statement.history):
                    return None
            initial_running_state = hash(longest_history_wedge_statement.running_state)
            differences_in_history = [diff_in_history(longest_history_wedge_statement, w) for w in wedge_statements if w != longest_history_wedge_statement)]
            for diff_in_history, replica in differences_in_history:
                  send(CatchupReq, to=replica)
            timer_start()
            await(timer_expires or Caughtup(_) in Received)
            if timer expires return None
            elif not all(initial_running_state == running_state for replica.running_state in CaughtUpReplicas):
                return None
            return quorum = (initial_running_state)
        found_quorum = find_quorum_util()
        while not found_quorum:
            found_quorum = find_quorum_util()
        return found_quorum


