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
        self.find_quorum(wedge_statements)
        # found quorum
        # get initial_running_state from quorum
        config.initial_running_state = initial_running_state
        config.mode = mode.ACTIVE
        # same number of replicas
        self.configuration = Configuration(config)

    def receive_wedge_statement_handler(self, response):
        # initialize wedge_statements if empty
        # collect all wedge_statements
        pass

    def find_quorum(self, wedge_statements):
        replicas = self.configuration.replicas
        def find_quorum_util():
            current_quorum = select t+1 random wedge_statements
            longest_history_wedge_statement = max(current_quorum, key=history)
            check if longest_history_wedge_statement is consistent with other wedge statements
            if consistent:
              initial_running_state = hash(longest_history_wedge_statement.running_state)
            differences_in_history = [diff_in_history(longest_history_wedge_statement, w) for w in wedge_statements if w != longest_history_wedge_statement)]
            for diff_in_history, replica in differences_in_history:
                  send(CatchupReq, to=replica)
            timer_start
            await(timer_expires or Caughtup(_) in Received)
            if timer expires return False
            else: compare hash(running_state) with initial_running_state for replica
            if all(compare hash(running_state) with initial_running_state for replica):
                return True     # return quorum
            select new quorum
            return False
            pass
        found_quorum = find_quorum_util()
        while not found_quorum:
            found_quorum = find_quorum_util()
        return found_quorum


