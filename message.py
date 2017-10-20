import uuid
import nacl
import nacl.hash
import nacl.encoding
from collections import namedtuple


class Message:
    client_request = 'request'
    replica_response = 'response'
    request_shuttle = 'request_shuttle'
    OrderStatement = namedtuple('OrderStatement', 'slot operation replica_id')
    OrderProof = namedtuple(
        'OrderProof',
        'client_id request_id slot operation configuration order_statements'
    )

    def __init__(self, identifier):
        self.identifier = identifier

    def new_request(self, payload):
        request_id = uuid.uuid4()
        # TODO: make id explicit
        message_body = {'id': self.identifier, 'request_id': request_id, 'payload': payload}
        return self.client_request, message_body

    def new_response(self, payload):
        message_body = {'id': self.identifier, 'payload': payload}  # TODO: make id explicit
        return self.replica_response, message_body

    def new_request_shuttle(self, payload):
        message_body = {'replica_id': self.identifier, 'payload': payload}
        return self.request_shuttle, message_body

    def new_order_statement(self, previous_order_statement):
        order_statement = {
            'slot': previous_order_statement.get('slot', uuid.uuid4()),
            'operation': previous_order_statement['operation'],
            'replica_id': self.identifier
        }
        return order_statement

    def new_order_proof(self, previous_order_proof, new_order_statement):
        order_statements = previous_order_proof['order_statements'] + [new_order_statement]

        # TODO: figure out serializing named tuple
        order_proof = {
            'client_id': previous_order_proof['client_id'],
            'request_id': previous_order_proof['request_id'],
            'slot': previous_order_proof['slot'],
            'operation': previous_order_proof['operation'],
            'configuration': 'DEFAULT',
            'order_statements': order_statements
        }
        return order_proof

    def new_result_statement(self, operation, result):
        hashed_result = nacl.hash.sha256(bytes(result, 'utf-8'), encoder=nacl.encoding.HexEncoder)
        result_statement = {
            'operation': operation,
            'result': hashed_result,
            'replica_id': self.identifier
        }
        return result_statement

    def new_result_proof(self, previous_result_proof, new_result_statement):
        result_statements = previous_result_proof['result_statements'] + [new_result_statement]

        # TODO: figure out serializing named tuple
        result_proof = {
            'client_id': previous_result_proof['client_id'],
            'request_id': previous_result_proof['request_id'],
            'result': previous_result_proof['result'],
            'operation': previous_result_proof['operation'],
            'configuration': 'DEFAULT',
            'result_statements': result_statements
        }
        return result_proof
