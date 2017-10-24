import json
import unittest

import os


class StateTest(unittest.TestCase):
    def test_state_equality(self):
        replica_count = 11
        replica_states = []
        parent_dir = os.path.abspath(os.pardir)
        logs_dir = 'logs'

        # Load Client State
        client_state_file = os.path.join(parent_dir, logs_dir, 'client_state_1.json')
        with open(client_state_file, 'r') as json_file:
            client_state = json.load(json_file)

        # Load Replica State
        for replica_id in range(replica_count):
            replica_log_name = 'replica_state_{}.json'.format(replica_id + 1)
            full_replica_path = os.path.join(parent_dir, logs_dir, replica_log_name)
            with open(full_replica_path, 'r') as json_file:
                replica_state = json.load(json_file)
                replica_states.append(replica_state)

        for replica_state in replica_states:
            self.assertEqual(set(replica_state.items()), set(client_state.items()))


if __name__ == '__main__':
    unittest.main()
