from configuration import Configuration
from message import WedgeRequest


class Olympus:
    def __init__(self, config):
        self.config = config
        self.configuration = Configuration(config.config)

    def request_reconfiguration_handler(self):
        # broadcast wedge request to all replicas
        self.configuration.broadcast_request(WedgeRequest())
        -- wedge statement yield point

        # find Quorum
        quorum = self.find_quorum(wedge_statements)

        # get initial_running_state from quorum
        config.initial_running_state = quorum.initial_running_state

        # replace with new configuration
        self.configuration = Configuration(config)

    def select_quorum(self, quorum_count):
        quorum = randomly select wedge statements of quorum_count number of replicas
        return quorum

    def receive_wedge_statement_handler(self, response):
        # await until all wedge statements arrive
        await(all(wedge_statements) in received)

    def is_history_consistent(self, history1, history2):
        # check for (slot, order) pair consistency in order proofs
        for order_proof1, order_proof2 in zip(history1, history2):
            if order_proof1.slot == order_proof2.slot and order_proof1.operation != order_proof2.operation:
                return False
        return True

    def find_quorum(self, wedge_statements):        
        replicas = self.configuration.replicas

        def find_quorum_util():
            # find t+1 value
            quorum_count  = (self.configuration.replica_count/2) + 1
            current_quorum = select_quorum(quorum_count)
            # select wedge statement with logest history
            longest_history_wedge_statement = max(current_quorum, key=history)
            other_wedge_statements = wedge_statements - longest_history_wedge_statement

            # check for consistency between longest and other histories
            longest_history = longest_history_wedge_statement.history
            for wedge_statement in other_wedge_statements:
                current_history = wedge_statement.history
                if not is_history_consistent(current_history, longest_history):
                    return None

            initial_running_state = hash(longest_history_wedge_statement.running_state)
            differences_in_history = [diff_in_history(longest_history_wedge_statement, wedge_statement)
                                      for wedge_statement in other_wedge_statements)]

            # send catch up requests for each difference in history
            for diff_in_history, replica in differences_in_history:
                  send(CatchupRequest, to=replica)

            # await until all caught up messages are received
            await(Caughtup(_) in Received)
            # check if running states are consistent
            is_states_consistent = all(initial_running_state == running_state
                                     for replica.running_state in CaughtUpReplicas)
            if is_states_consistent:
                quorum = (initial_running_state)
                return quorum
            else:
                return None

        # repeat until valid quorum is found
        found_quorum = find_quorum_util()
        while not found_quorum:
            found_quorum = find_quorum_util()
        return found_quorum


